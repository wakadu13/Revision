"""Transformation d'un cours (PDF, LaTeX) en page du wiki par Claude (API Anthropic).

- Clé : variable d'environnement ``ANTHROPIC_API_KEY`` du serveur (jamais dans le
  dépôt). Modèle : ``WIKI_CLAUDE_MODELE``, Claude Opus 5.5 par défaut.
- Les cours passent un par un dans un fil d'exécution du serveur : une
  transformation dure de quelques dizaines de secondes à plusieurs minutes,
  bien plus qu'une requête web (Cloudflare coupe à 100 s). La page
  /transformations/ suit l'avancement ; une transformation interrompue par un
  redémarrage du serveur repart au prochain passage sur cette page.
- La page produite est du Markdown, affiché comme toute note (HTML nettoyé). Une
  page déjà modifiée à la main n'est jamais écrasée : la version de Claude est
  enregistrée à côté.
"""

import base64
import hashlib
import logging
import os
import threading
from pathlib import PurePosixPath

from django.conf import settings
from django.db import close_old_connections, connection
from django.utils import timezone

from .models import Transformation
from .vault import INVALID_NAME_RE, get_vault

log = logging.getLogger(__name__)

MODELE_PAR_DEFAUT = "claude-opus-5-5"
# Assez pour la page d'un long cours et la réflexion du modèle (réponse en continu).
MAX_TOKENS = 128000
# Au-delà, le PDF passe par l'API Files : une requête est limitée à 32 Mo, et le
# base64 grossit le fichier d'un tiers.
PDF_EN_LIGNE_MAX = 20 * 1024 * 1024
EXTENSIONS_LATEX = {".tex", ".latex"}
# Modèles qui acceptent le repli automatique (« fallbacks ») quand un filtre de
# sécurité refuse un document légitime.
REPLI = {"claude-opus-5-5", "claude-opus-5", "claude-fable-5-1", "claude-sonnet-5-5"}
BETA_REPLI = "server-side-fallback-2026-07-01"
# Prix en dollars par million de jetons (entrée, sortie), pour l'estimation affichée.
PRIX = {
    "claude-opus-5-5": (4.0, 20.0),
    "claude-opus-5": (5.0, 25.0),
    "claude-sonnet-5-5": (2.0, 10.0),
    "claude-haiku-5-5": (0.10, 0.50),
    "claude-fable-5-1": (10.0, 50.0),
}

CONSIGNE = """Tu transformes un cours (PDF ou LaTeX) en une page de wiki au format Markdown d'Obsidian, \
pour qu'un étudiant le révise.

Contenu :
- Garde tout le contenu du cours : définitions, théorèmes, démonstrations, exemples, exercices, \
formules, tableaux, remarques. Ne résume pas et ne coupe rien.
- Reformule seulement pour que le texte se lise bien : des phrases complètes et des listes claires \
à la place des fragments de diapositives, sans répétitions d'en-têtes ni numéros de pages.
- Écris dans la langue du cours.

Forme :
- Commence par les propriétés : une ligne ---, puis tags: [2 à 5 mots-clés en minuscules, sans \
espaces], puis une ligne ---.
- Puis un titre # avec le nom du cours, un court paragraphe d'introduction qui dit ce que couvre le \
cours, et des sections ## et ### qui suivent son plan.
- Formules en LaTeX : $...$ dans le texte, $$...$$ seul sur ses lignes pour les formules centrées.
- Encadrés Obsidian pour ce qui doit ressortir, chaque ligne commençant par « > » :
  > [!definition] Nom de la notion
  > [!theoreme] Nom du théorème (propriétés, lois, formules à connaître)
  > [!demonstration]- Démonstration (le « - » la replie)
  > [!exemple] Titre
  > [!exercice] Titre
  > [!methode] Titre (méthodes, étapes à suivre)
  > [!remarque], > [!warning] (pièges et erreurs fréquentes), > [!retenir] (l'essentiel d'une partie)
- Tableaux Markdown pour les tableaux, blocs ``` avec le langage pour le code. Un schéma du cours \
qui s'y prête peut devenir un bloc ```mermaid ; sinon, décris-le en une ou deux phrases.
- Mets en **gras** les notions clés à leur première apparition.
- Pas de liens [[...]] vers d'autres pages ni d'images : elles n'existent pas dans le wiki.

Réponds uniquement par le contenu de la page, sans bloc de code autour et sans commentaire sur ta \
démarche."""


def disponible():
    """Une clé d'API est configurée sur le serveur."""
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def modele():
    return os.environ.get("WIKI_CLAUDE_MODELE", "").strip() or MODELE_PAR_DEFAUT


def cout(t):
    """Coût estimé d'une transformation en dollars, ou None (modèle inconnu)."""
    prix = PRIX.get(t.modele)
    if prix is None or not (t.jetons_entree or t.jetons_sortie):
        return None
    return (t.jetons_entree * prix[0] + t.jetons_sortie * prix[1]) / 1_000_000


def empreinte(texte):
    return hashlib.sha256(texte.encode("utf-8")).hexdigest()


# -- Demandes -------------------------------------------------------------------------------------


def demander_pdf(attachment, utilisateur=""):
    """Transformation d'un PDF du coffre en page (à côté de lui, même nom en .md)."""
    page = PurePosixPath(attachment.path).with_suffix(".md").as_posix()
    t = Transformation.objects.create(source=attachment.path.as_posix(), page=page,
                                      empreinte_page=_empreinte_actuelle(page), demande_par=utilisateur)
    lancer()
    return t


def demander_latex(nom, texte, page, utilisateur=""):
    """Transformation d'un cours LaTeX importé : remplace la page convertie sur place
    (``page``), si personne ne l'a modifiée d'ici là."""
    t = Transformation.objects.create(source=nom, texte_source=texte, page=page,
                                      empreinte_page=_empreinte_actuelle(page), demande_par=utilisateur)
    lancer()
    return t


def relancer(t):
    Transformation.objects.filter(pk=t.pk, statut=Transformation.ERREUR).update(
        statut=Transformation.ATTENTE, message="", debut=None, fin=None)
    lancer()


def _empreinte_actuelle(page):
    fichier = get_vault().root / page
    return empreinte(fichier.read_text(encoding="utf-8")) if fichier.is_file() else ""


# -- Traitement en arrière-plan -------------------------------------------------------------------

_verrou = threading.Lock()
_fil = None
_repris = False


def lancer():
    """Démarre le fil de traitement s'il ne tourne pas (rien en mode synchrone : tests)."""
    global _fil
    if not getattr(settings, "WIKI_CLAUDE_FIL", True):
        return
    with _verrou:
        if _fil is None:
            _fil = threading.Thread(target=_boucle, name="transformations-claude", daemon=True)
            _fil.start()


def _boucle():
    global _fil
    try:
        while True:
            close_old_connections()
            with _verrou:
                t = _prendre()
                if t is None:
                    _fil = None
                    return
            traiter(t)
    except Exception:  # noqa: BLE001 - le fil ne doit pas mourir en laissant _fil occupé
        log.exception("Transformations Claude : arrêt inattendu")
        with _verrou:
            _fil = None
    finally:
        connection.close()


def _prendre():
    """La prochaine transformation en attente, marquée « en cours » ; None s'il n'y en a plus."""
    global _repris
    if not _repris:
        # Interrompues par un arrêt du serveur (un seul processus sert le wiki) : on les reprend.
        Transformation.objects.filter(statut=Transformation.EN_COURS).update(statut=Transformation.ATTENTE)
        _repris = True
    for t in Transformation.objects.filter(statut=Transformation.ATTENTE).order_by("cree_le", "pk"):
        if Transformation.objects.filter(pk=t.pk, statut=Transformation.ATTENTE).update(
                statut=Transformation.EN_COURS, debut=timezone.now()):
            t.refresh_from_db()
            return t
    return None


def traiter_en_attente():
    """Traite toutes les transformations en attente, ici et maintenant (tests, commande)."""
    while (t := _prendre()) is not None:
        traiter(t)


def traiter(t):
    """Fait une transformation et enregistre son résultat (page écrite, ou erreur)."""
    t.modele = modele()
    try:
        texte, avertissement, usage = _transformer(t)
        t.jetons_entree, t.jetons_sortie = usage
        t.page_ecrite = _ecrire(t, texte, avertissement)
        t.statut = Transformation.FAIT
        t.message = avertissement or ""
    except Echec as e:
        t.statut, t.message = Transformation.ERREUR, str(e)
    except Exception:  # noqa: BLE001
        log.exception("Transformation Claude de %s", t.source)
        t.statut, t.message = Transformation.ERREUR, "Erreur inattendue (détail dans la fenêtre du serveur)."
    t.fin = timezone.now()
    t.save()


class Echec(Exception):
    """Transformation impossible ; le message est montré tel quel."""


def _client():
    import anthropic

    return anthropic.Anthropic(max_retries=3)


def _transformer(t):
    """(texte de la page, avertissement ou None, (jetons en entrée, en sortie))."""
    import anthropic

    if not disponible():
        raise Echec("Aucune clé ANTHROPIC_API_KEY sur le serveur.")
    client = _client()
    fichier_id = None
    try:
        if t.texte_source:
            document = {"type": "text", "text": f"Source LaTeX du cours « {t.nom} » :\n\n{t.texte_source}"}
        else:
            vault = get_vault()
            pdf = vault.attachments.get(t.source.lower())
            if pdf is None or not (vault.root / pdf.path).is_file():
                raise Echec("Le PDF n'est plus dans le wiki.")
            donnees = (vault.root / pdf.path).read_bytes()
            if len(donnees) > PDF_EN_LIGNE_MAX:
                fichier_id = client.files.upload(file=(pdf.path.name, donnees, "application/pdf")).id
                source = {"type": "file", "file_id": fichier_id}
            else:
                source = {"type": "base64", "media_type": "application/pdf",
                          "data": base64.standard_b64encode(donnees).decode("ascii")}
            document = {"type": "document", "source": source, "title": pdf.path.name}
        demande = {
            "model": t.modele,
            "max_tokens": MAX_TOKENS,
            "system": CONSIGNE,
            "output_config": {"effort": os.environ.get("WIKI_CLAUDE_EFFORT", "").strip() or "medium"},
            "messages": [{"role": "user", "content": [
                document,
                {"type": "text", "text": f"Transforme ce cours ({t.nom}) en page du wiki."},
            ]}],
        }
        if t.modele in REPLI:
            demande.update(betas=[BETA_REPLI], fallbacks="default")
        with client.beta.messages.stream(**demande) as flux:
            message = flux.get_final_message()
    except anthropic.AuthenticationError:
        raise Echec("Clé ANTHROPIC_API_KEY refusée par Anthropic : vérifiez-la.") from None
    except anthropic.PermissionDeniedError:
        raise Echec("Cette clé d'API n'a pas accès à ce modèle.") from None
    except anthropic.RateLimitError:
        raise Echec("Limite d'utilisation de l'API atteinte : relancez plus tard.") from None
    except anthropic.BadRequestError as e:
        raise Echec(f"Document refusé par l'API : {e.message}") from None
    except anthropic.APIStatusError as e:
        raise Echec(f"Service de Claude indisponible (erreur {e.status_code}) : relancez plus tard.") from None
    except anthropic.APIConnectionError:
        raise Echec("Serveur de Claude injoignable depuis le wiki : relancez plus tard.") from None
    finally:
        if fichier_id:
            try:
                client.files.delete(fichier_id)
            except anthropic.APIError:
                log.warning("Fichier %s non supprimé de l'API Files", fichier_id)

    usage = (message.usage.input_tokens or 0, message.usage.output_tokens or 0)
    if message.stop_reason == "refusal":
        raise Echec("Claude a refusé de transformer ce document.")
    texte = "".join(b.text for b in message.content if b.type == "text").strip()
    texte = _sans_cadre(texte)
    if not texte:
        raise Echec("Claude n'a renvoyé aucun texte.")
    avertissement = None
    if message.stop_reason == "max_tokens":
        avertissement = "Cours trop long : la fin de la page manque."
    return texte, avertissement, usage


def _sans_cadre(texte):
    """Retire un bloc ```markdown … ``` mis autour de toute la page."""
    lignes = texte.splitlines()
    if len(lignes) >= 2 and lignes[0].strip().lower() in ("```", "```markdown", "```md") and lignes[-1].strip() == "```":
        return "\n".join(lignes[1:-1]).strip()
    return texte


def _ecrire(t, texte, avertissement):
    """Écrit la page ; renvoie son chemin dans le coffre."""
    vault = get_vault()
    page = PurePosixPath(t.page)
    if page.suffix != ".md" or any(INVALID_NAME_RE.search(p) or p.startswith(".") for p in page.parts):
        raise Echec("Nom de page invalide.")
    if not t.texte_source:
        pdf = vault.attachments.get(t.source.lower())
        if pdf is not None:
            texte += f"\n\n## Document d'origine\n\n![[{vault.link_for(pdf)}]]"
    if avertissement:
        texte += f"\n\n> [!warning] {avertissement}\n> Le document d'origine reste disponible ci-dessus ou dans le dossier du cours."
    cible = vault.root / page
    if cible.is_file() and empreinte(cible.read_text(encoding="utf-8")) != t.empreinte_page:
        # Page modifiée (ou créée) par quelqu'un d'autre : la version de Claude va à côté.
        origine = page
        for i in range(1, 100):
            page = origine.with_name(f"{origine.stem} (Claude).md" if i == 1 else f"{origine.stem} (Claude {i}).md")
            cible = vault.root / page
            if not cible.exists():
                break
        else:
            raise Echec("Aucun nom libre pour la page.")
    if not cible.resolve().is_relative_to(vault.root.resolve()):
        raise Echec("Nom de page invalide.")
    cible.parent.mkdir(parents=True, exist_ok=True)
    cible.write_text(texte + "\n", encoding="utf-8", newline="\n")
    return page.as_posix()

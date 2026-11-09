"""Transformation d'un cours (PDF, LaTeX) en page du wiki par Claude (API Anthropic).

- Clé et modèle : saisis par un admin sur la page « Réglages de Claude »
  (base de données, jamais dans le dépôt) ; sinon variables d'environnement
  ``WIKI_CLAUDE_CLE`` (ou ``ANTHROPIC_API_KEY``) et ``WIKI_CLAUDE_MODELE``.
  Modèle par défaut : Claude Opus 5.5.
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

from . import paquets
from .models import ReglagesClaude, Transformation
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
# Lots (Message Batches) : moitié prix, résultats sous 24 heures ; vérifiés périodiquement.
REMISE_LOT = 0.5
INTERVALLE_LOTS_S = 600
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


# Modèles proposés sur la page des réglages : (identifiant, nom, aide).
MODELES = [
    ("claude-opus-5-5", "Claude Opus 5.5", "recommandé : les pages les plus fidèles, de l'ordre de 0,50 à 1 $ par cours"),
    ("claude-sonnet-5-5", "Claude Sonnet 5.5", "deux fois moins cher, un peu moins fin sur les cours difficiles"),
]


def cle_env():
    """Clé des variables d'environnement : WIKI_CLAUDE_CLE, sinon ANTHROPIC_API_KEY."""
    return (os.environ.get("WIKI_CLAUDE_CLE") or os.environ.get("ANTHROPIC_API_KEY") or "").strip()


def cle():
    """Clé d'API : celle saisie dans le site, sinon celle des variables d'environnement."""
    return ReglagesClaude.charger().cle or cle_env()


def verifier(cle_a_tester, modele_a_tester):
    """Demande à Anthropic si la clé est valable pour ce modèle (gratuit : aucun texte généré).

    Renvoie (True, None) si oui, (False, raison) si la clé est refusée, et
    (None, raison) si la vérification est impossible pour l'instant (réseau).
    """
    import anthropic

    try:
        anthropic.Anthropic(api_key=cle_a_tester, max_retries=1, timeout=20).models.retrieve(modele_a_tester)
    except anthropic.AuthenticationError:
        return False, "Clé refusée par Anthropic : vérifiez-la (elle commence par sk-ant-)."
    except (anthropic.PermissionDeniedError, anthropic.NotFoundError):
        return False, "Cette clé n'a pas accès à ce modèle."
    except (anthropic.APIConnectionError, anthropic.APIStatusError):
        return None, "Vérification impossible pour l'instant (réseau ou service d'Anthropic indisponible)."
    return True, None


def disponible():
    """Une clé d'API est configurée sur le serveur."""
    return bool(cle())


def modele():
    return ReglagesClaude.charger().modele or os.environ.get("WIKI_CLAUDE_MODELE", "").strip() or MODELE_PAR_DEFAUT


def cout(t):
    """Coût estimé d'une transformation en dollars, ou None (modèle inconnu). Les lots
    (Message Batches) sont facturés moitié prix."""
    prix = PRIX.get(t.modele)
    if prix is None or not (t.jetons_entree or t.jetons_sortie):
        return None
    total = (t.jetons_entree * prix[0] + t.jetons_sortie * prix[1]) / 1_000_000
    return total * REMISE_LOT if (t.options or {}).get("lot") else total


def empreinte(texte):
    return hashlib.sha256(texte.encode("utf-8")).hexdigest()


# -- Demandes -------------------------------------------------------------------------------------


def demander_pdf(attachment, utilisateur="", lot=False):
    """Transformation d'un PDF du coffre en page (à côté de lui, même nom en .md).
    ``lot`` : traitement différé dans un lot (moitié prix, résultat sous 24 h)."""
    page = PurePosixPath(attachment.path).with_suffix(".md").as_posix()
    t = Transformation.objects.create(source=attachment.path.as_posix(), page=page,
                                      empreinte_page=_empreinte_actuelle(page), demande_par=utilisateur,
                                      options={"lot": bool(lot)})
    lancer()
    return t


def demander_latex(nom, texte, page, utilisateur="", lot=False):
    """Transformation d'un cours LaTeX importé : remplace la page convertie sur place
    (``page``), si personne ne l'a modifiée d'ici là."""
    t = Transformation.objects.create(source=nom, texte_source=texte, page=page,
                                      empreinte_page=_empreinte_actuelle(page), demande_par=utilisateur,
                                      options={"lot": bool(lot)})
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
    """Fait un travail et enregistre son résultat (fichier écrit, brouillon, ou erreur) ;
    avec l'option « lot », la requête part dans un lot et le résultat viendra plus tard."""
    t.modele = modele()
    try:
        client = _client_pret()
        demande, fichier_id = _requete(t, client)
        if (t.options or {}).get("lot"):
            _envoyer_en_lot(t, client, demande, fichier_id)
            return
        try:
            message = _appeler(client, demande)
        finally:
            _supprimer_fichier(client, fichier_id)
        _terminer(t, message)
        return
    except Echec as e:
        t.statut, t.message = Transformation.ERREUR, str(e)
    except Exception:  # noqa: BLE001
        log.exception("Transformation Claude de %s", t.source)
        t.statut, t.message = Transformation.ERREUR, "Erreur inattendue (détail dans la fenêtre du serveur)."
    t.fin = timezone.now()
    t.save()


def _requete(t, client):
    """(requête à l'API, identifiant du fichier envoyé à l'API Files ou None) selon le genre."""
    if t.genre == Transformation.QCM:
        if (t.options or {}).get("variantes"):
            return _requete_variantes(t), None
        return _requete_qcm(t), None
    if t.genre == Transformation.VOCABULAIRE:
        return _requete_vocabulaire(t), None
    if t.genre == Transformation.FICHE:
        return _requete_fiche(t), None
    return _requete_transformation(t, client)


def _terminer(t, message):
    """Enregistre le résultat d'une réponse de Claude : page écrite, set publié ou brouillon."""
    try:
        if t.genre in (Transformation.QCM, Transformation.VOCABULAIRE):
            if t.genre == Transformation.QCM:
                resultat = _resultat_variantes if (t.options or {}).get("variantes") else _resultat_qcm
            else:
                resultat = _resultat_vocabulaire
            contenu, dossier, avertissement = resultat(t, message)
            t.jetons_entree, t.jetons_sortie = _usage(message)
            if (t.options or {}).get("publier"):
                t.page_ecrite = _publier_contenu(t.genre, dossier, contenu)
                t.statut, t.message = Transformation.FAIT, avertissement or ""
            else:
                # Brouillon : relu, corrigé et publié depuis la page des travaux.
                t.resultat = {"dossier": dossier, "contenu": contenu}
                t.statut = Transformation.BROUILLON
                t.message = " ".join(filter(None, [avertissement, "À relire avant publication."]))
        else:
            texte, avertissement = (_resultat_fiche if t.genre == Transformation.FICHE else _resultat_transformation)(t, message)
            t.page_ecrite = _ecrire(t, texte, avertissement)
            t.jetons_entree, t.jetons_sortie = _usage(message)
            t.statut, t.message = Transformation.FAIT, avertissement or ""
    except Echec as e:
        t.statut, t.message = Transformation.ERREUR, str(e)
    except Exception:  # noqa: BLE001
        log.exception("Transformation Claude de %s", t.source)
        t.statut, t.message = Transformation.ERREUR, "Erreur inattendue (détail dans la fenêtre du serveur)."
    t.fin = timezone.now()
    t.save()


def _supprimer_fichier(client, fichier_id):
    import anthropic

    if fichier_id:
        try:
            client.files.delete(fichier_id)
        except anthropic.APIError:
            log.warning("Fichier %s non supprimé de l'API Files", fichier_id)


class Echec(Exception):
    """Transformation impossible ; le message est montré tel quel."""


def _client():
    import anthropic

    return anthropic.Anthropic(api_key=cle(), max_retries=3)


def _demande(t, systeme, contenu, *, schema=None, max_tokens=MAX_TOKENS, effort=None, historique=()):
    """Requête à l'API : réponse en continu, effort réglable, repli automatique en cas de refus.
    ``t`` : le travail (son modèle), ou directement un identifiant de modèle ;
    ``historique`` : échanges précédents [(question, réponse)] placés avant ``contenu``."""
    modele_id = t if isinstance(t, str) else t.modele
    output_config = {"effort": effort or os.environ.get("WIKI_CLAUDE_EFFORT", "").strip() or "medium"}
    if schema is not None:
        output_config["format"] = {"type": "json_schema", "schema": schema}
    messages = []
    for question, reponse in historique:
        messages.append({"role": "user", "content": question})
        messages.append({"role": "assistant", "content": reponse})
    messages.append({"role": "user", "content": contenu})
    demande = {
        "model": modele_id,
        "max_tokens": max_tokens,
        "system": systeme,
        "output_config": output_config,
        "messages": messages,
    }
    if modele_id in REPLI:
        demande.update(betas=[BETA_REPLI], fallbacks="default")
    return demande


def _appeler(client, demande):
    """Envoie la requête ; les erreurs de l'API deviennent des Echec lisibles."""
    import anthropic

    try:
        with client.beta.messages.stream(**demande) as flux:
            message = flux.get_final_message()
    except anthropic.AuthenticationError:
        raise Echec("Clé d'API refusée par Anthropic : vérifiez-la sur la page « Réglages de Claude ».") from None
    except anthropic.PermissionDeniedError:
        raise Echec("Cette clé d'API n'a pas accès à ce modèle.") from None
    except anthropic.RateLimitError:
        raise Echec("Limite d'utilisation de l'API atteinte : relancez plus tard.") from None
    except anthropic.BadRequestError as e:
        if "credit balance" in str(e.message).lower():
            raise Echec("Plus de crédits d'API sur ce compte : relancez quand les crédits du mois suivant seront "
                        "arrivés (abonnement Max : 100 $ par mois), ou après un achat de crédits.") from None
        raise Echec(f"Document refusé par l'API : {e.message}") from None
    except anthropic.APIStatusError as e:
        raise Echec(f"Service de Claude indisponible (erreur {e.status_code}) : relancez plus tard.") from None
    except anthropic.APIConnectionError:
        raise Echec("Serveur de Claude injoignable depuis le wiki : relancez plus tard.") from None
    if message.stop_reason == "refusal":
        raise Echec("Claude a refusé ce travail.")
    return message


def _usage(message):
    return (message.usage.input_tokens or 0, message.usage.output_tokens or 0)


def _texte_reponse(message):
    return "".join(b.text for b in message.content if b.type == "text").strip()


def _client_pret():
    if not disponible():
        raise Echec("Aucune clé d'API : ajoutez-la sur la page « Réglages de Claude ».")
    return _client()


def _requete_transformation(t, client):
    """Requête de transformation d'un cours (PDF ou LaTeX) en page : (requête, fichier
    envoyé à l'API Files ou None — les gros PDF y passent plutôt qu'en ligne)."""
    import anthropic

    fichier_id = None
    if t.texte_source:
        document = {"type": "text", "text": f"Source LaTeX du cours « {t.nom} » :\n\n{t.texte_source}"}
    else:
        vault = get_vault()
        pdf = vault.attachments.get(t.source.lower())
        if pdf is None or not (vault.root / pdf.path).is_file():
            raise Echec("Le PDF n'est plus dans le wiki.")
        donnees = (vault.root / pdf.path).read_bytes()
        if len(donnees) > PDF_EN_LIGNE_MAX:
            try:
                fichier_id = client.files.upload(file=(pdf.path.name, donnees, "application/pdf")).id
            except anthropic.APIError:
                raise Echec("Envoi du PDF à Anthropic impossible : relancez plus tard.") from None
            source = {"type": "file", "file_id": fichier_id}
        else:
            source = {"type": "base64", "media_type": "application/pdf",
                      "data": base64.standard_b64encode(donnees).decode("ascii")}
        document = {"type": "document", "source": source, "title": pdf.path.name}
    return _demande(t, CONSIGNE, [
        document,
        {"type": "text", "text": f"Transforme ce cours ({t.nom}) en page du wiki."},
    ]), fichier_id


def _resultat_transformation(t, message):
    """(texte de la page, avertissement ou None)."""
    texte = _sans_cadre(_texte_reponse(message))
    if not texte:
        raise Echec("Claude n'a renvoyé aucun texte.")
    avertissement = "Cours trop long : la fin de la page manque." if message.stop_reason == "max_tokens" else None
    return texte, avertissement


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
    if cible.is_file():
        from . import historique

        historique.sauvegarder(page.as_posix(), cible.read_text(encoding="utf-8"), "Claude")
    cible.write_text(texte + "\n", encoding="utf-8", newline="\n")
    return page.as_posix()


# -- QCM et vocabulaire générés -------------------------------------------------------------------

DOSSIER_QCM = paquets.DOSSIER_QCM
MAX_TOKENS_GENERATION = 64000
NOMBRES_QUESTIONS = (10, 20, 30, 40)
MAX_MOTS = 150
# Cartes cochées d'office pour un paquet de vocabulaire : du français vers la langue apprise.
CARTES_PAR_DEFAUT = ("decouverte", "production", "contexte")
CATEGORIE_GENEREE = "Générés"
DOSSIER_VOCABULAIRE = "Vocabulaire"

CONSIGNE_QCM = """Tu écris des questions de révision à partir d'un cours, pour qu'un étudiant vérifie \
qu'il le connaît.

- Les questions sont fidèles au cours : rien qui n'y figure pas, aucune erreur. Elles couvrent tout le \
cours, des définitions aux applications, sans poser deux fois la même chose.
- Types (champ type) : QCM, une seule bonne réponse parmi 4 choix ; QCR, 2 ou 3 bonnes réponses parmi \
4 ou 5 choix ; TROU, une phrase du cours où un mot clé est remplacé par _____ ; QRC, une question à \
réponse courte (un mot, un nombre, une formule courte) ; FLASHCARD, une notion au recto, son explication \
au verso. Surtout des QCM, puis quelques QCR, TROU, QRC et FLASHCARD.
- choix : les choix (QCM et QCR ; sinon liste vide). reponses : les indices des bonnes réponses, à partir \
de 0 (QCM et QCR ; sinon liste vide). reponses_texte : les réponses acceptées, variantes d'écriture \
comprises (TROU et QRC ; sinon liste vide). verso : le dos de la carte (FLASHCARD ; sinon vide). \
consigne : une précision pour une QRC, sinon vide. explication : une phrase qui justifie la réponse.
- Mauvais choix plausibles, de longueur proche de la bonne réponse ; pas de « toutes les réponses » ni \
d'« aucune ». Varie la place de la bonne réponse.
- Formules en LaTeX entre $...$.
- titre : un nom court pour le QCM ; description : une phrase sur ce qu'il couvre.
Écris dans la langue du cours."""

_TEXTES = {"type": "array", "items": {"type": "string"}}
SCHEMA_QCM = {
    "type": "object",
    "properties": {
        "titre": {"type": "string"},
        "description": {"type": "string"},
        "questions": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "type": {"type": "string", "enum": ["QCM", "QCR", "TROU", "QRC", "FLASHCARD"]},
                "question": {"type": "string"},
                "choix": _TEXTES,
                "reponses": {"type": "array", "items": {"type": "integer"}},
                "reponses_texte": _TEXTES,
                "consigne": {"type": "string"},
                "verso": {"type": "string"},
                "explication": {"type": "string"},
            },
            "required": ["type", "question", "choix", "reponses", "reponses_texte", "consigne", "verso", "explication"],
            "additionalProperties": False,
        }},
    },
    "required": ["titre", "description", "questions"],
    "additionalProperties": False,
}

CONSIGNE_VOCABULAIRE = """Tu prépares des fiches de vocabulaire en {langue} pour un francophone qui révise.

On te donne une liste de mots ou d'expressions, un par ligne, en français ou en {langue}, parfois avec \
leur traduction. Pour chaque ligne, dans l'ordre, une fiche :
- mot : le mot en {langue}, sous sa forme de dictionnaire. En anglais : « a » ou « an » devant les noms \
dénombrables, « to » devant les verbes.
- traductions : une à trois traductions françaises usuelles, avec l'article pour les noms (« un emploi »).
- variantes : d'autres façons correctes de dire le mot en {langue} (orthographe britannique ou \
américaine, synonyme très proche), sinon liste vide.
- exemple : une phrase simple et naturelle en {langue} où le mot à retrouver est entre crochets, comme \
« She [achieved] her goal. ».
- exemple_traduction : la traduction française de l'exemple.
- prononciation : la prononciation en alphabet phonétique international, entre barres obliques.
- note : un piège, un registre, un faux ami ou une construction utile, sinon vide.
Ignore les lignes qui ne sont pas des mots (titres, numéros). Une fiche par mot.
titre : un nom court pour le paquet (le thème des mots) ; description : une phrase."""

SCHEMA_VOCABULAIRE = {
    "type": "object",
    "properties": {
        "titre": {"type": "string"},
        "description": {"type": "string"},
        "vocabulaire": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "mot": {"type": "string"},
                "traductions": _TEXTES,
                "variantes": _TEXTES,
                "exemple": {"type": "string"},
                "exemple_traduction": {"type": "string"},
                "prononciation": {"type": "string"},
                "note": {"type": "string"},
            },
            "required": ["mot", "traductions", "variantes", "exemple", "exemple_traduction", "prononciation", "note"],
            "additionalProperties": False,
        }},
    },
    "required": ["titre", "description", "vocabulaire"],
    "additionalProperties": False,
}


dossier_valide = paquets.dossier_valide


def demander_qcm(*, note=None, texte="", nombre=20, categorie="", titre="", utilisateur="", publier=False, lot=False):
    """QCM généré d'après une note du wiki (``note``) ou un texte collé."""
    source = note.path.as_posix() if note is not None else "Texte collé"
    if not categorie:
        categorie = (note.path.parent.name if note is not None else "") or CATEGORIE_GENEREE
    t = Transformation.objects.create(
        genre=Transformation.QCM, source=source, texte_source="" if note is not None else texte,
        page=f"{DOSSIER_QCM}/{categorie}", demande_par=utilisateur,
        options={"nombre": nombre, "categorie": categorie, "titre": titre,
                 "nom": note.title if note is not None else "", "publier": bool(publier), "lot": bool(lot)})
    lancer()
    return t


def demander_vocabulaire(*, mots, langue="Anglais", types=(), dossier="", titre="", utilisateur="", publier=False, lot=False):
    """Paquet de vocabulaire (un fichier de langue à lui) d'après une liste de mots collée."""
    dossier = dossier or DOSSIER_VOCABULAIRE
    t = Transformation.objects.create(
        genre=Transformation.VOCABULAIRE, source=titre or f"Vocabulaire ({langue})", texte_source=mots,
        page=f"{DOSSIER_QCM}/{dossier}", demande_par=utilisateur,
        options={"langue": langue, "exercices": list(types), "dossier": dossier, "titre": titre,
                 "publier": bool(publier), "lot": bool(lot)})
    lancer()
    return t


def _json_reponse(message, trop_long):
    import json

    if message.stop_reason == "max_tokens":
        raise Echec(trop_long)
    try:
        data = json.loads(_texte_reponse(message))
    except ValueError:
        raise Echec("Réponse de Claude illisible : relancez.") from None
    if not isinstance(data, dict):
        raise Echec("Réponse de Claude illisible : relancez.")
    return data


def _sans_vides(o):
    return {k: v for k, v in o.items() if v not in ("", [], None)}


def _nom_du_cours(t):
    options = t.options or {}
    if t.texte_source:
        return "texte collé"
    return options.get("nom") or PurePosixPath(t.source).stem


def _requete_qcm(t):
    """Requête d'un QCM d'après une page du wiki ou un texte collé."""
    options = t.options or {}
    nombre = options.get("nombre") if options.get("nombre") in NOMBRES_QUESTIONS else 20
    if t.texte_source:
        cours = t.texte_source
    else:
        fichier = get_vault().root / t.source
        if not fichier.is_file():
            raise Echec("La page du cours n'est plus dans le wiki.")
        cours = fichier.read_text(encoding="utf-8")
    return _demande(t, CONSIGNE_QCM, [
        {"type": "text", "text": f"Cours « {_nom_du_cours(t)} » :\n\n{cours}"},
        {"type": "text", "text": f"Écris {nombre} questions sur ce cours."},
    ], schema=SCHEMA_QCM, max_tokens=MAX_TOKENS_GENERATION)


def _resultat_qcm(t, message):
    """(JSON du set, catégorie, avertissement ou None)."""
    options = t.options or {}
    categorie = dossier_valide(options.get("categorie", "")) or CATEGORIE_GENEREE
    data = _json_reponse(message, "Réponse trop longue : demandez moins de questions.")
    questions, ecartees = _questions_valides(data)
    titre = str(options.get("titre") or data.get("titre") or _nom_du_cours(t)).strip()
    set_json = {"titre": titre, "description": str(data.get("description", "")).strip(),
                "genere_par": f"Claude ({t.modele})", "questions": questions}
    if not t.texte_source:
        set_json["source_page"] = t.source.removesuffix(".md")
    return set_json, categorie, _avertissement_ecartees(ecartees)


def _questions_valides(data):
    """Questions d'une réponse JSON de Claude qui passent le chargeur des sets
    (identifiants ia001, ia002…), et nombre de questions écartées."""
    from . import quiz

    questions, ecartees = [], 0
    for i, q in enumerate(data.get("questions") or [], start=1):
        q = _sans_vides(q if isinstance(q, dict) else {})
        q["id"] = f"ia{i:03d}"
        try:
            quiz.question_depuis_json(q, i, "question")
        except ValueError:
            ecartees += 1
            continue
        questions.append(q)
    if not questions:
        raise Echec("Claude n'a renvoyé aucune question utilisable : relancez.")
    return questions, ecartees


def _avertissement_ecartees(ecartees):
    if not ecartees:
        return None
    s = "s" if ecartees > 1 else ""
    return f"{ecartees} question{s} mal formée{s} écartée{s}."


def _requete_vocabulaire(t):
    langue = str((t.options or {}).get("langue") or "Anglais").strip()
    return _demande(t, CONSIGNE_VOCABULAIRE.format(langue=langue.lower()), [
        {"type": "text", "text": f"Mots à préparer en {langue.lower()} :\n\n{t.texte_source}"},
    ], schema=SCHEMA_VOCABULAIRE, max_tokens=MAX_TOKENS_GENERATION)


def _resultat_vocabulaire(t, message):
    """(JSON du paquet, dossier, avertissement ou None)."""
    from . import langues

    options = t.options or {}
    langue = str(options.get("langue") or "Anglais").strip()
    dossier = dossier_valide(options.get("dossier", "")) or DOSSIER_VOCABULAIRE
    types = [x for x in options.get("exercices") or [] if x in langues.TYPES_VOCABULAIRE] or list(langues.VOCABULAIRE_PAR_DEFAUT)
    data = _json_reponse(message, "Réponse trop longue : envoyez moins de mots à la fois.")
    titre = str(options.get("titre") or data.get("titre") or f"Vocabulaire ({langue})").strip()
    fiches = [_sans_vides(v) for v in data.get("vocabulaire") or [] if isinstance(v, dict)]
    paquet = paquets.paquet_vocabulaire(langue, titre, str(data.get("description", "")).strip(), types, fiches,
                                        f"Claude ({t.modele})")
    if not paquet["vocabulaire"]:
        raise Echec("Claude n'a renvoyé aucun mot utilisable : vérifiez la liste et relancez.")
    return paquet, dossier, None


def _publier_contenu(genre, dossier, contenu):
    """Écrit un set de QCM ou un paquet de langue dans le coffre ; renvoie son chemin."""
    try:
        if genre == Transformation.QCM:
            return paquets.ecrire_set_qcm(dossier, contenu)
        return paquets.ecrire_paquet_langue(dossier, contenu)
    except paquets.PaquetInvalide as e:
        raise Echec(str(e)) from None


def publier(t, contenu=None):
    """Publie un brouillon (tel quel, ou relu : ``contenu`` corrigé). Renvoie le chemin
    écrit ; lève Echec si le contenu ne passe pas le chargeur."""
    if t.statut != Transformation.BROUILLON or not t.resultat:
        raise Echec("Ce travail n'est pas un brouillon.")
    chemin = _publier_contenu(t.genre, t.resultat["dossier"], contenu if contenu is not None else t.resultat["contenu"])
    t.page_ecrite, t.resultat, t.statut, t.message = chemin, None, Transformation.FAIT, ""
    t.fin = timezone.now()
    t.save()
    return chemin


def supprimer_brouillon(t):
    t.resultat, t.statut, t.message = None, Transformation.ERREUR, "Brouillon supprimé sans publication."
    t.fin = timezone.now()
    t.save()


# -- Fiches de révision ---------------------------------------------------------------------------

CONSIGNE_FICHE = """Tu rédiges la fiche de révision d'une page de cours, pour un étudiant qui révise la veille d'un examen.

- Une seule page : l'essentiel, rien de plus. Pas de phrase d'introduction, pas de commentaire.
- Dans l'ordre du cours : définitions clés, formules et lois à connaître (en LaTeX : $...$ ou $$...$$), \
méthodes et étapes à suivre, pièges et erreurs fréquentes, ordres de grandeur et exemples très courts.
- Markdown d'Obsidian : sections ##, listes courtes, **gras** pour les mots clés, encadrés \
> [!definition], > [!theoreme], > [!methode], > [!warning] (pièges), > [!retenir] (l'essentiel en 5 lignes, à la fin).
- Rien qui ne soit pas dans la page. Pas de liens [[...]] ni d'images. Dans la langue de la page.
Réponds uniquement par le contenu de la fiche, sans bloc de code autour."""


def demander_fiche(note, utilisateur=""):
    """Fiche de révision d'une page du wiki, écrite à côté (« Page (Fiche).md »)."""
    page = note.path.with_name(f"{note.path.stem} (Fiche).md").as_posix()
    t = Transformation.objects.create(
        genre=Transformation.FICHE, source=note.path.as_posix(), page=page,
        empreinte_page=_empreinte_actuelle(page), demande_par=utilisateur, options={"nom": note.title, "cle": note.key})
    lancer()
    return t


def _requete_fiche(t):
    fichier = get_vault().root / t.source
    if not fichier.is_file():
        raise Echec("La page n'est plus dans le wiki.")
    nom = (t.options or {}).get("nom") or PurePosixPath(t.source).stem
    return _demande(t, CONSIGNE_FICHE, [
        {"type": "text", "text": f"Page « {nom} » :\n\n{fichier.read_text(encoding='utf-8')}"},
        {"type": "text", "text": "Rédige la fiche de révision de cette page."},
    ], max_tokens=MAX_TOKENS_GENERATION)


def _resultat_fiche(t, message):
    """(texte de la fiche, avertissement ou None)."""
    texte = _sans_cadre(_texte_reponse(message))
    if not texte:
        raise Echec("Claude n'a renvoyé aucun texte.")
    nom = (t.options or {}).get("nom") or PurePosixPath(t.source).stem
    cle = (t.options or {}).get("cle") or PurePosixPath(t.source).with_suffix("").as_posix()
    texte = f"> [!abstract] Fiche de révision de [[{cle}|{nom}]]\n\n{texte}"
    avertissement = "Fiche trop longue : la fin manque." if message.stop_reason == "max_tokens" else None
    return texte, avertissement


# -- « Explique-moi » (question de QCM) et « Améliorer la rédaction » (éditeur) --------------------

MODELE_EXPLICATIONS = "claude-haiku-5-5"  # explications courtes : le modèle le moins cher suffit
MAX_CHARS_COURS = 80_000
MAX_CHARS_AMELIORER = 12_000

CONSIGNE_EXPLICATION = """Tu expliques à un étudiant la réponse d'une question de révision, en français, en 4 à 8 phrases.
- Dis pourquoi la bonne réponse est juste et, si des choix étaient proposés, pourquoi les autres sont faux.
- Appuie-toi sur le cours fourni s'il y en a un ; sinon dis que tu expliques d'après tes connaissances générales.
- Markdown simple (gras, listes courtes, formules en $...$). Pas de titre, pas de préambule."""

CONSIGNE_AMELIORER = """Tu améliores la rédaction d'un extrait de page de wiki (notes de cours) en Markdown.
- Corrige l'orthographe, la grammaire et la ponctuation ; rends les phrases claires et fluides ; garde le sens, \
le niveau de détail, l'ordre et la langue d'origine. N'ajoute aucune information.
- Conserve tel quel tout ce qui est du balisage : titres #, listes, tableaux, blocs de code, formules LaTeX \
($...$, $$...$$), liens [[...]] et ![[...]], encadrés > [!…], propriétés --- en tête.
Réponds uniquement par le texte corrigé, sans commentaire ni bloc de code autour."""


def expliquer(qset, question):
    """Explication d'une question par Claude (Haiku), d'après la page du cours quand le
    set en vient. Renvoie (texte Markdown, (jetons entrée, sortie), modèle)."""
    client = _client_pret()
    vault = get_vault()
    note = vault.notes.get(qset.source_page.lower()) if qset.source_page else None
    contexte = ""
    if note is not None:
        contexte = (vault.root / note.path).read_text(encoding="utf-8")[:MAX_CHARS_COURS]
    lignes = [f"Question ({question.type}) : {question.enonce}"]
    if question.consigne:
        lignes.append(f"Consigne : {question.consigne}")
    if question.choix:
        lignes.append("Choix : " + " ; ".join(f"{chr(65 + i)}. {c}" for i, c in enumerate(question.choix)))
        lignes.append("Bonne(s) réponse(s) : " + ", ".join(chr(65 + i) for i in question.reponses))
    if question.reponses_texte:
        lignes.append("Réponse attendue : " + " / ".join(question.reponses_texte))
    if question.verso:
        lignes.append(f"Réponse : {question.verso}")
    if question.explication:
        lignes.append(f"Explication déjà donnée (à développer) : {question.explication}")
    contenu = []
    if contexte:
        contenu.append({"type": "text", "text": f"Cours « {note.title} » :\n\n{contexte}"})
    contenu.append({"type": "text", "text": "\n".join(lignes) + ("\n\nAucun cours fourni." if not contexte else "")})
    message = _appeler(client, _demande(MODELE_EXPLICATIONS, CONSIGNE_EXPLICATION, contenu, max_tokens=1500, effort="low"))
    texte = _texte_reponse(message)
    if not texte:
        raise Echec("Claude n'a renvoyé aucune explication.")
    return texte, _usage(message), MODELE_EXPLICATIONS


def ameliorer(texte):
    """Texte Markdown relu et corrigé par Claude (modèle réglé). Renvoie (texte, usage)."""
    if len(texte) > MAX_CHARS_AMELIORER:
        raise Echec(f"Sélectionnez un passage plus court ({MAX_CHARS_AMELIORER} caractères au plus).")
    client = _client_pret()
    message = _appeler(client, _demande(modele(), CONSIGNE_AMELIORER, [{"type": "text", "text": texte}],
                                        max_tokens=16000, effort="low"))
    resultat = _sans_cadre(_texte_reponse(message))
    if not resultat:
        raise Echec("Claude n'a renvoyé aucun texte.")
    if message.stop_reason == "max_tokens":
        raise Echec("Passage trop long pour une seule relecture : sélectionnez-en une partie.")
    return resultat, _usage(message)


# ---------------------------------------------------------------------------
# Correction d'une question signalée
# ---------------------------------------------------------------------------
CONSIGNE_CORRECTION = """Tu corriges une question de révision (QCM) qu'un étudiant a signalée : erreur, ambiguïté, \
coquille ou réponse discutable. Appuie-toi sur le cours fourni quand il y en a un. Renvoie la question corrigée \
complète, du même type si possible, avec une bonne réponse sans ambiguïté et une explication courte ; et dans \
« modification », en une ou deux phrases, ce que tu as changé et pourquoi. Si le signalement est infondé, renvoie \
la question inchangée et explique en quoi elle est juste. Les formules s'écrivent en LaTeX entre $."""

_QUESTION_SCHEMA = SCHEMA_QCM["properties"]["questions"]["items"]
SCHEMA_CORRECTION = {
    "type": "object",
    "properties": {**_QUESTION_SCHEMA["properties"], "modification": {"type": "string"}},
    "required": [*_QUESTION_SCHEMA["required"], "modification"],
    "additionalProperties": False,
}
CHAMPS_QUESTION = ("type", "question", "choix", "reponses", "reponses_texte", "consigne", "verso", "explication")


def question_en_json(question):
    """Une question du set sous la forme du JSON des fichiers de QCM."""
    return {"type": question.type, "question": question.enonce, "choix": question.choix, "reponses": question.reponses,
            "reponses_texte": question.reponses_texte, "consigne": question.consigne, "verso": question.verso,
            "explication": question.explication}


def corriger_question(qset, question, commentaires):
    """Correction d'une question signalée, proposée par Claude d'après le cours quand le
    set en vient. Renvoie (question JSON corrigée, note de modification, usage, modèle) ;
    la question est validée comme à l'import d'un set."""
    import json as json_module

    from . import quiz

    client = _client_pret()
    vault = get_vault()
    note = vault.notes.get(qset.source_page.lower()) if qset.source_page else None
    contenu = []
    if note is not None:
        contexte = (vault.root / note.path).read_text(encoding="utf-8")[:MAX_CHARS_COURS]
        contenu.append({"type": "text", "text": f"Cours « {note.title} » :\n\n{contexte}"})
    texte = f"Question signalée (set « {qset.titre} ») :\n{json_module.dumps(question_en_json(question), ensure_ascii=False, indent=1)}"
    texte += "\n\nSignalement(s) :\n" + "\n".join(f"- {c}" for c in commentaires if c) if any(commentaires) else "\n\nAucun commentaire : vérifie la question."
    if note is None:
        texte += "\n\nAucun cours fourni."
    contenu.append({"type": "text", "text": texte})
    message = _appeler(client, _demande(modele(), CONSIGNE_CORRECTION, contenu, schema=SCHEMA_CORRECTION,
                                        max_tokens=4000, effort="medium"))
    try:
        data = json_module.loads(_texte_reponse(message))
    except ValueError as e:
        raise Echec(f"Réponse de Claude illisible : {e}") from e
    modification = str(data.pop("modification", "")).strip()
    nouvelle = {k: v for k, v in data.items() if k in CHAMPS_QUESTION and v not in ("", [], None)}
    try:
        quiz.question_depuis_json({**nouvelle, "id": question.id}, 0, "correction")
    except ValueError as e:
        raise Echec(f"Correction invalide : {e}") from e
    return nouvelle, modification, _usage(message), modele()


# ---------------------------------------------------------------------------
# Variantes des questions ratées
# ---------------------------------------------------------------------------
CONSIGNE_VARIANTES = """Tu écris des variantes de questions de révision qu'un étudiant a ratées, pour qu'il retravaille \
la notion au lieu de réapprendre une réponse par cœur. Pour chaque question d'origine, écris une question nouvelle \
sur la même notion : angle différent (application, contre-exemple, cas particulier, autre formulation, calcul \
voisin), même difficulté ou un peu plus, en variant les types (QCM, QCR, TROU, QRC, FLASHCARD). Jamais la même \
question reformulée. Fidèle au cours fourni quand il y en a un ; explication courte. Les formules s'écrivent en LaTeX \
entre $. Réponds avec le titre, une description et la liste des questions."""
MAX_VARIANTES = 20


def demander_variantes(qset, question_ids, utilisateur=""):
    """Brouillon de QCM fait de variantes des questions ratées d'un set (une par question)."""
    titre = f"Variantes · {qset.titre}"
    t = Transformation.objects.create(
        genre=Transformation.QCM, source=qset.path.as_posix() if qset.path else qset.id,
        page=f"{DOSSIER_QCM}/{qset.categorie}", demande_par=utilisateur,
        options={"variantes": list(question_ids)[:MAX_VARIANTES], "set_source": qset.id, "categorie": qset.categorie,
                 "titre": titre, "nom": titre, "publier": False})
    lancer()
    return t


def _set_des_variantes(options):
    from . import quiz

    qset = quiz.get_library().get(str(options.get("set_source", "")))
    if qset is None:
        raise Echec("Le set d'origine n'est plus dans le wiki.")
    return qset


def _requete_variantes(t):
    """Requête de variantes des questions ratées d'un set."""
    import json as json_module

    options = t.options or {}
    qset = _set_des_variantes(options)
    voulues = set(options.get("variantes") or [])
    questions = [q for q in qset.questions if q.id in voulues]
    if not questions:
        raise Echec("Les questions ratées n'existent plus dans le set.")
    vault = get_vault()
    note = vault.notes.get(qset.source_page.lower()) if qset.source_page else None
    contenu = []
    if note is not None:
        contexte = (vault.root / note.path).read_text(encoding="utf-8")[:MAX_CHARS_COURS]
        contenu.append({"type": "text", "text": f"Cours « {note.title} » :\n\n{contexte}"})
    n = len(questions)
    texte = "Questions ratées :\n" + json_module.dumps([question_en_json(q) for q in questions], ensure_ascii=False, indent=1)
    texte += f"\n\nÉcris {n} variante{'s' if n > 1 else ''} : une par question, dans le même ordre."
    if note is None:
        texte += "\n\nAucun cours fourni : reste fidèle aux questions et à leurs explications."
    contenu.append({"type": "text", "text": texte})
    return _demande(t, CONSIGNE_VARIANTES, contenu, schema=SCHEMA_QCM, max_tokens=MAX_TOKENS_GENERATION)


def _resultat_variantes(t, message):
    """(JSON du set de variantes, catégorie, avertissement ou None)."""
    options = t.options or {}
    qset = _set_des_variantes(options)
    data = _json_reponse(message, "Réponse trop longue : demandez des variantes pour moins de questions.")
    questions_json, ecartees = _questions_valides(data)
    set_json = {"titre": str(options.get("titre") or f"Variantes · {qset.titre}"),
                "description": f"Variantes des questions ratées de « {qset.titre} », pour retravailler les notions "
                               "sans apprendre les réponses par cœur.",
                "genere_par": f"Claude ({t.modele})", "questions": questions_json}
    if qset.source_page:
        set_json["source_page"] = qset.source_page
    return set_json, dossier_valide(qset.categorie) or CATEGORIE_GENEREE, _avertissement_ecartees(ecartees)


# ---------------------------------------------------------------------------
# Réponses rédigées (QRC) corrigées par Claude ; coût du mois et plafond
# ---------------------------------------------------------------------------
CONSIGNE_QRC = """Tu corriges la réponse rédigée d'un étudiant à une question de révision, en français. Compare le fond \
avec la ou les réponses attendues : une formulation différente, plus précise ou plus complète est juste. Verdict \
« juste » si l'essentiel y est sans erreur, « partiel » s'il manque un élément important ou s'il y a une imprécision, \
« faux » sinon (hors sujet, contresens, réponse vide de sens). « retour » : une à trois phrases qui disent ce qui est \
bon, ce qui manque ou ce qui est faux, sans répéter la question ; tutoie l'étudiant."""
SCHEMA_QRC = {
    "type": "object",
    "properties": {"verdict": {"type": "string", "enum": ["juste", "partiel", "faux"]}, "retour": {"type": "string"}},
    "required": ["verdict", "retour"],
    "additionalProperties": False,
}
MAX_TOKENS_QRC = 600
MAX_CHARS_REPONSE = 2000


def corriger_qrc(qset, question, reponse):
    """Verdict de Claude (Haiku) sur une réponse rédigée : (verdict, retour, usage, modèle)."""
    client = _client_pret()
    lignes = [f"Question : {question.enonce}"]
    if question.consigne:
        lignes.append(f"Consigne : {question.consigne}")
    lignes.append("Réponse(s) attendue(s) : " + " / ".join(question.reponses_texte))
    if question.explication:
        lignes.append(f"Explication du corrigé : {question.explication}")
    lignes.append(f"Réponse de l'étudiant : {reponse[:MAX_CHARS_REPONSE]}")
    message = _appeler(client, _demande(MODELE_EXPLICATIONS, CONSIGNE_QRC, [{"type": "text", "text": "\n".join(lignes)}],
                                        schema=SCHEMA_QRC, max_tokens=MAX_TOKENS_QRC, effort="low"))
    data = _json_reponse(message, "Réponse de Claude trop longue.")
    verdict = data.get("verdict") if data.get("verdict") in ("juste", "partiel", "faux") else "faux"
    return verdict, str(data.get("retour", "")).strip(), _usage(message), MODELE_EXPLICATIONS


def cout_jetons(modele_id, entree, sortie):
    """Coût en dollars d'un appel, ou None si le modèle est inconnu."""
    prix = PRIX.get(modele_id)
    if prix is None:
        return None
    return (entree * prix[0] + sortie * prix[1]) / 1_000_000


def _debut_du_mois():
    return timezone.localtime().replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def cout_a_la_demande_du_mois():
    """Dollars dépensés ce mois-ci par les usages à la demande (explications, corrections
    de réponses rédigées, tuteur), ceux que le plafond limite."""
    from .models import Explication, UsageClaude

    debut = _debut_du_mois()
    total = 0.0
    for e in Explication.objects.filter(cree_le__gte=debut):
        total += cout_jetons(e.modele, e.jetons_entree, e.jetons_sortie) or 0.0
    for u in UsageClaude.objects.filter(cree_le__gte=debut):
        total += cout_jetons(u.modele, u.jetons_entree, u.jetons_sortie) or 0.0
    return total


def cout_du_mois():
    """Dollars dépensés ce mois-ci, tout compris (transformations terminées incluses)."""
    total = cout_a_la_demande_du_mois()
    for t in Transformation.objects.filter(fin__gte=_debut_du_mois()):
        total += cout(t) or 0.0
    return total


def plafond_atteint():
    """Vrai si les usages à la demande du mois dépassent le plafond des réglages (0 : pas de plafond)."""
    plafond = ReglagesClaude.charger().plafond_mensuel
    return plafond > 0 and cout_a_la_demande_du_mois() >= plafond


def noter_usage(genre, player, modele_id, usage):
    from .models import UsageClaude

    UsageClaude.objects.create(genre=genre, player=player, modele=modele_id, jetons_entree=usage[0], jetons_sortie=usage[1])


# ---------------------------------------------------------------------------
# Lots (Message Batches) : moitié prix, résultats sous 24 heures
# ---------------------------------------------------------------------------
_fil_lots = None


def _envoyer_en_lot(t, client, demande, fichier_id):
    """Dépose la requête dans un lot ; le résultat sera récupéré par surveiller_lots()."""
    import anthropic

    params = {k: v for k, v in demande.items() if k != "betas"}
    betas = demande.get("betas") or []
    try:
        lot = client.beta.messages.batches.create(requests=[{"custom_id": f"t{t.pk}", "params": params}],
                                                  **({"betas": betas} if betas else {}))
    except anthropic.APIError as e:
        _supprimer_fichier(client, fichier_id)
        raise Echec(f"Envoi du lot refusé par l'API : {getattr(e, 'message', e)}") from None
    options = dict(t.options or {})
    if fichier_id:
        options["fichier_api"] = fichier_id
    t.options, t.lot_id, t.statut = options, lot.id, Transformation.LOT
    t.message = "Dans un lot : résultat sous 24 heures, moitié prix."
    t.save()
    surveiller_lots()


def surveiller_lots():
    """Démarre, s'il ne tourne pas, le fil qui vérifie les lots en attente toutes les
    INTERVALLE_LOTS_S secondes (rien en mode synchrone : tests)."""
    global _fil_lots
    if not getattr(settings, "WIKI_CLAUDE_FIL", True):
        return
    with _verrou:
        if _fil_lots is None and Transformation.objects.filter(statut=Transformation.LOT).exists():
            _fil_lots = threading.Thread(target=_boucle_lots, name="lots-claude", daemon=True)
            _fil_lots.start()


def _boucle_lots():
    global _fil_lots
    try:
        while True:
            close_old_connections()
            try:
                verifier_lots()
            except Exception:  # noqa: BLE001
                log.exception("Lots Claude : vérification en échec")
            if not Transformation.objects.filter(statut=Transformation.LOT).exists():
                return
            time.sleep(getattr(settings, "WIKI_CLAUDE_LOTS_INTERVALLE", INTERVALLE_LOTS_S))
    finally:
        with _verrou:
            _fil_lots = None
        connection.close()


def verifier_lots():
    """Interroge l'API pour chaque lot en attente ; enregistre les résultats des lots
    terminés. Renvoie le nombre de transformations terminées."""
    import anthropic

    en_attente = list(Transformation.objects.filter(statut=Transformation.LOT).exclude(lot_id=""))
    if not en_attente:
        return 0
    client = _client_pret()
    terminees = 0
    for lot_id in sorted({t.lot_id for t in en_attente}):
        membres = {f"t{t.pk}": t for t in en_attente if t.lot_id == lot_id}
        try:
            lot = client.beta.messages.batches.retrieve(lot_id)
            if lot.processing_status != "ended":
                continue
            resultats = list(client.beta.messages.batches.results(lot_id))
        except anthropic.APIError as e:
            log.warning("Lot %s : %s", lot_id, e)
            continue
        vus = set()
        for r in resultats:
            t = membres.get(r.custom_id)
            if t is None:
                continue
            vus.add(r.custom_id)
            if r.result.type == "succeeded":
                _terminer(t, r.result.message)
            else:
                detail = getattr(getattr(r.result, "error", None), "message", "") or r.result.type
                t.statut, t.message, t.fin = Transformation.ERREUR, f"Lot : {detail}", timezone.now()
                t.save()
            _supprimer_fichier(client, (t.options or {}).get("fichier_api"))
            terminees += 1
        for custom_id, t in membres.items():
            if custom_id not in vus:
                t.statut, t.message, t.fin = Transformation.ERREUR, "Lot terminé sans résultat pour ce travail.", timezone.now()
                t.save()
                terminees += 1
    return terminees


# ---------------------------------------------------------------------------
# Tuteur : questions sur la page ouverte
# ---------------------------------------------------------------------------
CONSIGNE_TUTEUR = """Tu es le tuteur d'un étudiant qui révise la page de cours fournie. Réponds en français, en 3 à 10 \
phrases, en Markdown léger (gras pour les mots clés, listes courtes, formules en LaTeX entre $). Appuie-toi d'abord sur \
la page : cite la section ou la définition utile. Si la réponse n'est pas dans la page, dis-le clairement, puis réponds \
avec prudence d'après tes connaissances. Si l'étudiant propose un raisonnement, dis ce qui est juste et ce qui ne l'est \
pas. Tutoie l'étudiant ; pas de formule de politesse."""
MAX_TOKENS_TUTEUR = 1500
MAX_CHARS_QUESTION = 2000
HISTORIQUE_TUTEUR = 6  # derniers échanges rejoués


def tuteur(note, question, historique=()):
    """Réponse du tuteur (Haiku) à une question sur une page : (texte Markdown, usage, modèle)."""
    client = _client_pret()
    vault = get_vault()
    page = (vault.root / note.path).read_text(encoding="utf-8")[:MAX_CHARS_COURS]
    systeme = f"{CONSIGNE_TUTEUR}\n\nPage « {note.title} » :\n\n{page}"
    message = _appeler(client, _demande(MODELE_EXPLICATIONS, systeme, question[:MAX_CHARS_QUESTION],
                                        max_tokens=MAX_TOKENS_TUTEUR, effort="low", historique=historique))
    texte = _texte_reponse(message)
    if not texte:
        raise Echec("Claude n'a renvoyé aucune réponse.")
    return texte, _usage(message), MODELE_EXPLICATIONS

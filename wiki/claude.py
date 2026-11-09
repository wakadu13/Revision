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
    """Fait un travail et enregistre son résultat (fichier écrit, ou erreur)."""
    t.modele = modele()
    try:
        if t.genre in (Transformation.QCM, Transformation.VOCABULAIRE):
            generer = _generer_qcm if t.genre == Transformation.QCM else _generer_vocabulaire
            contenu, dossier, avertissement, usage = generer(t)
            t.jetons_entree, t.jetons_sortie = usage
            if (t.options or {}).get("publier"):
                t.page_ecrite = _publier_contenu(t.genre, dossier, contenu)
                t.statut, t.message = Transformation.FAIT, avertissement or ""
            else:
                # Brouillon : relu, corrigé et publié depuis la page des travaux.
                t.resultat = {"dossier": dossier, "contenu": contenu}
                t.statut = Transformation.BROUILLON
                t.message = " ".join(filter(None, [avertissement, "À relire avant publication."]))
            t.fin = timezone.now()
            t.save()
            return
        if t.genre == Transformation.FICHE:
            texte, avertissement, usage = _generer_fiche(t)
        else:
            texte, avertissement, usage = _transformer(t)
        t.page_ecrite = _ecrire(t, texte, avertissement)
        t.jetons_entree, t.jetons_sortie = usage
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

    return anthropic.Anthropic(api_key=cle(), max_retries=3)


def _demande(t, systeme, contenu, *, schema=None, max_tokens=MAX_TOKENS, effort=None):
    """Requête à l'API : réponse en continu, effort réglable, repli automatique en cas de refus.
    ``t`` : le travail (son modèle), ou directement un identifiant de modèle."""
    modele_id = t if isinstance(t, str) else t.modele
    output_config = {"effort": effort or os.environ.get("WIKI_CLAUDE_EFFORT", "").strip() or "medium"}
    if schema is not None:
        output_config["format"] = {"type": "json_schema", "schema": schema}
    demande = {
        "model": modele_id,
        "max_tokens": max_tokens,
        "system": systeme,
        "output_config": output_config,
        "messages": [{"role": "user", "content": contenu}],
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


def _transformer(t):
    """(texte de la page, avertissement ou None, (jetons en entrée, en sortie))."""
    import anthropic

    client = _client_pret()
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
                try:
                    fichier_id = client.files.upload(file=(pdf.path.name, donnees, "application/pdf")).id
                except anthropic.APIError:
                    raise Echec("Envoi du PDF à Anthropic impossible : relancez plus tard.") from None
                source = {"type": "file", "file_id": fichier_id}
            else:
                source = {"type": "base64", "media_type": "application/pdf",
                          "data": base64.standard_b64encode(donnees).decode("ascii")}
            document = {"type": "document", "source": source, "title": pdf.path.name}
        message = _appeler(client, _demande(t, CONSIGNE, [
            document,
            {"type": "text", "text": f"Transforme ce cours ({t.nom}) en page du wiki."},
        ]))
    finally:
        if fichier_id:
            try:
                client.files.delete(fichier_id)
            except anthropic.APIError:
                log.warning("Fichier %s non supprimé de l'API Files", fichier_id)

    texte = _sans_cadre(_texte_reponse(message))
    if not texte:
        raise Echec("Claude n'a renvoyé aucun texte.")
    avertissement = "Cours trop long : la fin de la page manque." if message.stop_reason == "max_tokens" else None
    return texte, avertissement, _usage(message)


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


def demander_qcm(*, note=None, texte="", nombre=20, categorie="", titre="", utilisateur="", publier=False):
    """QCM généré d'après une note du wiki (``note``) ou un texte collé."""
    source = note.path.as_posix() if note is not None else "Texte collé"
    if not categorie:
        categorie = (note.path.parent.name if note is not None else "") or CATEGORIE_GENEREE
    t = Transformation.objects.create(
        genre=Transformation.QCM, source=source, texte_source="" if note is not None else texte,
        page=f"{DOSSIER_QCM}/{categorie}", demande_par=utilisateur,
        options={"nombre": nombre, "categorie": categorie, "titre": titre,
                 "nom": note.title if note is not None else "", "publier": bool(publier)})
    lancer()
    return t


def demander_vocabulaire(*, mots, langue="Anglais", types=(), dossier="", titre="", utilisateur="", publier=False):
    """Paquet de vocabulaire (un fichier de langue à lui) d'après une liste de mots collée."""
    dossier = dossier or DOSSIER_VOCABULAIRE
    t = Transformation.objects.create(
        genre=Transformation.VOCABULAIRE, source=titre or f"Vocabulaire ({langue})", texte_source=mots,
        page=f"{DOSSIER_QCM}/{dossier}", demande_par=utilisateur,
        options={"langue": langue, "exercices": list(types), "dossier": dossier, "titre": titre, "publier": bool(publier)})
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


def _generer_qcm(t):
    """(JSON du set, catégorie, avertissement ou None, usage)."""
    from . import quiz

    options = t.options or {}
    categorie = dossier_valide(options.get("categorie", "")) or CATEGORIE_GENEREE
    nombre = options.get("nombre") if options.get("nombre") in NOMBRES_QUESTIONS else 20
    if t.texte_source:
        cours, nom = t.texte_source, "texte collé"
    else:
        fichier = get_vault().root / t.source
        if not fichier.is_file():
            raise Echec("La page du cours n'est plus dans le wiki.")
        cours, nom = fichier.read_text(encoding="utf-8"), options.get("nom") or PurePosixPath(t.source).stem
    client = _client_pret()
    message = _appeler(client, _demande(t, CONSIGNE_QCM, [
        {"type": "text", "text": f"Cours « {nom} » :\n\n{cours}"},
        {"type": "text", "text": f"Écris {nombre} questions sur ce cours."},
    ], schema=SCHEMA_QCM, max_tokens=MAX_TOKENS_GENERATION))
    data = _json_reponse(message, "Réponse trop longue : demandez moins de questions.")

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
    titre = str(options.get("titre") or data.get("titre") or nom).strip()
    set_json = {"titre": titre, "description": str(data.get("description", "")).strip(),
                "genere_par": f"Claude ({t.modele})", "questions": questions}
    if not t.texte_source:
        set_json["source_page"] = t.source.removesuffix(".md")
    avertissement = f"{ecartees} question{'s' if ecartees > 1 else ''} mal formée{'s' if ecartees > 1 else ''} écartée{'s' if ecartees > 1 else ''}." if ecartees else None
    return set_json, categorie, avertissement, _usage(message)


def _generer_vocabulaire(t):
    """(JSON du paquet, dossier, avertissement ou None, usage)."""
    from . import langues

    options = t.options or {}
    langue = str(options.get("langue") or "Anglais").strip()
    dossier = dossier_valide(options.get("dossier", "")) or DOSSIER_VOCABULAIRE
    types = [x for x in options.get("exercices") or [] if x in langues.TYPES_VOCABULAIRE] or list(langues.VOCABULAIRE_PAR_DEFAUT)
    client = _client_pret()
    message = _appeler(client, _demande(t, CONSIGNE_VOCABULAIRE.format(langue=langue.lower()), [
        {"type": "text", "text": f"Mots à préparer en {langue.lower()} :\n\n{t.texte_source}"},
    ], schema=SCHEMA_VOCABULAIRE, max_tokens=MAX_TOKENS_GENERATION))
    data = _json_reponse(message, "Réponse trop longue : envoyez moins de mots à la fois.")

    titre = str(options.get("titre") or data.get("titre") or f"Vocabulaire ({langue})").strip()
    fiches = [_sans_vides(v) for v in data.get("vocabulaire") or [] if isinstance(v, dict)]
    paquet = paquets.paquet_vocabulaire(langue, titre, str(data.get("description", "")).strip(), types, fiches,
                                        f"Claude ({t.modele})")
    if not paquet["vocabulaire"]:
        raise Echec("Claude n'a renvoyé aucun mot utilisable : vérifiez la liste et relancez.")
    return paquet, dossier, None, _usage(message)


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


def _generer_fiche(t):
    """(texte de la fiche, avertissement ou None, usage)."""
    fichier = get_vault().root / t.source
    if not fichier.is_file():
        raise Echec("La page n'est plus dans le wiki.")
    nom = (t.options or {}).get("nom") or PurePosixPath(t.source).stem
    client = _client_pret()
    message = _appeler(client, _demande(t, CONSIGNE_FICHE, [
        {"type": "text", "text": f"Page « {nom} » :\n\n{fichier.read_text(encoding='utf-8')}"},
        {"type": "text", "text": "Rédige la fiche de révision de cette page."},
    ], max_tokens=MAX_TOKENS_GENERATION))
    texte = _sans_cadre(_texte_reponse(message))
    if not texte:
        raise Echec("Claude n'a renvoyé aucun texte.")
    cle = (t.options or {}).get("cle") or PurePosixPath(t.source).with_suffix("").as_posix()
    texte = f"> [!abstract] Fiche de révision de [[{cle}|{nom}]]\n\n{texte}"
    avertissement = "Fiche trop longue : la fin manque." if message.stop_reason == "max_tokens" else None
    return texte, avertissement, _usage(message)


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

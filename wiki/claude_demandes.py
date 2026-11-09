"""Appels à Claude à la demande, courts et synchrones (réponse dans la requête) : explication
d'une réponse, correction d'une question signalée, réponse rédigée jugée, tuteur d'une page,
« Demander au wiki », copie photographiée, « Améliorer » de l'éditeur. Le client, les requêtes
et le plafond mensuel sont dans claude.py."""


from . import claude
from .vault import get_vault

# -- « Explique-moi » (question de QCM) et « Améliorer la rédaction » (éditeur) --------------------
MODELE_EXPLICATIONS = "claude-haiku-5-5"  # explications courtes : le modèle le moins cher suffit
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
    client = claude._client_pret()
    vault = get_vault()
    note = vault.notes.get(qset.source_page.lower()) if qset.source_page else None
    contexte = ""
    if note is not None:
        contexte = (vault.root / note.path).read_text(encoding="utf-8")[:claude.MAX_CHARS_COURS]
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
    message = claude._appeler(client, claude._demande(MODELE_EXPLICATIONS, CONSIGNE_EXPLICATION, contenu, max_tokens=1500, effort="low"))
    texte = claude._texte_reponse(message)
    if not texte:
        raise claude.Echec("Claude n'a renvoyé aucune explication.")
    return texte, claude._usage(message), MODELE_EXPLICATIONS


def ameliorer(texte):
    """Texte Markdown relu et corrigé par Claude (modèle réglé). Renvoie (texte, usage)."""
    if len(texte) > MAX_CHARS_AMELIORER:
        raise claude.Echec(f"Sélectionnez un passage plus court ({MAX_CHARS_AMELIORER} caractères au plus).")
    client = claude._client_pret()
    message = claude._appeler(client, claude._demande(claude.modele(), CONSIGNE_AMELIORER, [{"type": "text", "text": texte}],
                                        max_tokens=16000, effort="low"))
    resultat = claude._sans_cadre(claude._texte_reponse(message))
    if not resultat:
        raise claude.Echec("Claude n'a renvoyé aucun texte.")
    if message.stop_reason == "max_tokens":
        raise claude.Echec("Passage trop long pour une seule relecture : sélectionnez-en une partie.")
    return resultat, claude._usage(message)


# ---------------------------------------------------------------------------
# Correction d'une question signalée
# ---------------------------------------------------------------------------
CONSIGNE_CORRECTION = """Tu corriges une question de révision (QCM) qu'un étudiant a signalée : erreur, ambiguïté, \
coquille ou réponse discutable. Appuie-toi sur le cours fourni quand il y en a un. Renvoie la question corrigée \
complète, du même type si possible, avec une bonne réponse sans ambiguïté et une explication courte ; et dans \
« modification », en une ou deux phrases, ce que tu as changé et pourquoi. Si le signalement est infondé, renvoie \
la question inchangée et explique en quoi elle est juste. Les formules s'écrivent en LaTeX entre $."""


SCHEMA_CORRECTION = {
    "type": "object",
    "properties": {**claude._QUESTION_SCHEMA["properties"], "modification": {"type": "string"}},
    "required": [*claude._QUESTION_SCHEMA["required"], "modification"],
    "additionalProperties": False,
}


def corriger_question(qset, question, commentaires):
    """Correction d'une question signalée, proposée par Claude d'après le cours quand le
    set en vient. Renvoie (question JSON corrigée, note de modification, usage, modèle) ;
    la question est validée comme à l'import d'un set."""
    import json as json_module

    from . import quiz

    client = claude._client_pret()
    vault = get_vault()
    note = vault.notes.get(qset.source_page.lower()) if qset.source_page else None
    contenu = []
    if note is not None:
        contexte = (vault.root / note.path).read_text(encoding="utf-8")[:claude.MAX_CHARS_COURS]
        contenu.append({"type": "text", "text": f"Cours « {note.title} » :\n\n{contexte}"})
    texte = f"Question signalée (set « {qset.titre} ») :\n{json_module.dumps(claude.question_en_json(question), ensure_ascii=False, indent=1)}"
    texte += "\n\nSignalement(s) :\n" + "\n".join(f"- {c}" for c in commentaires if c) if any(commentaires) else "\n\nAucun commentaire : vérifie la question."
    if note is None:
        texte += "\n\nAucun cours fourni."
    contenu.append({"type": "text", "text": texte})
    message = claude._appeler(client, claude._demande(claude.modele(), CONSIGNE_CORRECTION, contenu, schema=SCHEMA_CORRECTION,
                                        max_tokens=4000, effort="medium"))
    try:
        data = json_module.loads(claude._texte_reponse(message))
    except ValueError as e:
        raise claude.Echec(f"Réponse de Claude illisible : {e}") from e
    modification = str(data.pop("modification", "")).strip()
    nouvelle = {k: v for k, v in data.items() if k in claude.CHAMPS_QUESTION and v not in ("", [], None)}
    try:
        quiz.question_depuis_json({**nouvelle, "id": question.id}, 0, "correction")
    except ValueError as e:
        raise claude.Echec(f"Correction invalide : {e}") from e
    return nouvelle, modification, claude._usage(message), claude.modele()


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
    client = claude._client_pret()
    lignes = [f"Question : {question.enonce}"]
    if question.consigne:
        lignes.append(f"Consigne : {question.consigne}")
    lignes.append("Réponse(s) attendue(s) : " + " / ".join(question.reponses_texte))
    if question.explication:
        lignes.append(f"Explication du corrigé : {question.explication}")
    lignes.append(f"Réponse de l'étudiant : {reponse[:MAX_CHARS_REPONSE]}")
    message = claude._appeler(client, claude._demande(MODELE_EXPLICATIONS, CONSIGNE_QRC, [{"type": "text", "text": "\n".join(lignes)}],
                                        schema=SCHEMA_QRC, max_tokens=MAX_TOKENS_QRC, effort="low"))
    data = claude._json_reponse(message, "Réponse de Claude trop longue.")
    verdict = data.get("verdict") if data.get("verdict") in ("juste", "partiel", "faux") else "faux"
    return verdict, str(data.get("retour", "")).strip(), claude._usage(message), MODELE_EXPLICATIONS


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
    client = claude._client_pret()
    vault = get_vault()
    page = (vault.root / note.path).read_text(encoding="utf-8")[:claude.MAX_CHARS_COURS]
    systeme = f"{CONSIGNE_TUTEUR}\n\nPage « {note.title} » :\n\n{page}"
    message = claude._appeler(client, claude._demande(MODELE_EXPLICATIONS, systeme, question[:MAX_CHARS_QUESTION],
                                        max_tokens=MAX_TOKENS_TUTEUR, effort="low", historique=historique))
    texte = claude._texte_reponse(message)
    if not texte:
        raise claude.Echec("Claude n'a renvoyé aucune réponse.")
    return texte, claude._usage(message), MODELE_EXPLICATIONS


CONSIGNE_WIKI = """Tu réponds à un étudiant à partir de son wiki de cours : des extraits numérotés de ses pages et \
de ses PDF te sont fournis. Réponds en français, en 3 à 12 phrases, en Markdown léger (gras pour les mots clés, listes \
courtes, formules en LaTeX entre $). Appuie-toi d'abord sur les extraits et cite-les par leur numéro entre crochets, \
par exemple [2] ou [1, 3], juste après l'idée qu'ils appuient. Si les extraits ne contiennent pas la réponse, dis-le \
clairement (« Le wiki n'en parle pas »), puis réponds avec prudence d'après tes connaissances, sans citation. \
N'invente jamais de numéro de source."""


def demander_wiki(question, sources, historique=()):
    """Réponse (Haiku) à une question sur tout le wiki, d'après les extraits numérotés :
    (texte Markdown, usage, modèle)."""
    client = claude._client_pret()
    extraits = "\n\n".join(f"[{i}] {s['titre']}\n{s['texte']}" for i, s in enumerate(sources, 1))
    systeme = f"{CONSIGNE_WIKI}\n\nExtraits du wiki :\n\n{extraits or '(aucun extrait ne correspond à la question)'}"
    message = claude._appeler(client, claude._demande(MODELE_EXPLICATIONS, systeme, question[:MAX_CHARS_QUESTION],
                                        max_tokens=MAX_TOKENS_TUTEUR, effort="low", historique=historique))
    texte = claude._texte_reponse(message)
    if not texte:
        raise claude.Echec("Claude n'a renvoyé aucune réponse.")
    return texte, claude._usage(message), MODELE_EXPLICATIONS


MODELE_COPIE = "claude-sonnet-5-5"  # lecture d'écriture manuscrite et raisonnement : bon rapport qualité-prix
MAX_TOKENS_COPIE = 6000
CONSIGNE_COPIE = """Tu corriges la copie manuscrite d'un étudiant, photographiée (images jointes, dans l'ordre des \
pages). Réponds en français, en Markdown (titres ###, listes, formules en LaTeX entre $), en suivant ce plan :

### Ce que tu as écrit
La démarche de l'étudiant, transcrite brièvement étape par étape (numérotées).

### Correction pas à pas
Pour chaque étape : ✅ juste, ⚠️ imprécis ou incomplet, ❌ faux ; une phrase d'explication et, si c'est faux, \
la correction (le bon calcul ou le bon raisonnement).

### Bilan
Ce qui est acquis, l'erreur principale à retenir, et une note indicative sur 20 si l'exercice s'y prête.

Appuie-toi sur l'énoncé et sur le cours fournis s'il y en a. Si une partie est illisible, dis-le au lieu de \
deviner. Si les images ne montrent pas une copie (photo floue, autre chose), dis-le simplement. Sois exigeant \
mais bienveillant."""


def corriger_copie(images, enonce="", cours="", titre_cours=""):
    """Correction (Sonnet) d'une copie manuscrite : ``images`` = JPEG (octets), dans
    l'ordre des pages. Renvoie (texte Markdown, usage, modèle)."""
    import base64

    client = claude._client_pret()
    systeme = CONSIGNE_COPIE
    if cours:
        systeme += f"\n\nCours de référence « {titre_cours} » :\n\n{cours[:claude.MAX_CHARS_COURS // 2]}"
    contenu = [{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                            "data": base64.b64encode(image).decode("ascii")}} for image in images]
    contenu.append({"type": "text", "text": f"Énoncé de l'exercice :\n{enonce[:MAX_CHARS_QUESTION * 2]}" if enonce.strip()
                    else "Pas d'énoncé fourni : déduis-le de la copie si possible."})
    message = claude._appeler(client, claude._demande(MODELE_COPIE, systeme, contenu, max_tokens=MAX_TOKENS_COPIE, effort="medium"))
    texte = claude._texte_reponse(message)
    if not texte:
        raise claude.Echec("Claude n'a renvoyé aucune correction.")
    return texte, claude._usage(message), MODELE_COPIE

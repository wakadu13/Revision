"""Explorer le wiki : « Demander au wiki » (Claude répond d'après les pages et les PDF,
en citant ses sources) et le graphe des liens entre pages."""

import json

from django.http import JsonResponse
from django.views.decorators.cache import never_cache

from . import claude, demander as recherche_sources
from .models import EchangeTuteur, UsageClaude
from .vault import get_vault
from .views import _render

HISTORIQUE_AFFICHE = 10
HISTORIQUE_REJOUE = 3


def _echange_html(vault, echange):
    from .quiz_views import _render_html

    html, cites = recherche_sources.lier_citations(_render_html(vault, echange.reponse), echange.sources)
    return {"question": echange.question, "html": html, "quand": echange.cree_le,
            "sources": [{**s, "n": i, "cite": i in cites} for i, s in enumerate(echange.sources, 1)]}


@never_cache
def demander(request):
    """Page « Demander au wiki » (GET) ; question posée à Claude (POST JSON {question})."""
    from .quiz_views import player_id

    vault = get_vault()
    player = player_id(request)
    echanges = EchangeTuteur.objects.filter(player=player, page=EchangeTuteur.PAGE_WIKI)
    if request.method != "POST":
        recents = list(echanges)[-HISTORIQUE_AFFICHE:]
        return _render(request, vault, "wiki/demander.html", {
            "dispo": claude.disponible(), "plafond": claude.plafond_atteint(), "question": request.GET.get("q", "")[:500],
            "echanges": [_echange_html(vault, e) for e in reversed(recents)],
        })
    try:
        question = str(json.loads(request.body)["question"]).strip()
    except (KeyError, ValueError, TypeError):
        return JsonResponse({"error": "requête invalide"}, status=400)
    if not question:
        return JsonResponse({"error": "Question vide."}, status=400)
    if not claude.disponible():
        return JsonResponse({"error": "Pas de clé d'API Claude sur le serveur."}, status=503)
    if claude.plafond_atteint():
        return JsonResponse({"error": "Plafond mensuel de Claude atteint : réessayez le mois prochain."}, status=429)
    precedents = list(echanges)[-HISTORIQUE_REJOUE:]
    # Les questions précédentes aident à retrouver les pages d'une question de suite (« et pourquoi ? »).
    sources = recherche_sources.rassembler(vault, question, [e.question for e in precedents[-1:]])
    try:
        texte, usage, modele_id = claude.demander_wiki(question, sources, [(e.question, e.reponse) for e in precedents])
    except claude.Echec as e:
        return JsonResponse({"error": str(e)}, status=502)
    echange = EchangeTuteur.objects.create(
        player=player, page=EchangeTuteur.PAGE_WIKI, question=question[:claude.MAX_CHARS_QUESTION], reponse=texte,
        sources=[{k: s[k] for k in ("titre", "url", "type")} for s in sources],
        modele=modele_id, jetons_entree=usage[0], jetons_sortie=usage[1])
    claude.noter_usage(UsageClaude.WIKI, player, modele_id, usage)
    rendu = _echange_html(vault, echange)
    return JsonResponse({"html": rendu["html"], "sources": rendu["sources"], "modele": modele_id})


def graphe(request):
    """Graphe des liens entre pages (``?page=<clé>`` : centré sur une page et ses voisines)."""
    vault = get_vault()
    centre = vault.notes.get(request.GET.get("page", "").lower())
    return _render(request, vault, "wiki/graphe.html", {"centre": centre})


def graphe_donnees(request):
    """Pages (titre, adresse, dossier) et liens entre elles, pour graphe.js."""
    vault = get_vault()
    notes = vault.sorted_notes()
    index = {n.key.lower(): i for i, n in enumerate(notes)}
    liens = set()
    for cle, sources in vault.backlinks.items():
        j = index.get(cle)
        if j is None:
            continue
        for source in sources:
            i = index[source.key.lower()]
            liens.add((min(i, j), max(i, j)))
    noeuds = [{"t": n.title, "u": n.url, "k": n.key, "d": n.folders[0] if n.folders else ""} for n in notes]
    return JsonResponse({"noeuds": noeuds, "liens": sorted(liens)})

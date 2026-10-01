"""Planning des révisions d'un set : quotas journaliers et estimation de la durée.

Deux quotas par jour, comme dans Anki : les nouvelles questions (jamais vues) et
les révisions (questions déjà vues, revenues à échéance).

L'estimation simule la révision espacée (Leitner) jour après jour : chaque jour,
les questions dues sont révisées dans la limite des quotas, avec un taux de bonnes
réponses égal à la précision du joueur sur ce set. Une question est « sue »
dès qu'elle a atteint la boîte BOITE_OBJECTIF, même si elle retombe ensuite
(une erreur renvoie en boîte 0 : compter les questions actuellement en boîte
haute ne convergerait pas toujours). Le set est prêt quand une part
PART_OBJECTIF des questions est sue (viser 100 % ferait dépendre l'estimation
de la question la plus malchanceuse).

Comme quiz.py, ce module ne dépend ni des modèles ni des vues.
"""

import math
import random
from datetime import timedelta

from django.utils import timezone

from . import quiz

BOITE_OBJECTIF = 3          # réussie 3 fois (intervalle de 7 jours) : considérée comme sue
PART_OBJECTIF = 0.95        # part des questions sues pour considérer le set prêt
PRECISION_DEFAUT = 0.8      # tant qu'il y a trop peu de réponses pour la mesurer
PRECISION_MIN, PRECISION_MAX = 0.6, 0.97
REPONSES_MIN_PRECISION = 20
SECONDES_DEFAUT = 20        # temps par question tant qu'il n'est pas mesuré
REPONSES_MIN_CHRONO = 10
HORIZON_JOURS = 365


def faites_aujourdhui(progress, now):
    """(nouvelles, révisions) déjà faites aujourd'hui sur ce set (heure locale).

    Une question découverte aujourd'hui compte comme nouvelle, même si elle a
    été revue ensuite dans la journée.
    """
    jour = timezone.localdate(now)
    nouvelles = revisions = 0
    for st in progress.values():
        if st.premiere_revue and timezone.localdate(st.premiere_revue) == jour:
            nouvelles += 1
        elif st.last_review and timezone.localdate(st.last_review) == jour:
            revisions += 1
    return nouvelles, revisions


def restant(limite, deja):
    """Places restantes aujourd'hui pour un quota (None : pas de limite)."""
    return None if limite is None else max(0, limite - deja)


def simuler(cartes, quota_nouvelles, quota_revisions, precision, deja=(0, 0)):
    """Simule les révisions. `cartes` : liste de (boîte, jour où elle est due, jamais vue).

    Les quotas sont des nombres par jour ; `deja` = (nouvelles, révisions) déjà
    faites aujourd'hui. Renvoie (jours nécessaires, nombre de réponses), ou None
    au-delà de HORIZON_JOURS.
    """
    boites = [b for b, _, _ in cartes]
    dues = [d for _, d, _ in cartes]
    nouvelles = [i for i, (_, _, n) in enumerate(cartes) if n]
    vues = [i for i, (_, _, n) in enumerate(cartes) if not n]
    sues = {i for i, b in enumerate(boites) if b >= BOITE_OBJECTIF}
    restantes = math.ceil(PART_OBJECTIF * len(boites)) - len(sues)
    if restantes <= 0:
        return 0, 0
    hasard = random.Random(0)  # graine fixe : même estimation à chaque affichage
    reponses = 0
    for jour in range(HORIZON_JOURS):
        places_n = max(0, quota_nouvelles - (deja[0] if jour == 0 else 0))
        places_r = max(0, quota_revisions - (deja[1] if jour == 0 else 0))
        # Même ordre que la file du jour : révisions (boîtes basses d'abord), puis nouvelles.
        a_revoir = sorted((i for i in vues if dues[i] <= jour), key=lambda i: (boites[i], dues[i]))[:places_r]
        decouvertes, nouvelles = nouvelles[:places_n], nouvelles[places_n:]
        for i in a_revoir + decouvertes:
            reponses += 1
            boites[i] = quiz.nouvelle_boite(boites[i], hasard.random() < precision)
            dues[i] = jour + max(1, quiz.INTERVALLES_JOURS[boites[i]])
            if boites[i] >= BOITE_OBJECTIF and i not in sues:
                sues.add(i)
                restantes -= 1
        vues += decouvertes
        if restantes <= 0:
            return jour + 1, reponses
    return None


def _cartes(qset, progress, now):
    aujourdhui = timezone.localdate(now)
    cartes = []
    for q in qset.questions:
        st = progress.get(q.id)
        if st is None:
            cartes.append((0, 0, True))
        elif st.is_due(now):
            cartes.append((st.box, 0, False))
        else:
            echeance = timezone.localdate(st.last_review + timedelta(days=quiz.INTERVALLES_JOURS[st.box]))
            cartes.append((st.box, max(1, (echeance - aujourdhui).days), False))
    return cartes


def precision(progress):
    reponses = sum(st.seen for st in progress.values())
    if reponses < REPONSES_MIN_PRECISION:
        return PRECISION_DEFAUT, False
    p = sum(st.correct for st in progress.values()) / reponses
    return min(PRECISION_MAX, max(PRECISION_MIN, p)), True


def estimer(qset, progress, deck, now):
    """Durée estimée pour tout savoir, et date à laquelle commencer pour l'examen."""
    aujourdhui = timezone.localdate(now)
    cartes = _cartes(qset, progress, now)
    total = len(cartes)
    p, p_mesuree = precision(progress)
    secondes, s_mesure = deck.secondes_par_carte(SECONDES_DEFAUT, REPONSES_MIN_CHRONO)
    deja = faites_aujourdhui(progress, now)

    def duree(nouvelles, revisions):
        return simuler(cartes, nouvelles, revisions, p, deja)

    def par_jour(resultat):
        jours, reponses = resultat
        return round(reponses / jours) if jours else 0

    def minutes(resultat):
        jours, reponses = resultat
        return round(reponses / jours * secondes / 60) if jours else 0

    # Sans limite, toutes les questions peuvent passer le même jour.
    res = duree(deck.nouvelles_jour or total, deck.revisions_jour or total)
    e = {
        "nouvelles_jour": deck.nouvelles_jour,
        "revisions_jour": deck.revisions_jour,
        "precision": round(p * 100),
        "precision_mesuree": p_mesuree,
        "secondes": round(secondes),
        "secondes_mesurees": s_mesure,
        "boite_objectif": BOITE_OBJECTIF,
        "part_objectif": round(PART_OBJECTIF * 100),
        "su": res == (0, 0),
        "jours": res[0] if res else None,
        "fin": aujourdhui + timedelta(days=res[0] - 1) if res and res[0] else None,
        "questions_jour": par_jour(res) if res else None,
        "minutes_jour": minutes(res) if res else None,
        "objectif": deck.date_objectif,
    }
    if not deck.date_objectif or e["su"]:
        return e

    # Jours de révision disponibles : d'aujourd'hui à la veille de l'examen.
    dispo = (deck.date_objectif - aujourdhui).days
    e["jours_dispo"] = dispo
    if dispo <= 0:
        e["statut"] = "passee"
    elif res and res[0] <= dispo:
        debut = deck.date_objectif - timedelta(days=res[0])
        e["statut"] = "ok"
        e["debut"] = debut
        e["commencer_maintenant"] = debut <= aujourdhui
        e["marge"] = dispo - res[0]
    else:
        # Conseil à la Anki : ne pas plafonner les révisions, et chercher le plus
        # petit nombre de nouvelles questions par jour qui suffit (dichotomie).
        meilleur = duree(total, total)
        if not meilleur or meilleur[0] > dispo:
            e["statut"] = "impossible"
            e["jours_min"] = meilleur[0] if meilleur else None
            return e
        bas, haut = 1, total
        while bas < haut:
            milieu = (bas + haut) // 2
            r = duree(milieu, total)
            if r and r[0] <= dispo:
                haut, meilleur = milieu, r
            else:
                bas = milieu + 1
        e["statut"] = "retard"
        e["nouvelles_conseillees"] = haut
        e["questions_conseillees"] = par_jour(meilleur)
        e["minutes_conseillees"] = minutes(meilleur)
        e["revisions_limitees"] = bool(deck.revisions_jour)
    return e

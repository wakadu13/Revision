"""Planning des révisions d'un set : quota journalier et estimation de la durée.

L'estimation simule la révision espacée (Leitner) jour après jour : chaque jour,
les questions dues sont révisées dans la limite du quota, avec un taux de bonnes
réponses égal à la précision du joueur sur ce set. Une question est « sue »
lorsqu'elle atteint la boîte BOITE_OBJECTIF ; le set est prêt quand une part
PART_OBJECTIF des questions l'est (viser 100 % ferait dépendre l'estimation de
la question la plus malchanceuse).

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
SECONDES_DEFAUT = 20        # temps par carte tant qu'il n'est pas mesuré
REPONSES_MIN_CHRONO = 10
HORIZON_JOURS = 365


def revues_aujourdhui(progress, now):
    """Nombre de questions du set déjà révisées aujourd'hui (heure locale)."""
    jour = timezone.localdate(now)
    return sum(1 for st in progress.values() if st.last_review and timezone.localdate(st.last_review) == jour)


def simuler(cartes, limite, precision, quota_jour0):
    """Simule les révisions. `cartes` : liste de (boîte, jour où elle est due, jamais vue).

    Renvoie (jours nécessaires, nombre de révisions), ou None au-delà de HORIZON_JOURS.
    """
    boites = [b for b, _, _ in cartes]
    dues = [d for _, d, _ in cartes]
    nouvelles = [n for _, _, n in cartes]
    restantes = math.ceil(PART_OBJECTIF * len(boites)) - sum(b >= BOITE_OBJECTIF for b in boites)
    if restantes <= 0:
        return 0, 0
    hasard = random.Random(0)  # graine fixe : même estimation à chaque affichage
    revisions = 0
    for jour in range(HORIZON_JOURS):
        capacite = quota_jour0 if jour == 0 else limite
        candidates = [i for i in range(len(boites)) if dues[i] <= jour]
        # Même ordre que la file du jour : déjà vues (boîtes basses d'abord), puis nouvelles.
        candidates.sort(key=lambda i: (nouvelles[i], boites[i], dues[i]))
        for i in candidates[:capacite]:
            revisions += 1
            correcte = hasard.random() < precision
            avant = boites[i] >= BOITE_OBJECTIF
            boites[i] = quiz.nouvelle_boite(boites[i], correcte)
            dues[i] = jour + max(1, quiz.INTERVALLES_JOURS[boites[i]])
            nouvelles[i] = False
            restantes += avant - (boites[i] >= BOITE_OBJECTIF)
        if restantes <= 0:
            return jour + 1, revisions
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
    deja = revues_aujourdhui(progress, now)

    def duree(limite):
        return simuler(cartes, limite, p, max(0, limite - deja))

    def minutes(resultat):
        jours, revisions = resultat
        return round(revisions / jours * secondes / 60) if jours else 0

    limite = deck.limite_jour or total
    res = duree(limite)
    e = {
        "limite": limite,
        "sans_limite": not deck.limite_jour,
        "precision": round(p * 100),
        "precision_mesuree": p_mesuree,
        "secondes": round(secondes),
        "secondes_mesurees": s_mesure,
        "boite_objectif": BOITE_OBJECTIF,
        "part_objectif": round(PART_OBJECTIF * 100),
        "su": res == (0, 0),
        "jours": res[0] if res else None,
        "fin": aujourdhui + timedelta(days=res[0] - 1) if res and res[0] else None,
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
        # Plus petite limite journalière qui suffit (recherche dichotomique).
        bas, haut = limite + 1, max(total, limite + 1)
        meilleur = duree(haut)
        if not meilleur or meilleur[0] > dispo:
            e["statut"] = "impossible"
            e["jours_min"] = meilleur[0] if meilleur else None
            return e
        while bas < haut:
            milieu = (bas + haut) // 2
            r = duree(milieu)
            if r and r[0] <= dispo:
                haut, meilleur = milieu, r
            else:
                bas = milieu + 1
        e["statut"] = "retard"
        e["limite_conseillee"] = haut
        e["minutes_conseillees"] = minutes(meilleur)
    return e

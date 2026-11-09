"""Envoie les rappels quotidiens par notification web (Web Push).

À lancer régulièrement, par exemple toutes les 15 minutes par cron sur le serveur :

    */15 * * * * cd /home/pi/deploy && docker compose exec -T web python manage.py envoyer_rappels

Chaque appareil abonné reçoit au plus un rappel par jour, à partir de l'heure
choisie ; rien si tout est déjà révisé et qu'on a travaillé aujourd'hui.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone

from wiki import push, quiz
from wiki.models import AbonnementPush
from wiki.quiz_views import etat_rappel, texte_rappel


class Command(BaseCommand):
    help = "Envoie les rappels quotidiens par notification web."

    def handle(self, *args, **options):
        maintenant = timezone.localtime()
        jour = maintenant.date()
        library = quiz.get_library()
        envoyes = expires = rien = erreurs = 0
        etats = {}
        for a in AbonnementPush.objects.select_related("user").filter(user__is_active=True):
            if a.dernier_envoi == jour or (a.heure, a.minute) > (maintenant.hour, maintenant.minute):
                continue
            player = a.user.get_username()
            if player not in etats:
                etats[player] = etat_rappel(player, library, timezone.now())
            texte = texte_rappel(etats[player])
            if texte is None:
                rien += 1
            else:
                try:
                    push.envoyer(a, "ProjetPluri", texte)
                    envoyes += 1
                except push.AbonnementExpire:
                    a.delete()
                    expires += 1
                    continue
                except Exception as e:  # noqa: BLE001
                    erreurs += 1
                    self.stderr.write(f"{a} : {e}")
                    continue
            AbonnementPush.objects.filter(pk=a.pk).update(dernier_envoi=jour)
        self.stdout.write(f"{envoyes} envoyé(s), {rien} sans objet, {expires} abonnement(s) expiré(s), {erreurs} erreur(s)")

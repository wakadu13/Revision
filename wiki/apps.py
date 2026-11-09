from django.apps import AppConfig


class WikiConfig(AppConfig):
    name = 'wiki'
    verbose_name = 'Wiki'

    def ready(self):
        from django.core.signals import got_request_exception

        from .erreurs import au_signal

        # Erreurs 500 gardées pour la page « Erreurs du serveur » des admins.
        got_request_exception.connect(au_signal, dispatch_uid="wiki-erreurs-serveur")

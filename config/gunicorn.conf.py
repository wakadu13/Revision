"""Serveur de production : gunicorn.

    gunicorn -c config/gunicorn.conf.py config.wsgi

Un seul processus, plusieurs fils : la file des travaux de Claude, la surveillance
des lots et les caches du coffre vivent dans le processus. Avec plusieurs
processus, un travail de Claude interrompu pourrait être repris deux fois.
"""

import os

bind = os.environ.get("GUNICORN_BIND", "0.0.0.0:8000")
workers = 1
worker_class = "gthread"
threads = int(os.environ.get("GUNICORN_THREADS", "4"))
# Les appels à Claude faits pendant une requête (« Améliorer », correction d'une
# question signalée) peuvent durer plus d'une minute.
timeout = 180
graceful_timeout = 30
# Journaux sur la sortie standard : « docker compose logs web ».
accesslog = "-"
errorlog = "-"
loglevel = "info"

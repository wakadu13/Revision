"""Réglages du wiki pour le scénario de bout en bout (e2e/scenario.js) : le coffre
de test et une base de données à part. Lancer avec PYTHONPATH=e2e et
DJANGO_SETTINGS_MODULE=settings_e2e ; voir .github/workflows/tests.yml."""

import os
from pathlib import Path

from config.settings import *  # noqa: F401,F403

WIKI_DIR = Path(os.environ["E2E_VAULT"])
WIKI_HOME = "Accueil"

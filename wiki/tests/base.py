"""Bases et faux objets communs aux tests du wiki : coffre temporaire, set de QCM de test,
faux client de l'API Claude, PDF fabriqué avec du texte."""

import tempfile
from pathlib import Path

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from wiki.vault import get_vault


class WikiTestCase(TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        override = override_settings(WIKI_DIR=self.root, WIKI_HOME="Accueil", SECURE_SSL_REDIRECT=False)
        override.enable()
        self.addCleanup(override.disable)
        # Site privé : les tests du wiki se font avec un compte utilisateur.
        self.reader = get_user_model().objects.create_user("lecteur", password="x")
        self.client.force_login(self.reader)

    def write(self, path, text):
        file = self.root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding="utf-8")

    def html(self, key):
        vault = get_vault()
        return vault.render(vault.notes[key.lower()])[0]


class QuizBase(TestCase):
    """Coffre de test avec un set de QCM (reseaux/test_set) et le compte « alice » connecté."""

    def setUp(self):
        import json
        import tempfile
        from pathlib import Path
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        override = override_settings(WIKI_DIR=self.root, WIKI_HOME="Accueil", SECURE_SSL_REDIRECT=False)
        override.enable()
        self.addCleanup(override.disable)
        self.set = {
            "titre": "Set de test",
            "questions": [
                {"id": "q-qcm", "type": "QCM", "question": "2+2 ?", "choix": ["3", "4"], "reponses": [1]},
                {"id": "q-qcr", "type": "QCR", "question": "Pairs ?", "choix": ["2", "3", "4"], "reponses": [0, 2]},
                {"id": "q-trou", "type": "TROU", "question": "Capitale de la France ?", "reponses_texte": ["Paris"]},
                {"id": "q-flash", "type": "FLASHCARD", "question": "chat", "verso": "cat"},
            ],
        }
        (self.root / "reseaux").mkdir(parents=True)
        (self.root / "reseaux" / "test_set.json").write_text(json.dumps(self.set), encoding="utf-8")
        self.user = get_user_model().objects.create_user("alice", password="x")
        self.client.force_login(self.user)


class _FauxFlux:
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def get_final_message(self):
        return self.message


class _FauxClaude:
    """Remplace le client Anthropic : aucune requête réseau, aucun coût."""

    def __init__(self, texte="---\ntags: [cours]\n---\n# Cours\n\nUne **notion** : $x^2$.", stop="end_turn", erreur=None):
        from types import SimpleNamespace

        self.demandes, self.envois, self.suppressions = [], [], []
        faux = self

        class Messages:
            def stream(self, **demande):
                faux.demandes.append(demande)
                if erreur is not None:
                    raise erreur
                contenu = [SimpleNamespace(type="thinking", thinking=""), SimpleNamespace(type="text", text=texte)]
                usage = SimpleNamespace(input_tokens=1000, output_tokens=500)
                return _FauxFlux(SimpleNamespace(content=contenu, stop_reason=stop, usage=usage))

        def upload(file):
            faux.envois.append(file)
            return SimpleNamespace(id="file_1")

        self.beta = SimpleNamespace(messages=Messages())
        self.files = SimpleNamespace(upload=upload, delete=faux.suppressions.append)


class _FauxLots:
    """Faux « client.beta.messages.batches » : un lot créé, puis terminé quand on le décide."""

    def __init__(self, texte, statut="in_progress", type_resultat="succeeded"):
        from types import SimpleNamespace
        self.SimpleNamespace = SimpleNamespace
        self.texte, self.statut, self.type_resultat = texte, statut, type_resultat
        self.creations = []

    def create(self, requests, **extra):
        self.creations.append({"requests": requests, **extra})
        return self.SimpleNamespace(id="msgbatch_1")

    def retrieve(self, lot_id):
        return self.SimpleNamespace(id=lot_id, processing_status=self.statut)

    def results(self, lot_id):
        S = self.SimpleNamespace
        for demande in self.creations[0]["requests"]:
            if self.type_resultat == "succeeded":
                message = S(content=[S(type="text", text=self.texte)], stop_reason="end_turn",
                            usage=S(input_tokens=2000, output_tokens=800))
                yield S(custom_id=demande["custom_id"], result=S(type="succeeded", message=message))
            else:
                yield S(custom_id=demande["custom_id"], result=S(type="errored", error=S(message="Quota dépassé")))


def _pdf_texte(*pages):
    """PDF minimal (Helvetica) : une page par texte, une ligne par « \\n »."""
    objets = [b"<< /Type /Catalog /Pages 2 0 R >>",
              f"<< /Type /Pages /Kids [{' '.join(f'{4 + 2 * i} 0 R' for i in range(len(pages)))}] /Count {len(pages)} >>".encode(),
              b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"]
    for i, texte in enumerate(pages):
        lignes = " ".join(f"({ligne}) Tj 0 -16 Td" for ligne in texte.split("\n"))
        flux = f"BT /F1 12 Tf 72 720 Td {lignes} ET".encode("cp1252")
        objets.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 3 0 R >> >> /Contents {5 + 2 * i} 0 R >>".encode())
        objets.append(b"<< /Length %d >>\nstream\n" % len(flux) + flux + b"\nendstream")
    sortie, positions = bytearray(b"%PDF-1.4\n"), []
    for i, objet in enumerate(objets, 1):
        positions.append(len(sortie))
        sortie += f"{i} 0 obj\n".encode() + objet + b"\nendobj\n"
    xref = len(sortie)
    sortie += f"xref\n0 {len(objets) + 1}\n0000000000 65535 f \n".encode() + b"".join(f"{p:010d} 00000 n \n".encode() for p in positions)
    sortie += f"trailer\n<< /Size {len(objets) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return bytes(sortie)

package fr.projetpluri.qcm;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.net.Uri;
import android.webkit.CookieManager;
import android.widget.Toast;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Téléchargements : « Enregistrer sous » d'Android (Storage Access Framework),
 * sans permission de stockage, puis écriture en arrière-plan. Les fichiers du
 * serveur sont lus avec les cookies de la session du wiki.
 */
class Fichiers {
    interface Source {
        void ecrire(OutputStream sortie) throws IOException;
    }

    private final Activity activite;
    private final ExecutorService fond = Executors.newSingleThreadExecutor();
    private Source enAttente;
    private String nomEnAttente;

    Fichiers(Activity activite) {
        this.activite = activite;
    }

    void arreter() {
        fond.shutdownNow();
    }

    /** Demande où enregistrer ``nom``, puis y écrit ``source``. */
    void enregistrerSous(String nom, String type, Source source) {
        enAttente = source;
        nomEnAttente = nom;
        Intent intention = new Intent(Intent.ACTION_CREATE_DOCUMENT)
                .addCategory(Intent.CATEGORY_OPENABLE)
                .setType(type == null || type.isEmpty() ? "application/octet-stream" : type)
                .putExtra(Intent.EXTRA_TITLE, nom);
        try {
            activite.startActivityForResult(intention, MainActivity.ENREGISTRER);
        } catch (ActivityNotFoundException e) {
            enAttente = null;
            Toast.makeText(activite, "Aucune application pour enregistrer le fichier.", Toast.LENGTH_LONG).show();
        }
    }

    void resultat(int code, Intent donnees) {
        Source source = enAttente;
        String nom = nomEnAttente;
        enAttente = null;
        if (source == null || code != Activity.RESULT_OK || donnees == null || donnees.getData() == null) return;
        Uri cible = donnees.getData();
        fond.execute(() -> {
            String message;
            try (OutputStream sortie = activite.getContentResolver().openOutputStream(cible)) {
                if (sortie == null) throw new IOException("emplacement inaccessible");
                source.ecrire(sortie);
                message = "Fichier enregistré : " + nom;
            } catch (Exception e) {
                message = "Échec de l'enregistrement : " + (e.getMessage() == null ? e.getClass().getSimpleName() : e.getMessage());
            }
            String texte = message;
            activite.runOnUiThread(() -> Toast.makeText(activite, texte, Toast.LENGTH_LONG).show());
        });
    }

    /** Contenu d'une adresse du serveur, lu avec les cookies de la session. */
    Source depuis(String adresse, String agent) {
        return sortie -> {
            HttpURLConnection cnx = (HttpURLConnection) new URL(adresse).openConnection();
            try {
                String cookies = CookieManager.getInstance().getCookie(adresse);
                if (cookies != null) cnx.setRequestProperty("Cookie", cookies);
                cnx.setRequestProperty("User-Agent", agent);
                cnx.setConnectTimeout(8000);
                cnx.setReadTimeout(60000);
                int statut = cnx.getResponseCode();
                if (statut >= 400) throw new IOException("erreur " + statut + " du serveur");
                try (InputStream entree = cnx.getInputStream()) {
                    byte[] bloc = new byte[65536];
                    for (int n; (n = entree.read(bloc)) != -1; ) sortie.write(bloc, 0, n);
                }
            } finally {
                cnx.disconnect();
            }
        };
    }
}

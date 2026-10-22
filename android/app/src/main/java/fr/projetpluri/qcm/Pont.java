package fr.projetpluri.qcm;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Build;
import android.os.Handler;
import android.os.Looper;
import android.util.Base64;
import android.webkit.JavascriptInterface;
import android.webkit.WebView;

import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Pont entre la page (window.QcmNatif) et le réseau.
 *
 * requete() fait l'appel HTTP en Java et rend la réponse à la page par
 * QcmReseau._fin(id, statut, type, location, corpsBase64) ; appli.js en fait une
 * Response, si bien que le code du wiki l'utilise comme fetch(). Le jeton
 * d'appareil (Authorization: Bearer) n'est ajouté que pour le serveur enregistré.
 */
class Pont {
    private static final int DELAI_CONNEXION_MS = 8000;
    private static final int DELAI_LECTURE_MS = 60000;

    private final WebView vue;
    private final SharedPreferences prefs;
    private final ExecutorService reseau = Executors.newFixedThreadPool(4);
    private final Handler ui = new Handler(Looper.getMainLooper());

    Pont(Context contexte, WebView vue) {
        this.vue = vue;
        this.prefs = contexte.getSharedPreferences("compte", Context.MODE_PRIVATE);
    }

    void arreter() {
        reseau.shutdownNow();
    }

    @JavascriptInterface
    public String serveur() {
        return prefs.getString("serveur", "");
    }

    @JavascriptInterface
    public String joueur() {
        return prefs.getString("joueur", "");
    }

    @JavascriptInterface
    public boolean connecte() {
        return !prefs.getString("jeton", "").isEmpty();
    }

    @JavascriptInterface
    public String nomAppareil() {
        return Build.MANUFACTURER + " " + Build.MODEL;
    }

    @JavascriptInterface
    public void enregistrerCompte(String serveur, String jeton, String joueur) {
        prefs.edit().putString("serveur", serveur).putString("jeton", jeton).putString("joueur", joueur).apply();
    }

    /** Oublie le jeton ; l'adresse du serveur reste proposée à la prochaine connexion. */
    @JavascriptInterface
    public void oublierCompte() {
        prefs.edit().remove("jeton").remove("joueur").apply();
    }

    /** url : chemin du serveur (« /qcm/… ») ou adresse complète ; corps : JSON ou null. */
    @JavascriptInterface
    public void requete(String id, String methode, String url, String corps) {
        reseau.execute(() -> {
            HttpURLConnection cnx = null;
            try {
                String serveur = serveur();
                String cible = url.startsWith("/") ? serveur + url : url;
                if (!cible.startsWith("http://") && !cible.startsWith("https://")) {
                    throw new IllegalArgumentException("aucun serveur configuré");
                }
                cnx = (HttpURLConnection) new URL(cible).openConnection();
                cnx.setConnectTimeout(DELAI_CONNEXION_MS);
                cnx.setReadTimeout(DELAI_LECTURE_MS);
                cnx.setInstanceFollowRedirects(false);
                cnx.setUseCaches(false);
                cnx.setRequestMethod(methode);
                cnx.setRequestProperty("Accept", "application/json, */*");
                String jeton = prefs.getString("jeton", "");
                if (!jeton.isEmpty() && !serveur.isEmpty() && (cible.equals(serveur) || cible.startsWith(serveur + "/"))) {
                    cnx.setRequestProperty("Authorization", "Bearer " + jeton);
                }
                if (corps != null) {
                    byte[] octets = corps.getBytes(StandardCharsets.UTF_8);
                    cnx.setDoOutput(true);
                    cnx.setRequestProperty("Content-Type", "application/json");
                    cnx.setFixedLengthStreamingMode(octets.length);
                    try (OutputStream sortie = cnx.getOutputStream()) {
                        sortie.write(octets);
                    }
                }
                int statut = cnx.getResponseCode();
                String type = cnx.getContentType();
                String location = cnx.getHeaderField("Location");
                byte[] reponse = lire(statut >= 400 ? cnx.getErrorStream() : cnx.getInputStream());
                rendre("QcmReseau._fin(" + JSONObject.quote(id) + "," + statut + "," + JSONObject.quote(type == null ? "" : type)
                        + "," + JSONObject.quote(location == null ? "" : location)
                        + ",\"" + Base64.encodeToString(reponse, Base64.NO_WRAP) + "\")");
            } catch (Exception e) {
                String message = e.getMessage() == null ? e.getClass().getSimpleName() : e.getMessage();
                rendre("QcmReseau._echec(" + JSONObject.quote(id) + "," + JSONObject.quote(message) + ")");
            } finally {
                if (cnx != null) cnx.disconnect();
            }
        });
    }

    private static byte[] lire(InputStream entree) throws java.io.IOException {
        if (entree == null) return new byte[0];
        try (InputStream in = entree; ByteArrayOutputStream tampon = new ByteArrayOutputStream()) {
            byte[] bloc = new byte[16384];
            for (int n; (n = in.read(bloc)) != -1; ) tampon.write(bloc, 0, n);
            return tampon.toByteArray();
        }
    }

    private void rendre(String script) {
        ui.post(() -> vue.evaluateJavascript(script, null));
    }
}

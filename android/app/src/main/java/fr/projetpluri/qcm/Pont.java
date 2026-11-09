package fr.projetpluri.qcm;

import android.content.ContentResolver;
import android.content.Context;
import android.content.SharedPreferences;
import android.database.Cursor;
import android.net.Uri;
import android.provider.OpenableColumns;
import android.os.Build;
import android.os.Handler;
import android.os.Looper;
import android.util.Base64;
import android.webkit.CookieManager;
import android.webkit.JavascriptInterface;
import android.webkit.WebView;

import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.function.Consumer;
import java.util.function.IntConsumer;

/**
 * Pont entre la page (window.QcmNatif) et le réseau.
 *
 * requete() fait l'appel HTTP en Java et rend la réponse à la page par
 * QcmReseau._fin(id, statut, type, location, corpsBase64) ; appli.js en fait une
 * Response, si bien que le code du wiki l'utilise comme fetch(). Le jeton
 * d'appareil (Authorization: Bearer) n'est ajouté que pour le serveur enregistré.
 *
 * L'objet est visible des pages locales seulement (QCM hors ligne, réglages) :
 * quand la page affichée vient du serveur, ses méthodes ne font rien.
 */
class Pont {
    private static final int DELAI_CONNEXION_MS = 8000;
    private static final int DELAI_LECTURE_MS = 60000;

    private final Context contexte;
    private final WebView vue;
    private final SharedPreferences prefs;
    private final ExecutorService reseau = Executors.newFixedThreadPool(4);
    private final Handler ui = new Handler(Looper.getMainLooper());
    private volatile boolean locale = true;

    Pont(Context contexte, WebView vue) {
        this.contexte = contexte.getApplicationContext();
        this.vue = vue;
        this.prefs = contexte.getSharedPreferences("compte", Context.MODE_PRIVATE);
    }

    void arreter() {
        reseau.shutdownNow();
    }

    /** Appelé à chaque page : vrai pour les pages de l'application (assets). */
    void pageLocale(boolean oui) {
        locale = oui;
    }

    String adresse() {
        return prefs.getString("serveur", "");
    }

    boolean aUnCompte() {
        return !adresse().isEmpty() && !prefs.getString("jeton", "").isEmpty();
    }

    /**
     * Échange le jeton contre une session du wiki (cookie mis dans la WebView).
     * ``fin`` reçoit le statut HTTP sur le fil de l'interface (0 : serveur injoignable,
     * 401 : jeton révoqué, alors oublié).
     */
    void ouvrirSession(IntConsumer fin) {
        session(adresse(), statut -> {
            if (statut == 401) effacer();
            fin.accept(statut);
        });
    }

    /** POST /api/appareil/session/ sur ``serveur`` ; cookies mis dans la WebView si 200. */
    private void session(String serveur, IntConsumer fin) {
        String jeton = prefs.getString("jeton", "");
        reseau.execute(() -> {
            int statut = 0;
            List<String> recus = new ArrayList<>();
            HttpURLConnection cnx = null;
            try {
                cnx = (HttpURLConnection) new URL(serveur + "/api/appareil/session/").openConnection();
                cnx.setConnectTimeout(DELAI_CONNEXION_MS);
                cnx.setReadTimeout(DELAI_LECTURE_MS);
                cnx.setInstanceFollowRedirects(false);
                cnx.setUseCaches(false);
                cnx.setRequestMethod("POST");
                cnx.setRequestProperty("Accept", "application/json");
                cnx.setRequestProperty("Authorization", "Bearer " + jeton);
                cnx.setDoOutput(true);
                cnx.setFixedLengthStreamingMode(0);
                cnx.getOutputStream().close();
                statut = cnx.getResponseCode();
                for (Map.Entry<String, List<String>> entete : cnx.getHeaderFields().entrySet()) {
                    if (entete.getKey() != null && entete.getKey().equalsIgnoreCase("Set-Cookie")) recus.addAll(entete.getValue());
                }
                lire(statut >= 400 ? cnx.getErrorStream() : cnx.getInputStream());
            } catch (Exception e) {
                statut = 0;
            } finally {
                if (cnx != null) cnx.disconnect();
            }
            int resultat = statut;
            ui.post(() -> {
                if (resultat == 200) {
                    CookieManager cookies = CookieManager.getInstance();
                    for (String cookie : recus) cookies.setCookie(serveur, cookie);
                    cookies.flush();
                }
                fin.accept(resultat);
            });
        });
    }

    private void effacer() {
        prefs.edit().remove("jeton").remove("joueur").apply();
        CookieManager.getInstance().removeAllCookies(null);
        CookieManager.getInstance().flush();
    }

    @JavascriptInterface
    public String serveur() {
        return locale ? adresse() : "";
    }

    @JavascriptInterface
    public String joueur() {
        return locale ? prefs.getString("joueur", "") : "";
    }

    @JavascriptInterface
    public boolean connecte() {
        return locale && !prefs.getString("jeton", "").isEmpty();
    }

    @JavascriptInterface
    public String nomAppareil() {
        return Build.MANUFACTURER + " " + Build.MODEL;
    }

    @JavascriptInterface
    public void enregistrerCompte(String serveur, String jeton, String joueur) {
        if (!locale) return;
        prefs.edit().putString("serveur", serveur).putString("jeton", jeton).putString("joueur", joueur).apply();
    }

    /**
     * Passe à une autre adresse du même wiki (son adresse publique, par exemple)
     * sans redemander le mot de passe : le jeton n'est envoyé qu'en HTTPS, et
     * l'adresse n'est gardée que si le serveur l'accepte (session ouverte). Rend
     * QcmReseau._statut(id, statut) : 200 fait, 401 appareil inconnu de ce
     * serveur (le jeton reste valable à l'ancienne adresse), 0 injoignable.
     */
    @JavascriptInterface
    public void changerServeur(String id, String nouveau) {
        String retour = "QcmReseau._statut(" + JSONObject.quote(id) + ",";
        if (!locale || nouveau == null || !nouveau.startsWith("https://") || prefs.getString("jeton", "").isEmpty()) {
            rendre(retour + "-1)");
            return;
        }
        ui.post(() -> session(nouveau, statut -> {
            if (statut == 200) prefs.edit().putString("serveur", nouveau).apply();
            rendre(retour + statut + ")");
        }));
    }

    /** Réglages du rappel quotidien : {actif, heure, minute, autorise} (JSON). */
    @JavascriptInterface
    public String rappel() {
        return locale ? Rappel.reglages(contexte).toString() : "{}";
    }

    /** Programme (ou annule) le rappel quotidien ; la permission est demandée par l'activité. */
    @JavascriptInterface
    public void reglerRappel(boolean actif, int heure, int minute) {
        if (!locale) return;
        int h = Math.max(0, Math.min(23, heure)), m = Math.max(0, Math.min(59, minute));
        ui.post(() -> {
            Rappel.programmer(contexte, actif, h, m);
            if (actif && vue.getContext() instanceof MainActivity) {
                ((MainActivity) vue.getContext()).demanderNotifications();
            }
        });
    }

    /** Résultat d'un envoi de fichiers : message à afficher, et page à ouvrir (ou null). */
    static final class Envoi {
        final String message;
        final String chemin;

        Envoi(String message, String chemin) {
            this.message = message;
            this.chemin = chemin;
        }
    }

    /**
     * Envoie des fichiers partagés par une autre application au wiki (/importer/,
     * jeton d'appareil), dans le dossier « Importés », en demandant la
     * transformation des cours par Claude. ``fin`` est appelé sur le fil de l'interface.
     */
    void envoyerFichiers(List<Uri> fichiers, Consumer<Envoi> fin) {
        String serveur = adresse();
        String jeton = prefs.getString("jeton", "");
        reseau.execute(() -> {
            Envoi resultat;
            try {
                resultat = envoyerMultipart(serveur, jeton, fichiers);
            } catch (Exception e) {
                String message = e.getMessage() == null ? e.getClass().getSimpleName() : e.getMessage();
                resultat = new Envoi("Envoi impossible : " + message, null);
            }
            Envoi r = resultat;
            ui.post(() -> fin.accept(r));
        });
    }

    private Envoi envoyerMultipart(String serveur, String jeton, List<Uri> fichiers) throws Exception {
        ContentResolver resolveur = contexte.getContentResolver();
        String frontiere = "----ProjetPluri" + System.currentTimeMillis();
        HttpURLConnection cnx = (HttpURLConnection) new URL(serveur + "/importer/").openConnection();
        cnx.setConnectTimeout(DELAI_CONNEXION_MS);
        cnx.setReadTimeout(DELAI_LECTURE_MS * 5);
        cnx.setInstanceFollowRedirects(false);
        cnx.setUseCaches(false);
        cnx.setRequestMethod("POST");
        cnx.setDoOutput(true);
        cnx.setChunkedStreamingMode(64 * 1024);
        cnx.setRequestProperty("Accept", "application/json");
        cnx.setRequestProperty("Authorization", "Bearer " + jeton);
        cnx.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + frontiere);
        try (OutputStream sortie = cnx.getOutputStream()) {
            champ(sortie, frontiere, "dossier", "Importés");
            champ(sortie, frontiere, "claude", "1");
            for (Uri uri : fichiers) {
                String nom = nomFichier(resolveur, uri);
                champ(sortie, frontiere, "chemins", nom);
                String type = resolveur.getType(uri);
                sortie.write(("--" + frontiere + "\r\nContent-Disposition: form-data; name=\"fichiers\"; filename=\""
                        + nom.replace("\"", "_") + "\"\r\nContent-Type: " + (type == null ? "application/octet-stream" : type)
                        + "\r\n\r\n").getBytes(StandardCharsets.UTF_8));
                try (InputStream entree = resolveur.openInputStream(uri)) {
                    if (entree == null) throw new IllegalStateException("fichier illisible : " + nom);
                    byte[] bloc = new byte[64 * 1024];
                    for (int n; (n = entree.read(bloc)) != -1; ) sortie.write(bloc, 0, n);
                }
                sortie.write("\r\n".getBytes(StandardCharsets.UTF_8));
            }
            sortie.write(("--" + frontiere + "--\r\n").getBytes(StandardCharsets.UTF_8));
        }
        int statut = cnx.getResponseCode();
        String corps = new String(lire(statut >= 400 ? cnx.getErrorStream() : cnx.getInputStream()), StandardCharsets.UTF_8);
        cnx.disconnect();
        if (statut == 401) throw new IllegalStateException("appareil déconnecté du wiki (reconnectez l'application)");
        if (statut == 403) throw new IllegalStateException("l'import est réservé aux admins du wiki");
        if (statut == 413) throw new IllegalStateException("fichier trop gros pour le réseau (100 Mo au plus)");
        if (statut != 200) throw new IllegalStateException("le serveur a répondu " + statut);
        JSONObject reponse = new JSONObject(corps);
        org.json.JSONArray resultats = reponse.getJSONArray("results");
        int ok = 0, claude = 0;
        StringBuilder erreurs = new StringBuilder();
        String premiere = null;
        for (int i = 0; i < resultats.length(); i++) {
            JSONObject r = resultats.getJSONObject(i);
            if (r.optBoolean("ok")) {
                ok++;
                if (!r.optString("claude").isEmpty()) claude++;
                if (premiere == null && !r.optString("url").isEmpty()) premiere = r.optString("url");
            } else if (!r.optBoolean("ignored")) {
                erreurs.append(erreurs.length() == 0 ? "" : " · ").append(r.optString("name")).append(" : ").append(r.optString("message"));
            }
        }
        String message = ok + (ok > 1 ? " fichiers importés" : " fichier importé")
                + (claude > 0 ? ", transformation par Claude lancée" : "")
                + (erreurs.length() > 0 ? ". Refusés : " + erreurs : ".");
        String chemin = claude > 0 ? "/transformations/" : premiere != null ? premiere : "/importer/";
        return new Envoi(message, ok > 0 ? chemin : null);
    }

    private static void champ(OutputStream sortie, String frontiere, String nom, String valeur) throws java.io.IOException {
        sortie.write(("--" + frontiere + "\r\nContent-Disposition: form-data; name=\"" + nom + "\"\r\n\r\n" + valeur + "\r\n")
                .getBytes(StandardCharsets.UTF_8));
    }

    private static String nomFichier(ContentResolver resolveur, Uri uri) {
        String nom = null;
        try (Cursor c = resolveur.query(uri, new String[]{OpenableColumns.DISPLAY_NAME}, null, null, null)) {
            if (c != null && c.moveToFirst()) nom = c.getString(0);
        } catch (Exception ignore) {
            // Fournisseur sans nom : repli sur l'URI.
        }
        if (nom == null || nom.isEmpty()) nom = uri.getLastPathSegment();
        if (nom == null || nom.isEmpty()) nom = "document";
        return nom.replace("/", "_");
    }

    /** Oublie le jeton et la session du wiki ; l'adresse du serveur reste proposée. */
    @JavascriptInterface
    public void oublierCompte() {
        if (!locale) return;
        ui.post(this::effacer);
    }

    /** url : chemin du serveur (« /qcm/… ») ou adresse complète ; corps : JSON ou null. */
    @JavascriptInterface
    public void requete(String id, String methode, String url, String corps) {
        if (!locale) {
            rendre("QcmReseau._echec(" + JSONObject.quote(id) + ",\"réservé aux pages de l'application\")");
            return;
        }
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

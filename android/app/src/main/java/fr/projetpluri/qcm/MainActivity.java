package fr.projetpluri.qcm;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.content.res.Configuration;
import android.graphics.Bitmap;
import android.graphics.Insets;
import android.net.Uri;
import android.net.http.SslError;
import android.os.Build;
import android.os.Bundle;
import android.util.Base64;
import android.view.View;
import android.view.WindowInsets;
import android.view.WindowInsetsController;
import android.webkit.CookieManager;
import android.webkit.JavascriptInterface;
import android.webkit.MimeTypeMap;
import android.webkit.SslErrorHandler;
import android.webkit.URLUtil;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import android.widget.Toast;

import androidx.webkit.WebViewAssetLoader;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/**
 * Application ProjetPluri : le wiki en plein écran, pensé pour le tactile, et
 * les QCM hors ligne embarqués.
 *
 * - Les pages du wiki viennent du serveur choisi au premier lancement. La
 *   session est ouverte avec le jeton de l'appareil ({@link Pont#ouvrirSession}) :
 *   pas de mot de passe à retaper. Le site reconnaît l'application (User-Agent
 *   « ProjetPluriApp/ ») et affiche une barre de navigation en bas de l'écran.
 * - Les pages locales (QCM hors ligne, réglages, « hors réseau ») sont servies
 *   depuis les assets sur https://appassets.androidplatform.net/.
 * - Liens vers d'autres sites : navigateur. Fichiers à envoyer : sélecteur
 *   Android. Téléchargements : « Enregistrer sous » d'Android.
 * - Sans réseau : la dernière version enregistrée de la page si elle existe,
 *   sinon une page qui propose de réessayer ou de réviser hors ligne.
 */
public class MainActivity extends Activity {
    static final String HOTE = "appassets.androidplatform.net";
    static final String LOCAL = "https://" + HOTE + "/";
    static final int CHOIX_FICHIERS = 1;
    static final int ENREGISTRER = 2;

    private FrameLayout cadre;
    private WebView vue;
    private WebSettings reglages;
    private Pont pont;
    private Fichiers fichiers;
    private String agent;
    private Interface chrome;
    private ValueCallback<Uri[]> choixEnAttente;
    private View pleinEcran;
    private WebChromeClient.CustomViewCallback finPleinEcran;
    private boolean sessionTentee;
    private boolean essaiCache;
    private boolean echec;

    @SuppressLint({"SetJavaScriptEnabled", "JavascriptInterface"})
    @Override
    protected void onCreate(Bundle etat) {
        super.onCreate(etat);
        vue = new WebView(this);
        cadre = new FrameLayout(this);
        cadre.addView(vue, new FrameLayout.LayoutParams(FrameLayout.LayoutParams.MATCH_PARENT, FrameLayout.LayoutParams.MATCH_PARENT));
        setContentView(cadre);
        // Android 15 affiche l'application sous les barres système : on s'en écarte.
        if (Build.VERSION.SDK_INT >= 35) {
            cadre.setOnApplyWindowInsetsListener((v, insets) -> {
                Insets b = insets.getInsets(WindowInsets.Type.systemBars() | WindowInsets.Type.ime());
                v.setPadding(b.left, b.top, b.right, b.bottom);
                return WindowInsets.CONSUMED;
            });
        }
        boolean nuit = (getResources().getConfiguration().uiMode & Configuration.UI_MODE_NIGHT_MASK) == Configuration.UI_MODE_NIGHT_YES;
        vue.setBackgroundColor(nuit ? 0xff1e1e1e : 0xffffffff);

        reglages = vue.getSettings();
        reglages.setJavaScriptEnabled(true);
        reglages.setDomStorageEnabled(true);
        reglages.setAllowFileAccess(false);
        // Lecture des fichiers choisis dans le sélecteur (content://) pour l'envoi : seules
        // les pages du serveur choisi et de l'application sont chargées.
        reglages.setAllowContentAccess(true);
        reglages.setSupportZoom(true);
        reglages.setBuiltInZoomControls(true);
        reglages.setDisplayZoomControls(false);
        reglages.setTextZoom(Math.round(getResources().getConfiguration().fontScale * 100));
        agent = reglages.getUserAgentString() + " ProjetPluriApp/" + version();
        reglages.setUserAgentString(agent);

        CookieManager cookies = CookieManager.getInstance();
        cookies.setAcceptCookie(true);
        cookies.setAcceptThirdPartyCookies(vue, false);

        pont = new Pont(this, vue);
        fichiers = new Fichiers(this);
        vue.addJavascriptInterface(pont, "QcmNatif");
        vue.addJavascriptInterface(new Appli(), "AppliNatif");

        WebViewAssetLoader assets = new WebViewAssetLoader.Builder()
                .setDomain(HOTE)
                .addPathHandler("/", new WebViewAssetLoader.AssetsPathHandler(this))
                .build();
        vue.setWebViewClient(new Navigation(assets));
        chrome = new Interface();
        vue.setWebChromeClient(chrome);
        vue.setDownloadListener((url, userAgent, disposition, type, taille) -> {
            if (!URLUtil.isNetworkUrl(url)) {
                toast("Ce fichier ne peut pas être téléchargé depuis l'application.");
                return;
            }
            String nom = Uri.decode(URLUtil.guessFileName(url, disposition, type));
            fichiers.enregistrerSous(nom, type, fichiers.depuis(url, agent));
        });

        if (etat != null) vue.restoreState(etat);
        else ouvrirWiki("/");
    }

    private String version() {
        try {
            return getPackageManager().getPackageInfo(getPackageName(), 0).versionName;
        } catch (Exception e) {
            return "2";
        }
    }

    /** Page du wiki (chemin « /… ») ; réglages si l'application n'est pas encore connectée. */
    void ouvrirWiki(String chemin) {
        if (!pont.aUnCompte()) {
            vue.loadUrl(LOCAL + "connexion.html");
            return;
        }
        vue.loadUrl(pont.adresse() + chemin);
    }

    /** Ouvre la session du wiki avec le jeton, puis affiche ``chemin``. */
    private void ouvrirSession(String chemin) {
        sessionTentee = true;
        pont.ouvrirSession(statut -> {
            if (statut == 200) vue.loadUrl(pont.adresse() + chemin);
            else if (statut == 401) vue.loadUrl(LOCAL + "connexion.html?revoque=1");
            else if (statut == 0) vue.loadUrl(LOCAL + "hors-reseau.html?url=" + Uri.encode(pont.adresse() + chemin));
            // Serveur qui ne connaît pas encore cette fonction : formulaire de connexion du wiki.
            else vue.loadUrl(pont.adresse() + "/connexion/?next=" + Uri.encode(chemin));
        });
    }

    private boolean estServeur(Uri url) {
        String serveur = pont.adresse();
        if (serveur.isEmpty() || url.getHost() == null) return false;
        return url.getHost().equalsIgnoreCase(Uri.parse(serveur).getHost());
    }

    private static boolean estConnexion(Uri url) {
        return url.getPath() != null && url.getPath().startsWith("/connexion");
    }

    private static String suivante(Uri url) {
        String next = url.getQueryParameter("next");
        return next != null && next.startsWith("/") && !next.startsWith("//") ? next : "/";
    }

    private void ouvrirDehors(Uri url) {
        try {
            startActivity(new Intent(Intent.ACTION_VIEW, url));
        } catch (ActivityNotFoundException ignore) {
            toast("Aucune application pour ouvrir ce lien.");
        }
    }

    void toast(String texte) {
        Toast.makeText(this, texte, Toast.LENGTH_LONG).show();
    }

    // -- Navigation ---------------------------------------------------------------------

    private class Navigation extends WebViewClient {
        private final WebViewAssetLoader assets;

        Navigation(WebViewAssetLoader assets) {
            this.assets = assets;
        }

        @Override
        public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
            Uri url = request.getUrl();
            if (HOTE.equals(url.getHost())) {
                String chemin = url.getPath() == null || url.getPath().equals("/") ? "/index.html" : url.getPath();
                return assets.shouldInterceptRequest(url.buildUpon().path(chemin).build());
            }
            return null;
        }

        @Override
        public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
            if (!request.isForMainFrame()) return false;
            Uri url = request.getUrl();
            if (HOTE.equals(url.getHost())) {
                String chemin = url.getPath() == null ? "/" : url.getPath();
                if (chemin.equals("/") || chemin.endsWith(".html")) return false;
                // Lien du wiki écrit dans une page locale (ex. /wiki/Page) : sur le serveur.
                if (pont.aUnCompte()) view.loadUrl(pont.adresse() + chemin + (url.getQuery() == null ? "" : "?" + url.getQuery()));
                return true;
            }
            if (estServeur(url)) {
                if (estConnexion(url) && pont.aUnCompte() && !sessionTentee) {
                    ouvrirSession(suivante(url));
                    return true;
                }
                return false;
            }
            ouvrirDehors(url);
            return true;
        }

        @Override
        public void onPageStarted(WebView view, String adresse, Bitmap icone) {
            Uri url = Uri.parse(adresse);
            echec = false;
            pont.pageLocale(HOTE.equals(url.getHost()));
            // Session expirée : le wiki renvoie vers sa page de connexion, on la rouvre avec le jeton.
            if (estServeur(url) && estConnexion(url) && pont.aUnCompte() && !sessionTentee) {
                view.stopLoading();
                ouvrirSession(suivante(url));
            }
        }

        @Override
        public void onPageFinished(WebView view, String adresse) {
            Uri url = Uri.parse(adresse);
            if (!estConnexion(url) && !echec) sessionTentee = false;
            if (essaiCache && !echec) {
                essaiCache = false;
                reglages.setCacheMode(WebSettings.LOAD_DEFAULT);
                toast("Pas de connexion au wiki : dernière version enregistrée de cette page.");
            }
        }

        @Override
        public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError erreur) {
            if (!request.isForMainFrame() || HOTE.equals(request.getUrl().getHost())) return;
            echec = true;
            String adresse = request.getUrl().toString();
            if (!essaiCache) {
                // Serveur injoignable : la page déjà vue est peut-être dans le cache.
                essaiCache = true;
                reglages.setCacheMode(WebSettings.LOAD_CACHE_ONLY);
                view.post(() -> view.loadUrl(adresse));
            } else {
                essaiCache = false;
                reglages.setCacheMode(WebSettings.LOAD_DEFAULT);
                view.post(() -> view.loadUrl(LOCAL + "hors-reseau.html?url=" + Uri.encode(adresse)));
            }
        }

        @Override
        public void onReceivedSslError(WebView view, SslErrorHandler handler, SslError erreur) {
            // Jamais de certificat accepté à l'aveugle : on explique comment installer l'autorité.
            handler.cancel();
            if (!estServeur(Uri.parse(erreur.getUrl()))) return;
            echec = true;
            view.post(() -> view.loadUrl(LOCAL + "hors-reseau.html?ssl=1&url=" + Uri.encode(erreur.getUrl())));
        }
    }

    // -- Fichiers, plein écran ----------------------------------------------------------------

    private class Interface extends WebChromeClient {
        @Override
        public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> rappel, FileChooserParams params) {
            if (choixEnAttente != null) choixEnAttente.onReceiveValue(null);
            choixEnAttente = rappel;
            Intent choix = new Intent(Intent.ACTION_GET_CONTENT).addCategory(Intent.CATEGORY_OPENABLE).setType("*/*");
            String[] types = typesMime(params.getAcceptTypes());
            if (types.length > 0) choix.putExtra(Intent.EXTRA_MIME_TYPES, types);
            if (params.getMode() == FileChooserParams.MODE_OPEN_MULTIPLE) choix.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
            try {
                startActivityForResult(Intent.createChooser(choix, null), CHOIX_FICHIERS);
            } catch (ActivityNotFoundException e) {
                choixEnAttente = null;
                return false;
            }
            return true;
        }

        @Override
        public void onShowCustomView(View view, CustomViewCallback rappel) {
            if (pleinEcran != null) {
                rappel.onCustomViewHidden();
                return;
            }
            pleinEcran = view;
            finPleinEcran = rappel;
            cadre.addView(view, new FrameLayout.LayoutParams(FrameLayout.LayoutParams.MATCH_PARENT, FrameLayout.LayoutParams.MATCH_PARENT));
            vue.setVisibility(View.GONE);
            barresSysteme(false);
        }

        @Override
        public void onHideCustomView() {
            if (pleinEcran == null) return;
            cadre.removeView(pleinEcran);
            pleinEcran = null;
            vue.setVisibility(View.VISIBLE);
            barresSysteme(true);
            if (finPleinEcran != null) finPleinEcran.onCustomViewHidden();
            finPleinEcran = null;
        }
    }

    /** Types acceptés par le champ (« .pdf,image/* ») ; vide si une extension est inconnue (tout accepter). */
    private static String[] typesMime(String[] acceptes) {
        List<String> types = new ArrayList<>();
        for (String accepte : acceptes) {
            for (String type : accepte.split(",")) {
                type = type.trim().toLowerCase(Locale.ROOT);
                if (type.isEmpty()) continue;
                if (type.contains("/")) {
                    types.add(type);
                    continue;
                }
                String mime = MimeTypeMap.getSingleton().getMimeTypeFromExtension(type.replaceFirst("^\\.", ""));
                if (mime == null) return new String[0];
                types.add(mime);
            }
        }
        return types.toArray(new String[0]);
    }

    @SuppressWarnings("deprecation")
    private void barresSysteme(boolean visibles) {
        if (Build.VERSION.SDK_INT >= 30) {
            WindowInsetsController controle = getWindow().getInsetsController();
            if (controle == null) return;
            if (visibles) {
                controle.show(WindowInsets.Type.systemBars());
            } else {
                controle.setSystemBarsBehavior(WindowInsetsController.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
                controle.hide(WindowInsets.Type.systemBars());
            }
        } else {
            getWindow().getDecorView().setSystemUiVisibility(visibles ? View.SYSTEM_UI_FLAG_VISIBLE
                    : View.SYSTEM_UI_FLAG_FULLSCREEN | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);
        }
    }

    @Override
    protected void onActivityResult(int code, int resultat, Intent donnees) {
        super.onActivityResult(code, resultat, donnees);
        if (code == CHOIX_FICHIERS && choixEnAttente != null) {
            Uri[] choisis = null;
            if (resultat == RESULT_OK && donnees != null) {
                if (donnees.getClipData() != null) {
                    choisis = new Uri[donnees.getClipData().getItemCount()];
                    for (int i = 0; i < choisis.length; i++) choisis[i] = donnees.getClipData().getItemAt(i).getUri();
                } else if (donnees.getData() != null) {
                    choisis = new Uri[]{donnees.getData()};
                }
            }
            choixEnAttente.onReceiveValue(choisis);
            choixEnAttente = null;
        } else if (code == ENREGISTRER) {
            fichiers.resultat(resultat, donnees);
        }
    }

    // -- Pont pour toutes les pages (rien de sensible : pas de jeton) ------------------------

    private class Appli {
        @JavascriptInterface
        public String version() {
            return MainActivity.this.version();
        }

        @JavascriptInterface
        public void ouvrirWiki() {
            runOnUiThread(() -> MainActivity.this.ouvrirWiki("/"));
        }

        /** Fichier produit par la page (ex. « Télécharger la page en .md » de l'éditeur). */
        @JavascriptInterface
        public void enregistrer(String nom, String type, String base64) {
            byte[] octets = Base64.decode(base64, Base64.DEFAULT);
            runOnUiThread(() -> fichiers.enregistrerSous(nom, type, sortie -> sortie.write(octets)));
        }
    }

    // -- Cycle de vie -----------------------------------------------------------------------

    @Override
    protected void onSaveInstanceState(Bundle etat) {
        super.onSaveInstanceState(etat);
        vue.saveState(etat);
    }

    @Override
    protected void onPause() {
        super.onPause();
        CookieManager.getInstance().flush();
    }

    @Override
    @SuppressWarnings("deprecation")
    public void onBackPressed() {
        if (pleinEcran != null) {
            chrome.onHideCustomView();
            return;
        }
        // La page peut d'abord fermer son menu latéral ou une fenêtre (window.appliRetour).
        vue.evaluateJavascript("window.appliRetour ? window.appliRetour() : false", valeur -> {
            if ("true".equals(valeur)) return;
            if (vue.canGoBack()) vue.goBack();
            else finish();
        });
    }

    @Override
    protected void onDestroy() {
        pont.arreter();
        fichiers.arreter();
        vue.destroy();
        super.onDestroy();
    }
}

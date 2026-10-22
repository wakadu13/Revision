package fr.projetpluri.qcm;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Intent;
import android.graphics.Insets;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.WindowInsets;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;

import androidx.webkit.WebViewAssetLoader;

/**
 * QCM hors ligne : la page du wiki (/qcm/hors-ligne/) embarquée dans l'APK.
 *
 * Les pages sont servies depuis les assets sur https://appassets.androidplatform.net/
 * (origine sécurisée : IndexedDB garde les sets et les réponses sur le téléphone).
 * Les échanges avec le serveur Pi passent par {@link Pont} (code natif) : pas de
 * CORS ni de contenu mixte, et le jeton d'appareil n'est jamais exposé au réseau
 * autrement que vers le serveur choisi.
 */
public class MainActivity extends Activity {
    static final String HOTE = "appassets.androidplatform.net";
    static final String ACCUEIL = "https://" + HOTE + "/";

    private WebView vue;
    private Pont pont;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle etat) {
        super.onCreate(etat);
        vue = new WebView(this);
        FrameLayout cadre = new FrameLayout(this);
        cadre.addView(vue);
        setContentView(cadre);
        // Android 15 affiche l'application sous les barres système : on s'en écarte.
        if (Build.VERSION.SDK_INT >= 35) {
            cadre.setOnApplyWindowInsetsListener((v, insets) -> {
                Insets b = insets.getInsets(WindowInsets.Type.systemBars() | WindowInsets.Type.ime());
                v.setPadding(b.left, b.top, b.right, b.bottom);
                return WindowInsets.CONSUMED;
            });
        }

        WebSettings reglages = vue.getSettings();
        reglages.setJavaScriptEnabled(true);
        reglages.setDomStorageEnabled(true);
        reglages.setAllowFileAccess(false);
        reglages.setAllowContentAccess(false);

        WebViewAssetLoader assets = new WebViewAssetLoader.Builder()
                .setDomain(HOTE)
                .addPathHandler("/", new WebViewAssetLoader.AssetsPathHandler(this))
                .build();
        pont = new Pont(this, vue);
        vue.addJavascriptInterface(pont, "QcmNatif");
        vue.setWebViewClient(new WebViewClient() {
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
                Uri url = request.getUrl();
                if (HOTE.equals(url.getHost())) {
                    String chemin = url.getPath() == null ? "/" : url.getPath();
                    if (chemin.equals("/") || chemin.endsWith(".html")) return false;
                    // Lien interne du wiki (ex. /wiki/Page) : ouvert sur le serveur, dans le navigateur.
                    String serveur = pont.serveur();
                    if (serveur.isEmpty()) return true;
                    url = Uri.parse(serveur + chemin + (url.getQuery() == null ? "" : "?" + url.getQuery()));
                }
                ouvrirDehors(url);
                return true;
            }
        });

        if (etat == null) vue.loadUrl(ACCUEIL);
        else vue.restoreState(etat);
    }

    private void ouvrirDehors(Uri url) {
        try {
            startActivity(new Intent(Intent.ACTION_VIEW, url));
        } catch (Exception ignore) {
            // aucun navigateur
        }
    }

    @Override
    protected void onSaveInstanceState(Bundle etat) {
        super.onSaveInstanceState(etat);
        vue.saveState(etat);
    }

    @Override
    @SuppressWarnings("deprecation")
    public void onBackPressed() {
        if (vue.canGoBack()) vue.goBack();
        else super.onBackPressed();
    }

    @Override
    protected void onDestroy() {
        pont.arreter();
        vue.destroy();
        super.onDestroy();
    }
}

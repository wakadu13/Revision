package fr.projetpluri.qcm;

import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.widget.RemoteViews;

import androidx.work.Constraints;
import androidx.work.ExistingWorkPolicy;
import androidx.work.NetworkType;
import androidx.work.OneTimeWorkRequest;
import androidx.work.WorkManager;

import org.json.JSONObject;

/**
 * Widget d'écran d'accueil : ce qu'il reste à réviser et la série de jours, d'après
 * /api/rappel/ (demandé par MajWidget en arrière-plan ; rafraîchi par le rappel
 * quotidien, à l'ouverture de l'application et toutes les 30 minutes). Un appui ouvre
 * les QCM.
 */
public class Widget extends AppWidgetProvider {
    static final String TRAVAIL = "maj-widget";

    @Override
    public void onUpdate(Context contexte, AppWidgetManager gestion, int[] ids) {
        afficher(contexte, gestion, ids, null);
        planifier(contexte);
    }

    /** Demande une mise à jour du widget (rien si aucun widget n'est posé). */
    static void planifier(Context contexte) {
        if (!aDesWidgets(contexte)) return;
        OneTimeWorkRequest demande = new OneTimeWorkRequest.Builder(MajWidget.class)
                .setConstraints(new Constraints.Builder().setRequiredNetworkType(NetworkType.CONNECTED).build())
                .build();
        WorkManager.getInstance(contexte).enqueueUniqueWork(TRAVAIL, ExistingWorkPolicy.KEEP, demande);
    }

    static boolean aDesWidgets(Context contexte) {
        AppWidgetManager gestion = AppWidgetManager.getInstance(contexte);
        return gestion.getAppWidgetIds(new ComponentName(contexte, Widget.class)).length > 0;
    }

    /** Affiche l'état reçu du serveur (ou un texte d'attente si null) sur tous les widgets. */
    static void rafraichir(Context contexte, JSONObject etat) {
        AppWidgetManager gestion = AppWidgetManager.getInstance(contexte);
        afficher(contexte, gestion, gestion.getAppWidgetIds(new ComponentName(contexte, Widget.class)), etat);
    }

    private static void afficher(Context contexte, AppWidgetManager gestion, int[] ids, JSONObject etat) {
        if (ids == null || ids.length == 0) return;
        String compte, detail;
        if (etat == null) {
            compte = contexte.getString(R.string.widget_attente);
            detail = contexte.getString(R.string.widget_ouvrir);
        } else {
            int n = etat.optInt("a_revoir", 0);
            int serie = etat.optInt("serie", 0);
            compte = n == 0 ? contexte.getString(R.string.widget_a_jour) : n + (n > 1 ? " éléments à réviser" : " élément à réviser");
            detail = serie > 0 ? "🔥 " + serie + " jour" + (serie > 1 ? "s" : "") + " d'affilée" : contexte.getString(R.string.widget_serie_vide);
            if (etat.optInt("aujourdhui", 0) == 0 && serie > 0) detail += " · à prolonger aujourd'hui";
            if (n > 0) detail += " · QCM " + etat.optInt("qcm", 0) + " · langues " + etat.optInt("langues", 0);
        }
        Intent ouvrir = new Intent(contexte, MainActivity.class)
                .putExtra(MainActivity.EXTRA_CHEMIN, "/qcm/")
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);
        PendingIntent clic = PendingIntent.getActivity(contexte, 1, ouvrir, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        for (int id : ids) {
            RemoteViews vues = new RemoteViews(contexte.getPackageName(), R.layout.widget);
            vues.setTextViewText(R.id.widget_compte, compte);
            vues.setTextViewText(R.id.widget_detail, detail);
            vues.setOnClickPendingIntent(R.id.widget_racine, clic);
            gestion.updateAppWidget(id, vues);
        }
    }
}

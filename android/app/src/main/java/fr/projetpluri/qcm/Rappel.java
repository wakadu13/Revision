package fr.projetpluri.qcm;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.os.Build;

import androidx.annotation.NonNull;
import androidx.core.app.NotificationCompat;
import androidx.core.content.ContextCompat;
import androidx.work.ExistingPeriodicWorkPolicy;
import androidx.work.PeriodicWorkRequest;
import androidx.work.WorkManager;
import androidx.work.Worker;
import androidx.work.WorkerParameters;

import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Calendar;
import java.util.concurrent.TimeUnit;

/**
 * Rappel quotidien de révision : une notification à l'heure choisie dans les
 * réglages de l'application, avec ce qu'il reste à réviser (demandé au serveur
 * avec le jeton d'appareil ; texte générique sans réseau). Rien si tout est déjà
 * révisé et qu'on a travaillé aujourd'hui. WorkManager relance le rappel après
 * un redémarrage du téléphone.
 */
public class Rappel extends Worker {
    static final String TRAVAIL = "rappel-quotidien";
    static final String CANAL = "rappels";
    static final String PREFS = "rappel";
    private static final int NOTIFICATION = 1;

    public Rappel(@NonNull Context contexte, @NonNull WorkerParameters params) {
        super(contexte, params);
    }

    /** Programme (ou annule) le rappel quotidien à heure:minute, heure locale. */
    static void programmer(Context contexte, boolean actif, int heure, int minute) {
        SharedPreferences prefs = contexte.getSharedPreferences(PREFS, Context.MODE_PRIVATE);
        prefs.edit().putBoolean("actif", actif).putInt("heure", heure).putInt("minute", minute).apply();
        WorkManager gestion = WorkManager.getInstance(contexte);
        if (!actif) {
            gestion.cancelUniqueWork(TRAVAIL);
            return;
        }
        Calendar prochain = Calendar.getInstance();
        prochain.set(Calendar.HOUR_OF_DAY, heure);
        prochain.set(Calendar.MINUTE, minute);
        prochain.set(Calendar.SECOND, 0);
        if (prochain.getTimeInMillis() <= System.currentTimeMillis()) prochain.add(Calendar.DAY_OF_YEAR, 1);
        long delai = prochain.getTimeInMillis() - System.currentTimeMillis();
        PeriodicWorkRequest demande = new PeriodicWorkRequest.Builder(Rappel.class, 24, TimeUnit.HOURS)
                .setInitialDelay(delai, TimeUnit.MILLISECONDS)
                .build();
        gestion.enqueueUniquePeriodicWork(TRAVAIL, ExistingPeriodicWorkPolicy.UPDATE, demande);
    }

    static JSONObject reglages(Context contexte) {
        SharedPreferences prefs = contexte.getSharedPreferences(PREFS, Context.MODE_PRIVATE);
        JSONObject o = new JSONObject();
        try {
            o.put("actif", prefs.getBoolean("actif", false));
            o.put("heure", prefs.getInt("heure", 19));
            o.put("minute", prefs.getInt("minute", 0));
            o.put("autorise", notificationsAutorisees(contexte));
        } catch (Exception ignore) {
            // JSONObject.put ne lève pas pour ces types.
        }
        return o;
    }

    static boolean notificationsAutorisees(Context contexte) {
        if (Build.VERSION.SDK_INT < 33) return true;
        return ContextCompat.checkSelfPermission(contexte, "android.permission.POST_NOTIFICATIONS") == PackageManager.PERMISSION_GRANTED;
    }

    @NonNull
    @Override
    public Result doWork() {
        Context contexte = getApplicationContext();
        if (!notificationsAutorisees(contexte)) return Result.success();
        SharedPreferences compte = contexte.getSharedPreferences("compte", Context.MODE_PRIVATE);
        String serveur = compte.getString("serveur", "");
        String jeton = compte.getString("jeton", "");
        if (serveur.isEmpty() || jeton.isEmpty()) return Result.success();

        String texte = "C'est l'heure de réviser un peu.";
        JSONObject etat = demander(serveur + "/api/rappel/", jeton);
        if (etat != null) {
            int aRevoir = etat.optInt("a_revoir", 0);
            int serie = etat.optInt("serie", 0);
            int aujourdhui = etat.optInt("aujourdhui", 0);
            if (aRevoir == 0 && aujourdhui > 0) return Result.success(); // déjà fait pour aujourd'hui
            if (aRevoir > 0) texte = aRevoir + (aRevoir > 1 ? " éléments à réviser" : " élément à réviser");
            else texte = "Rien d'urgent : quelques nouveaux mots ?";
            if (serie > 0) texte += " · série de " + serie + " jour" + (serie > 1 ? "s" : "") + (aujourdhui == 0 ? " à prolonger" : "");
        }
        notifier(contexte, texte);
        return Result.success();
    }

    private static JSONObject demander(String adresse, String jeton) {
        HttpURLConnection cnx = null;
        try {
            cnx = (HttpURLConnection) new URL(adresse).openConnection();
            cnx.setConnectTimeout(8000);
            cnx.setReadTimeout(15000);
            cnx.setRequestProperty("Accept", "application/json");
            cnx.setRequestProperty("Authorization", "Bearer " + jeton);
            if (cnx.getResponseCode() != 200) return null;
            try (InputStream in = cnx.getInputStream(); ByteArrayOutputStream tampon = new ByteArrayOutputStream()) {
                byte[] bloc = new byte[4096];
                for (int n; (n = in.read(bloc)) != -1; ) tampon.write(bloc, 0, n);
                return new JSONObject(tampon.toString(StandardCharsets.UTF_8.name()));
            }
        } catch (Exception e) {
            return null;
        } finally {
            if (cnx != null) cnx.disconnect();
        }
    }

    private static void notifier(Context contexte, String texte) {
        NotificationManager gestion = (NotificationManager) contexte.getSystemService(Context.NOTIFICATION_SERVICE);
        if (gestion == null) return;
        gestion.createNotificationChannel(new NotificationChannel(CANAL, "Rappels de révision", NotificationManager.IMPORTANCE_DEFAULT));
        Intent ouvrir = new Intent(contexte, MainActivity.class)
                .putExtra(MainActivity.EXTRA_CHEMIN, "/qcm/")
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);
        PendingIntent clic = PendingIntent.getActivity(contexte, 0, ouvrir, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        Notification n = new NotificationCompat.Builder(contexte, CANAL)
                .setSmallIcon(android.R.drawable.ic_menu_edit)
                .setContentTitle("ProjetPluri")
                .setContentText(texte)
                .setStyle(new NotificationCompat.BigTextStyle().bigText(texte))
                .setContentIntent(clic)
                .setAutoCancel(true)
                .build();
        try {
            gestion.notify(NOTIFICATION, n);
        } catch (SecurityException ignore) {
            // Permission retirée entre-temps.
        }
    }
}

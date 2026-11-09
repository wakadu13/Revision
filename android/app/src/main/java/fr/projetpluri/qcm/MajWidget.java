package fr.projetpluri.qcm;

import android.content.Context;
import android.content.SharedPreferences;

import androidx.annotation.NonNull;
import androidx.work.Worker;
import androidx.work.WorkerParameters;

import org.json.JSONObject;

/** Mise à jour du widget : demande /api/rappel/ au serveur (jeton d'appareil) et affiche le résultat. */
public class MajWidget extends Worker {
    public MajWidget(@NonNull Context contexte, @NonNull WorkerParameters params) {
        super(contexte, params);
    }

    @NonNull
    @Override
    public Result doWork() {
        Context contexte = getApplicationContext();
        SharedPreferences compte = contexte.getSharedPreferences("compte", Context.MODE_PRIVATE);
        String serveur = compte.getString("serveur", "");
        String jeton = compte.getString("jeton", "");
        if (serveur.isEmpty() || jeton.isEmpty()) {
            Widget.rafraichir(contexte, null);
            return Result.success();
        }
        JSONObject etat = Rappel.demander(serveur + "/api/rappel/", jeton);
        if (etat == null) return getRunAttemptCount() < 3 ? Result.retry() : Result.failure();
        compte.edit().putBoolean("admin", etat.optBoolean("admin", false)).apply();
        Widget.rafraichir(contexte, etat);
        return Result.success();
    }
}

from django.db import migrations, models


def reprise_des_donnees(apps, schema_editor):
    # Une question vue une seule fois l'a été pour la première fois à sa dernière révision.
    QuizProgress = apps.get_model("wiki", "QuizProgress")
    QuizProgress.objects.filter(seen__lte=1, premiere_revue__isnull=True).update(premiere_revue=models.F("last_review"))
    # L'ancienne limite unique s'appliquait aussi aux nouvelles : on la garde pour les deux quotas.
    QuizDeck = apps.get_model("wiki", "QuizDeck")
    QuizDeck.objects.filter(nouvelles_jour__isnull=True).update(nouvelles_jour=models.F("revisions_jour"))


class Migration(migrations.Migration):

    dependencies = [
        ("wiki", "0002_quizdeck"),
    ]

    operations = [
        # L'ancienne limite unique devient la limite des révisions et des nouvelles.
        migrations.RenameField("quizdeck", "limite_jour", "revisions_jour"),
        migrations.AddField(
            model_name="quizdeck",
            name="nouvelles_jour",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="quizprogress",
            name="premiere_revue",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RunPython(reprise_des_donnees, migrations.RunPython.noop),
    ]

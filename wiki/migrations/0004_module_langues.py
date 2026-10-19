from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wiki", "0003_quotas_nouvelles_revisions"),
    ]

    operations = [
        migrations.AddField(
            model_name="quizprogress",
            name="stabilite",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="quizprogress",
            name="difficulte",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="quizprogress",
            name="echeance",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="quizprogress",
            name="decouverte",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="quizprogress",
            name="oublis",
            field=models.PositiveIntegerField(default=0),
        ),
    ]

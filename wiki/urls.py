from django.urls import path

from . import langues_views, quiz_views, views

app_name = "wiki"

urlpatterns = [
    path("", views.home, name="home"),
    path("wiki/<path:path>", views.page, name="page"),
    path("fichiers/<path:path>", views.file, name="file"),
    path("tags/", views.tags, name="tags"),
    path("tags/<path:tag>", views.tag, name="tag"),
    path("sommaire/", views.sommaire, name="sommaire"),
    path("recherche/", views.search, name="search"),
    path("documentation/", views.documentation, name="documentation"),
    path("documentation/<slug:doc>/", views.documentation, name="documentation_doc"),
    path("nouvelle/", views.new, name="new"),
    path("modifier/<path:path>", views.edit, name="edit"),
    path("apercu/<path:path>", views.preview, name="preview"),
    path("qcm/", quiz_views.index, name="quiz_index"),
    path("qcm/jouer/", quiz_views.play, name="quiz_play"),
    path("qcm/reponse/", quiz_views.record, name="quiz_record"),
    path("qcm/importer/", quiz_views.importer, name="quiz_import"),
    path("qcm/deplacer/", quiz_views.deplacer, name="quiz_move"),
    path("qcm/supprimer/", quiz_views.supprimer, name="quiz_delete"),
    path("qcm/planning/", quiz_views.plan, name="quiz_plan"),
    path("qcm/stats/", quiz_views.stats, name="quiz_stats"),
    path("qcm/reinitialiser/", quiz_views.reset, name="quiz_reset"),
    path("qcm/langue/corriger/", langues_views.corriger, name="langue_corriger"),
    path("qcm/langue/reponse/", langues_views.record, name="langue_record"),
    path("qcm/langues/<str:langue>/", langues_views.menu, name="langue_menu"),
    path("qcm/langues/<str:langue>/jouer/", langues_views.play, name="langue_play"),
    path("qcm/langues/<str:langue>/reinitialiser/", langues_views.reset, name="langue_reset"),
]

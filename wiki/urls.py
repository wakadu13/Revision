from django.urls import path

from . import hors_ligne_views, langues_views, quiz_views, views

app_name = "wiki"

urlpatterns = [
    path("", views.home, name="home"),
    path("wiki/<path:path>", views.page, name="page"),
    path("fichiers/<path:path>", views.file, name="file"),
    path("pdf/<path:path>", views.pdf, name="pdf"),
    path("tags/", views.tags, name="tags"),
    path("tags/<path:tag>", views.tag, name="tag"),
    path("sommaire/", views.sommaire, name="sommaire"),
    path("recherche/", views.search, name="search"),
    path("documentation/", views.documentation, name="documentation"),
    path("documentation/<slug:doc>/", views.documentation, name="documentation_doc"),
    path("nouvelle/", views.new, name="new"),
    path("importer/", views.import_files, name="import"),
    path("latex/", views.latex, name="latex"),
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
    path("qcm/hors-ligne/", hors_ligne_views.page, name="quiz_offline"),
    path("qcm/hors-ligne/catalogue/", hors_ligne_views.catalogue, name="quiz_offline_catalogue"),
    path("qcm/hors-ligne/sets/", hors_ligne_views.telecharger, name="quiz_offline_sets"),
    path("qcm/hors-ligne/synchro/", hors_ligne_views.synchro, name="quiz_offline_sync"),
    path("qcm/sw.js", hors_ligne_views.service_worker, name="quiz_sw"),
    path("qcm/manifest.webmanifest", hors_ligne_views.manifest, name="quiz_manifest"),
    path("qcm/langue/corriger/", langues_views.corriger, name="langue_corriger"),
    path("qcm/langue/reponse/", langues_views.record, name="langue_record"),
    path("qcm/langues/<str:langue>/", langues_views.menu, name="langue_menu"),
    path("qcm/langues/<str:langue>/jouer/", langues_views.play, name="langue_play"),
    path("qcm/langues/<str:langue>/reinitialiser/", langues_views.reset, name="langue_reset"),
]

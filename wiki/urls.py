from django.urls import path

from . import quiz_views, views

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
    path("qcm/planning/", quiz_views.plan, name="quiz_plan"),
    path("qcm/stats/", quiz_views.stats, name="quiz_stats"),
    path("qcm/reinitialiser/", quiz_views.reset, name="quiz_reset"),
]

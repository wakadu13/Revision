from django.contrib import admin

from .models import JetonAppareil


@admin.register(JetonAppareil)
class JetonAppareilAdmin(admin.ModelAdmin):
    list_display = ["user", "nom", "cree", "utilise"]
    readonly_fields = ["user", "empreinte", "cree", "utilise"]

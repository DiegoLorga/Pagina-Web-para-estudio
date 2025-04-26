from django.contrib import admin
from .models import Agenda


class AgendaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'importante', 'fecha_evento','descripcion')
    search_fields = ('titulo','fecha_evento')
    list_filter = ('titulo','fecha_evento')

admin.site.register(Agenda, AgendaAdmin)
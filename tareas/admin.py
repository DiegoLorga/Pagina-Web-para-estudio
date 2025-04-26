from django.contrib import admin
from .models import Tarea


class TareaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'estado', 'fecha_creacion','descripcion')
    search_fields = ('titulo','fecha_creacion')
    list_filter = ('titulo','fecha_creacion')

admin.site.register(Tarea, TareaAdmin)

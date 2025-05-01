from django.contrib import admin
from .models import Estudiante

# usuarios/admin.py
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'rachaDias','fecha_ingreso')
    search_fields = ('nombre', 'correo')
    list_filter = ('rachaDias',)

admin.site.register(Estudiante, EstudianteAdmin)
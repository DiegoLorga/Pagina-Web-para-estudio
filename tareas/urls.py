# tareas/urls.py
from django.urls import path
from . import views

app_name = 'tareas'  # <-- esto define el namespace 'tareas'

urlpatterns = [
    path('', views.tareas_view, name='tareas_view'),
    path('crear/', views.crear_tarea, name='crear_tarea'),
    path('actualizar/<int:tarea_id>/', views.actualizar_tarea, name='actualizar_tarea'),
]



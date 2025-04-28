from django.urls import path
from . import views

urlpatterns = [
    path('usuario/<int:estudiante_id>/', views.obtener_eventos_por_usuario),
    path('desde/<str:fecha>/', views.obtener_eventos_desde_fecha),
    path('crear/', views.crear_evento),
    path('eliminar/<int:evento_id>/', views.eliminar_evento),
    path('editar/<int:evento_id>/', views.editar_evento),
]



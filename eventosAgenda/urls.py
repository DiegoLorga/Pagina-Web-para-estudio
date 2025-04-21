from django.urls import path
from . import views

urlpatterns = [
    path('agenda/', views.agenda_view, name='agenda'),
    path('api/eventos/usuario/<int:estudiante_id>/', views.obtener_eventos_por_usuario),
    path('api/eventos/desde/<str:fecha>/', views.obtener_eventos_desde_fecha),
    path('api/eventos/crear/', views.crear_evento),
    path('api/eventos/eliminar/<int:evento_id>/', views.eliminar_evento),
    path('api/eventos/editar/<int:evento_id>/', views.editar_evento),
]



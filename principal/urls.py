
from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_principal, name='menu_principal'),
    path('aumentar-racha/', views.aumentar_racha, name='aumentar_racha'), 
    path('procesar_pdf/', views.procesar_pdf, name='procesar_pdf'),
]

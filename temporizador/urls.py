# temporizador/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.timer, name='timer'),  # redirige a menú principal
]
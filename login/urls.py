from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  
    path('login/', views.login_estudiante, name='login_estudiante'),  
    path('registrar/', views.registro_estudiante, name='registrar_estudiante'),  
]
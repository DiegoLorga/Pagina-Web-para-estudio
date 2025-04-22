from . import views
from django.urls import path

urlpatterns = [   
    path('login/', views.login_view, name='login'),
    path('registrar/', views.registro_estudiante, name='registrar_estudiante'),
     path('l/', views.login_estudiante, name='login_estudiante'),
]
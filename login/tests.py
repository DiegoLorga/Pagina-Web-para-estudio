import pytest
from django.urls import reverse
from login.models import Estudiante
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password


@pytest.mark.django_db
def test_registro_estudiante(client):
    url = reverse('registrar_estudiante')
    response = client.post(url, {
        'nombre': 'Test User',
        'correo': 'test@example.com',
        'password': 'testpassword123'
    })
    
    # Asegura que fue un redirect (registro exitoso redirige)
    assert response.status_code == 302
    
    # Verifica que el estudiante fue creado
    estudiante = Estudiante.objects.get(correo='test@example.com')
    assert estudiante.nombre == 'Test User'
    assert check_password('testpassword123', estudiante.password)  # La contraseña fue hasheada y funciona

@pytest.mark.django_db
def test_login_estudiante_correcto(client):
    # Primero, crea un estudiante manualmente
    estudiante = Estudiante.objects.create(
        nombre='Login User',
        correo='login@example.com',
        password=make_password('securepassword123'),
        rachaDias=0
    )
    
    url = reverse('login_estudiante')
    response = client.post(url, {
        'correo': 'login@example.com',
        'password': 'securepassword123'
    })
    
    # Debe redirigir al 'lista_view'
    assert response.status_code == 302
    assert response.url == reverse('lista_view')

@pytest.mark.django_db
def test_login_estudiante_contraseña_incorrecta(client):
    # Crea un estudiante
    estudiante = Estudiante.objects.create(
        nombre='Bad Login User',
        correo='badlogin@example.com',
        password=make_password('rightpassword'),
        rachaDias=0
    )
    
    url = reverse('login_estudiante')
    response = client.post(url, {
        'correo': 'badlogin@example.com',
        'password': 'wrongpassword'  # contraseña incorrecta
    })

    # Debe quedarse en el login, mostrando error (no redirige)
    assert response.status_code == 200
    assert b'Error al iniciar sesi' in response.content  # Buscamos parte del mensaje de error

@pytest.mark.django_db
def test_login_estudiante_usuario_no_existente(client):
    url = reverse('login_estudiante')
    response = client.post(url, {
        'correo': 'nonexistent@example.com',
        'password': 'whatever'
    })

    # Igual, no debe redirigir, debe mostrar error
    assert response.status_code == 200
    assert b'no tiene una cuenta registrada' in response.content

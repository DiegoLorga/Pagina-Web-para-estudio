import pytest
from django.urls import reverse
from eventosAgenda.models import Agenda
from registro.models import Estudiante
from datetime import date
import json
from django.contrib.auth.hashers import make_password

@pytest.mark.django_db
def test_crear_evento(client):
    # Preparamos un estudiante porque Agenda necesita un usuario
    estudiante = Estudiante.objects.create(
        nombre='Evento Tester',
        correo='evento@example.com',
        password=make_password('password123'),
        rachaDias=0
    )
    
    url = reverse('crear_evento')
    data = {
        'usuarioid': estudiante.id,
        'titulo': 'Test Evento',
        'descripcion': 'Este es un evento de prueba',
        'fecha_evento': str(date.today()),
        'importante': True
    }
    response = client.post(url, data=json.dumps(data), content_type='application/json')
    
    assert response.status_code == 200
    response_data = response.json()
    assert 'id' in response_data
    assert Agenda.objects.filter(id=response_data['id']).exists()

@pytest.mark.django_db
def test_obtener_eventos_por_usuario(client):
    estudiante = Estudiante.objects.create(
        nombre='Evento Tester',
        correo='usuarioeventos@example.com',
        password=make_password('password123'),
        rachaDias=0
    )
    evento = Agenda.objects.create(
        usuarioid=estudiante,
        titulo='Evento del usuario',
        descripcion='Descripción evento',
        fecha_evento=date.today(),
        importante=True
    )
    
    url = reverse('obtener_eventos_por_usuario', args=[estudiante.id])
    response = client.get(url)
    
    assert response.status_code == 200
    eventos = response.json()
    assert len(eventos) == 1
    assert eventos[0]['titulo'] == 'Evento del usuario'

@pytest.mark.django_db
def test_obtener_eventos_desde_fecha(client):
    estudiante = Estudiante.objects.create(
        nombre='Fecha Tester',
        correo='fechatest@example.com',
        password=make_password('password123'),
        rachaDias=0
    )
    evento = Agenda.objects.create(
        usuarioid=estudiante,
        titulo='Evento reciente',
        descripcion='Evento creado hoy',
        fecha_evento=date.today(),
        importante=False
    )
    
    url = reverse('obtener_eventos_desde_fecha', args=[str(date.today())])
    response = client.get(url)
    
    assert response.status_code == 200
    eventos = response.json()
    assert any(e['titulo'] == 'Evento reciente' for e in eventos)

@pytest.mark.django_db
def test_editar_evento(client):
    estudiante = Estudiante.objects.create(
        nombre='Editar Tester',
        correo='editartest@example.com',
        password=make_password('password123'),
        rachaDias=0
    )
    evento = Agenda.objects.create(
        usuarioid=estudiante,
        titulo='Viejo título',
        descripcion='Vieja descripción',
        fecha_evento=date.today(),
        importante=False
    )
    
    url = reverse('editar_evento', args=[evento.id])
    data = {
        'titulo': 'Nuevo título',
        'descripcion': 'Nueva descripción',
        'fecha_evento': str(date.today()),
        'importante': True
    }
    response = client.put(url, data=json.dumps(data), content_type='application/json')
    
    assert response.status_code == 200
    evento.refresh_from_db()
    assert evento.titulo == 'Nuevo título'
    assert evento.descripcion == 'Nueva descripción'
    assert evento.importante is True

@pytest.mark.django_db
def test_eliminar_evento(client):
    estudiante = Estudiante.objects.create(
        nombre='Eliminar Tester',
        correo='eliminartest@example.com',
        password=make_password('password123'),
        rachaDias=0
    )
    evento = Agenda.objects.create(
        usuarioid=estudiante,
        titulo='Evento a eliminar',
        descripcion='Descripción de prueba',
        fecha_evento=date.today(),
        importante=False
    )
    
    url = reverse('eliminar_evento', args=[evento.id])
    response = client.delete(url)
    
    assert response.status_code == 200
    assert not Agenda.objects.filter(id=evento.id).exists()

from django.test import TestCase, Client
from django.urls import reverse
from eventosAgenda.models import Agenda
from login.models import Estudiante
from datetime import date
import json

class AgendaTests(TestCase):
    def setUp(self):
        # Se configura el cliente de pruebas y se crea un estudiante de prueba
        self.client = Client()
        self.estudiante = Estudiante.objects.create(
            nombre="Estudiante Test",
            correo="evento@test.com",
            password="1234",  # Se asume que el hash de la contraseña se gestiona en la vista
            rachaDias=0
        )
        # Se simula la sesión del usuario iniciada asignando su ID a la sesión
        session = self.client.session
        session['usuario_id'] = self.estudiante.id
        session.save()

    def test_crear_evento(self):
        # Prueba que se pueda crear un evento mediante POST
        url = reverse('crear_evento')  # URL correspondiente a la vista de creación
        data = {
            "usuarioid": self.estudiante.id,
            "titulo": "Evento Prueba",
            "descripcion": "Descripción de prueba",
            "fecha_evento": str(date.today()),  # Fecha del evento en formato string
            "importante": True
        }
        # Se envía la solicitud POST con los datos en formato JSON
        response = self.client.post(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)  # Se espera un código 200 de éxito
        self.assertIn("mensaje", response.json())  # Se verifica que la respuesta contenga un mensaje

    def test_obtener_eventos_usuario(self):
        # Se crea un evento asociado al estudiante
        Agenda.objects.create(
            usuarioid=self.estudiante,
            titulo="Evento A",
            descripcion="Descripción A",
            fecha_evento=date.today(),
            importante=False
        )
        url = reverse('obtener_eventos_usuario')  # URL de la vista que obtiene eventos
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Se espera respuesta exitosa
        self.assertEqual(len(response.json()), 1)  # Se espera un evento en la respuesta

    def test_editar_evento(self):
        # Se crea un evento y luego se envía una solicitud PUT para editarlo
        evento = Agenda.objects.create(
            usuarioid=self.estudiante,
            titulo="Viejo",
            descripcion="Antiguo",
            fecha_evento=date.today(),
            importante=False
        )
        url = reverse('editar_evento', args=[evento.id])  # URL para editar el evento específico
        data = {
            "titulo": "Nuevo título",
            "descripcion": "Actualizado",
            "fecha_evento": str(date.today()),
            "importante": True
        }
        # Se hace la solicitud PUT con datos actualizados
        response = self.client.put(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)  # Se espera que se actualice correctamente

    def test_eliminar_evento(self):
        # Se crea un evento que se eliminará
        evento = Agenda.objects.create(
            usuarioid=self.estudiante,
            titulo="Temporal",
            descripcion="Se eliminará",
            fecha_evento=date.today(),
            importante=False
        )
        url = reverse('eliminar_evento', args=[evento.id])  # URL para eliminar un evento específico
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)  # Se espera éxito al eliminar

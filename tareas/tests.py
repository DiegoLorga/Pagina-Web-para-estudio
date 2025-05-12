from django.test import TestCase, Client
from django.urls import reverse
from login.models import Estudiante
from tareas.models import Tarea
import json

class TareasViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = Estudiante.objects.create(
            nombre="Test User",
            correo="test@correo.com",
            password="123456",
            rachaDias=1
        )
        session = self.client.session
        session["usuario_id"] = self.usuario.id
        session.save()

    def test_tareas_view_autenticado(self):
        url = reverse("tareas:tareas_view")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_crear_tarea(self):
        url = reverse("tareas:crear_tarea")
        response = self.client.post(url, {
            "titulo": "Nueva tarea",
            "descripcion": "Descripción de prueba",
            "estado": 0
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Tarea.objects.filter(titulo="Nueva tarea").exists())

    def test_actualizar_tarea(self):
        tarea = Tarea.objects.create(
            usuarioid=self.usuario,
            titulo="Actualizar",
            descripcion="",
            estado=0
        )
        url = reverse("tareas:actualizar_tarea", args=[tarea.id])
        response = self.client.post(
            url,
            data=json.dumps({"estado": 1}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        tarea.refresh_from_db()
        self.assertEqual(tarea.estado, 1)

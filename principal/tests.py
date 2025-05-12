from django.test import TestCase, Client
from django.urls import reverse
from login.models import Estudiante
from unittest.mock import patch

# Pruebas para las vistas de la app 'principal'
class PrincipalViewsTest(TestCase):
    def setUp(self):
        # Se inicializa el cliente de pruebas y se crea un usuario de tipo Estudiante
        self.client = Client()
        self.estudiante = Estudiante.objects.create(
            nombre='Tester',
            correo='test@correo.com',
            password='123456',
            rachaDias=2
        )
        # Se simula una sesión autenticada almacenando el ID del estudiante
        session = self.client.session
        session['usuario_id'] = self.estudiante.id
        session.save()

    def test_menu_principal_autenticado(self):
        # Prueba que un usuario autenticado puede acceder al menú principal
        url = reverse('menu_principal')  # Obtiene la URL de la vista
        response = self.client.get(url)  # Se realiza una solicitud GET
        self.assertEqual(response.status_code, 200)  # Se espera respuesta OK
        self.assertContains(response, 'racha')  # Verifica que el contenido incluye "racha"

    def test_aumentar_racha(self):
        # Prueba que la vista para aumentar la racha funciona correctamente
        url = reverse('aumentar_racha')  # URL de la vista correspondiente
        response = self.client.post(url)  # Solicitud POST simulando acción
        self.assertEqual(response.status_code, 200)  # Se espera respuesta exitosa
        self.assertIn('racha', response.json())  # Se verifica que el JSON contiene la clave 'racha'

    @patch("principal.views.Ollama.invoke")  # Se simula el método invoke de la clase Ollama
    def test_procesar_pdf_resumen(self, mock_invoke):
        # Se simula la respuesta del modelo para la acción 'resumen'
        mock_invoke.return_value = "Este es un resumen simulado."
        url = reverse('procesar_pdf')

        # Se abre un archivo PDF de prueba y se envía como parte del formulario
        with open("principal/tests/ejemplo.pdf", "rb") as f:
            response = self.client.post(url, {
                'archivo': f,
                'accion': 'resumen'
            })

        self.assertEqual(response.status_code, 200)  # Se espera éxito
        self.assertIn("resultado", response.json())  # El JSON debe contener 'resultado'

    @patch("principal.views.Ollama.invoke")  # Se simula la llamada a Ollama para cuestionario
    def test_procesar_pdf_cuestionario(self, mock_invoke):
        # Simula la respuesta de un cuestionario JSON válido
        mock_invoke.return_value = '[{"pregunta": "¿Qué es IA?", "opciones": {"a": "Uno", "b": "Dos", "c": "Tres", "d": "Cuatro"}, "respuesta_correcta": "a"}]'
        url = reverse('procesar_pdf')

        # Envía un archivo PDF con la acción 'cuestionario'
        with open("principal/tests/ejemplo.pdf", "rb") as f:
            response = self.client.post(url, {
                'archivo': f,
                'accion': 'cuestionario'
            })

        self.assertEqual(response.status_code, 200)  # Verifica que la respuesta fue exitosa
        self.assertIn("resultado", response.json())  # Comprueba que 'resultado' está presente en el JSON

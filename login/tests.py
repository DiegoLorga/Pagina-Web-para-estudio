from django.test import TestCase, Client
from django.urls import reverse
from login.models import Estudiante
from django.contrib.auth.hashers import make_password, check_password

# Pruebas para el modelo Estudiante y el flujo de autenticación
class EstudianteTests(TestCase):
    def setUp(self):
        # Se inicializa el cliente de pruebas
        self.client = Client()

    def test_registro_estudiante(self):
        # Prueba que se pueda registrar un nuevo estudiante
        url = reverse('registrar_estudiante')  # URL de la vista de registro
        response = self.client.post(url, {
            'nombre': 'Test User',
            'correo': 'test@example.com',
            'password': 'testpassword123'
        })

        self.assertEqual(response.status_code, 302)  # Se espera redirección tras registro exitoso
        estudiante = Estudiante.objects.get(correo='test@example.com')  # Se obtiene el estudiante creado
        self.assertEqual(estudiante.nombre, 'Test User')  # Se valida el nombre
        self.assertTrue(check_password('testpassword123', estudiante.password))  # Se comprueba el hash de la contraseña

    def test_login_estudiante_correcto(self):
        # Se crea un estudiante con contraseña hasheada
        Estudiante.objects.create(
            nombre='Login User',
            correo='login@example.com',
            password=make_password('securepassword123'),
            rachaDias=0
        )

        url = reverse('login_estudiante')  # URL de la vista de login
        response = self.client.post(url, {
            'correo': 'login@example.com',
            'password': 'securepassword123'
        })

        self.assertEqual(response.status_code, 302)  # Se espera redirección tras login exitoso
        self.assertEqual(response.url, reverse('menu_principal'))  # Se verifica que redirige al menú principal

    def test_login_estudiante_contraseña_incorrecta(self):
        # Se crea un estudiante válido
        Estudiante.objects.create(
            nombre='Bad Login User',
            correo='badlogin@example.com',
            password=make_password('rightpassword'),
            rachaDias=0
        )

        url = reverse('login_estudiante')  # URL de la vista de login
        response = self.client.post(url, {
            'correo': 'badlogin@example.com',
            'password': 'wrongpassword'  # Contraseña incorrecta
        })

        self.assertEqual(response.status_code, 200)  # La vista responde con recarga (sin redirección)
        self.assertContains(response, 'Contraseña incorrecta')  # Se espera mensaje de error

    def test_login_estudiante_usuario_no_existente(self):
        # Se intenta iniciar sesión con un correo no registrado
        url = reverse('login_estudiante')
        response = self.client.post(url, {
            'correo': 'nonexistent@example.com',
            'password': 'whatever'
        })

        self.assertEqual(response.status_code, 200)  # La vista responde sin redirección
        self.assertContains(response, 'no tiene una cuenta registrada')  # Mensaje esperado en respuesta

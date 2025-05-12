from django.db import models

# Modelo que representa a un estudiante en el sistema
class Estudiante(models.Model):
    # Campo para el nombre del estudiante
    nombre = models.CharField(max_length=100)

    # Campo para el correo electrónico, debe ser único
    correo = models.EmailField(unique=True)

    # Campo para registrar la cantidad de días consecutivos de actividad
    rachaDias = models.IntegerField()

    # Campo para almacenar la contraseña (debe estar hasheada en la lógica del sistema)
    password = models.CharField(max_length=255)

    # Fecha y hora en que el estudiante fue registrado (se asigna automáticamente al crear)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    # Fecha de la última actividad del estudiante, puede quedar en blanco o nulo
    ultima_actividad = models.DateField(null=True, blank=True)

    # Representación legible del objeto cuando se imprime o se consulta desde el admin
    def __str__(self):
        return self.nombre

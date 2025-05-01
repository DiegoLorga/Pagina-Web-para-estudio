from django.db import models


class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    rachaDias = models.IntegerField()
    password = models.CharField(max_length=255)  # Para almacenar la contraseña
    fecha_ingreso = models.DateTimeField(auto_now_add=True)  # Para registrar la fecha de ingreso
    ultima_actividad = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.nombre
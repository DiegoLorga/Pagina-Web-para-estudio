
from django.db import models


class Agenda(models.Model):
    # En lugar de importar el modelo:
    usuarioid = models.ForeignKey('login.Estudiante', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    fecha_evento = models.DateField()
    importante = models.BooleanField()

    def __str__(self):
        return self.titulo

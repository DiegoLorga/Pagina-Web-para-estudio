
from django.db import models


class Tarea(models.Model):
    # En lugar de importar el modelo:
    usuarioid = models.ForeignKey('login.Estudiante', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    estado = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

from __future__ import unicode_literals

from django.db import models

class Materia(models.Model):
    anio_de_cursado = models.IntegerField(default=1) #materia de primer anio u otro
    lugar_de_dictado = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    id_calendario = models.IntegerField()

class Asistencia(models.Model):
    id_alumno = models.CharField(max_length=50)
    id_materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    latitud = models.FloatField(null = True)
    longitud = models.FloatField(null = True)

from __future__ import unicode_literals

from django.db import models

class Materia(models.Model):
    codigo = models.CharField(max_length=5, null=True)
    anio = models.IntegerField(default=1) #materia de primer anio u otro
    cuatrimestre = models.IntegerField(default=1) #materia de primer anio u otro
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, null=True)
    id_calendario = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nombre

class Asistencia(models.Model):
    id_alumno = models.CharField(max_length=50)
    id_materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    latitud = models.FloatField(null = True)
    longitud = models.FloatField(null = True)

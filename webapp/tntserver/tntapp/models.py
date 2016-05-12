from __future__ import unicode_literals

from django.db import models

class Materia(models.Model):
    anio_de_cursado = models.IntegerField(default=1) #materia de primer anio u otro
    lugar_de_dictado = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    id_calendario = models.IntegerField()

class Alumno(models.Model):
    id = models.IntegerField(primary_key=True) #hash que viene de la app en android
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField()

class AlumnoMateria(models.Model):
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    id_materia = models.ForeignKey(Materia, on_delete=models.CASCADE)

class Asistencia(models.Model):
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    id_materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    fecha = models.DateTimeField()

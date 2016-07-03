from __future__ import unicode_literals

from django.db import models

class Materia(models.Model):
    codigo = models.CharField(max_length=5, primary_key=True)
    anio = models.IntegerField(default=1) #materia de primer anio u otro
    cuatrimestre = models.IntegerField(default=1) #materia de primer anio u otro
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, null=True)
    id_calendario = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nombre

    @classmethod
    def get_calendars_url(self):
        urls = {}
        for materia in Materia.objects.all():
            urls.update({materia.codigo: materia.id_calendario})
        return urls

class Asistencia(models.Model):
    id_alumno = models.CharField(max_length=50)
    id_materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='materias')
    fecha = models.DateTimeField()
    latitud = models.FloatField(null = True)
    longitud = models.FloatField(null = True)

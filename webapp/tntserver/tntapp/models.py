# -*- coding: utf-8 -*-
from django.db import models
from django.forms.models import model_to_dict

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

    def get_meta(self):
        return '%d° Cuatrimestre - %d° Año' % (self.cuatrimestre, self.anio)

class Asistencia(models.Model):
    id_alumno = models.CharField(max_length=50)
    id_materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='materias')
    fecha = models.DateTimeField()
    latitud = models.FloatField(null = True)
    longitud = models.FloatField(null = True)

class EventoMateria(models.Model):
    id_evento = models.CharField(max_length=80, primary_key=True)
    comienzo = models.CharField(max_length=80, null=True)
    fin = models.CharField(max_length=80, null=True)
    direccion = models.CharField(max_length=80, null=True)
    titulo = models.CharField(max_length=80, null=True)
    descrip = models.CharField(max_length=80, null=True)
    se_repite = models.BooleanField()
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='eventos')
    ts_last_modified = models.DateTimeField(null=True, db_index=True)

    def __unicode__(self):
        return "Evento: %s\n" % (self.id_evento)

    def get_dict(self):
        d = model_to_dict(self)
        d['ts_last_modified'] = str(d['ts_last_modified'])
        return d

    def update(self, fields_dict):
        for field_name in self.__dict__.keys():
            if fields_dict.has_key(field_name):
                self.__dict__[field_name] = fields_dict.get(field_name)
        self.save()

    @classmethod
    def cleanup(self, eventos_actuales):
        eventos_db = [e.id_evento for e in EventoMateria.objects.all()]
        if len(eventos_db) != len(eventos_actuales):
            print "limpiando"
            for ev_id in eventos_db:
                if not ev_id in eventos_actuales:
                    EventoMateria.objects.filter(pk=ev_id).delete()
                    #print str(ev_id) + ' no estaba en: ' + str(eventos_actuales)

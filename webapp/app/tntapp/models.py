# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.forms.models import model_to_dict
from django.utils.dateparse import parse_datetime
from datetime import datetime

class Materia(models.Model):
    codigo = models.CharField(max_length=5, primary_key=True)
    anio = models.IntegerField(default=1) #materia de primer anio u otro
    cuatrimestre = models.IntegerField(default=1) #materia de primer anio u otro
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, null=True)
    id_calendario = models.CharField(max_length=100)

    @classmethod
    def get_calendars_url(self):
        urls = {}
        for materia in Materia.objects.all():
            urls.update({materia.codigo: materia.id_calendario})
        return urls

    def get_meta(self):
        return '%d° Cuatrimestre - %d° Año' % (self.cuatrimestre, self.anio)

    def __unicode__(self):
        return self.nombre

    def filter_events(self, params):
        eventos = self.eventos.all()
        if params['es_hoy'][0] == 'true':
            eventos = filter(lambda e: e.es_hoy(), eventos)
        if params['en_curso'][0] == 'true':
            eventos = filter(lambda e: e.en_curso(), eventos)
        if params['tipo_evento'][0] != u'Todos':
            titulo = params['tipo_evento'][0].lower()
            eventos = filter(lambda e: titulo in e.titulo.encode('utf8').lower(), eventos)
        return eventos

class Asistencia(models.Model):
    id_alumno = models.CharField(max_length=50)
    id_materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='asistencias')
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

    @classmethod
    def cleanup(self, eventos_actuales):
        """ Verifica si la lista de eventos de google calendar tiene menos
            eventos que la local y si es asi, elimina los eventos locales que no
            existan en google calendar.
        """
        eventos_db = [e.id_evento for e in EventoMateria.objects.all()]
        if len(eventos_db) != len(eventos_actuales):
            for ev_id in eventos_db:
                if not ev_id in eventos_actuales:
                    EventoMateria.objects.filter(pk=ev_id).delete()
                    #print str(ev_id) + ' no estaba en: ' + str(eventos_actuales)

    @classmethod
    def update_events(self, eventos, materia_id):
        """
            Verifica si los eventos de una materia fueron modificados en
            google calendar y actualiza la informacion local.
        """
        for event in eventos:
            defaults = {'comienzo' : event['DTSTART'].dt,
                        'fin'       : event['DTEND'].dt,
                        'direccion' : unicode(event['LOCATION']),
                        'titulo'    : unicode(event['SUMMARY']),
                        'descrip'   : unicode(event['DESCRIPTION']),
                        'se_repite' : True if event.has_key('RRULE') else False,
                        'ts_last_modified': event['LAST-MODIFIED'].dt,
                        'materia_id': materia_id }

            ev_materia, created = EventoMateria.objects.get_or_create(
                id_evento = str(event['UID']),
                defaults  = defaults
            )
            if ev_materia:
                if event['LAST-MODIFIED'].dt > ev_materia.ts_last_modified:
                    ev_materia.update(defaults)

    def __unicode__(self):
        return "Evento: %s\n" % (self.id_evento)

    def get_dict(self):
        d = model_to_dict(self)
        d['ts_last_modified'] = str(d['ts_last_modified'])
        return d

    def update(self, fields_dict):
        """
            Actualiza los datos de una instancia de EventoMateria
        """
        for field_name in self.__dict__.keys():
            if fields_dict.has_key(field_name):
                self.__dict__[field_name] = fields_dict.get(field_name)
        self.save()

    def en_curso(self, fecha_actual=None):
        if fecha_actual:
            fecha_actual = fecha_actual.replace(tzinfo=None)
        else:
            fecha_actual = datetime.now().replace(tzinfo=None)
        comienzo = parse_datetime(self.comienzo).replace(tzinfo=None)
        fin = parse_datetime(self.fin).replace(tzinfo=None)
        result = False
        print "fecha_actual", fecha_actual
        print "comienzo", comienzo
        if self.se_repite:
            if comienzo.weekday() == fecha_actual.weekday():
                result = self.en_curso_ahora(fecha_actual)
        else:
            print "verificando si es hoy"
            if self.es_hoy():
                print "verificando si esta en curso ahora"
                result = self.en_curso_ahora(fecha_actual)
        return result

    def en_curso_ahora(self, fecha_actual=None):
        if fecha_actual:
            fecha_actual = fecha_actual.replace(tzinfo=None)
        else:
            fecha_actual = datetime.now().replace(tzinfo=None)
        comienzo = parse_datetime(self.comienzo).replace(tzinfo=None)
        fin = parse_datetime(self.fin).replace(tzinfo=None)
        if fecha_actual >= comienzo and fecha_actual <= fin:
            return True
        else:
            return False

    def es_hoy(self, fecha_actual=None):
        if fecha_actual:
            fecha_actual = fecha_actual.replace(tzinfo=None)
        else:
            fecha_actual = datetime.now().replace(tzinfo=None)
        comienzo = parse_datetime(self.comienzo).replace(tzinfo=None)
        delta = fecha_actual - comienzo
        diferencia_dias = abs(delta.days)
        print diferencia_dias
        return diferencia_dias == 0

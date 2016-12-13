# -*- coding: utf-8 -*-
import datetime
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from channels import Group
from rest_framework import viewsets
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from urlparse import parse_qs, urlparse
import itertools

# Nuestra app
from .serializers import *
from .models import *

# Google calendar interaction
import json
import urllib2
import threading
from icalendar import Calendar

events_id = []
new_content = False
deleted_content = False

class MateriaList(ListView):
    model = Materia
    #para sobreescribir ubicacion y nombre de template por defecto
    def get_template_names(self):
            return ['tntapp/listado_materias.html']

    def get_context_data(self, **kwargs):
        context = super(MateriaList, self).get_context_data(**kwargs)
        context['materias'] = Materia.objects.all()
        return context

class MateriaCreation(CreateView):
    model = Materia
    success_url = reverse_lazy('materias:list')
    fields = ['nombre', 'lugar_de_dictado', 'anio_de_cursado', 'id_calendario']

class MateriaUpdate(UpdateView):
    model = Materia
    success_url = reverse_lazy('materias:list')
    fields = ['nombre', 'lugar_de_dictado', 'anio_de_cursado', 'id_calendario']

class MateriaDelete(DeleteView):
    model = Materia
    success_url = reverse_lazy('materias:list')

def verMapa(request):
    asis = Asistencia.objects.all()
    return render(request, "verMapa/maps.html",{'asistencias': asis})

#Rehacer
def verMapaDia(request, dia):
    ahora = datetime.date.today()
    return render(request, "verMapa/maps.html",{'asistencias': asis})

class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer

class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer

def update_events(request):
    if not request.is_ajax():
        return HttpResponse('')
    params = parse_params(request.META["QUERY_STRING"])
    mesas = Materia.objects.filter(nombre__icontains="Exámen")
    materias = get_materias()
    materias = list(itertools.chain(materias, mesas))
    eventos = get_eventos(materias, params)
    html = render_to_string('tntapp/scroll-list-content.html',
            {'materias': materias,
            'eventos':eventos,
            'notifications': False})
    return HttpResponse(html)

def search_events(request):
    if not request.is_ajax():
        return HttpResponse('')
    params = parse_params(request.META["QUERY_STRING"])
    if len(params['termino']) > 0:
        mesas = Materia.objects.filter(nombre__icontains="Exámen", descripcion__icontains=params['termino'][0])
        materias = get_materias().filter(nombre__icontains=params['termino'][0])
        materias = list(itertools.chain(materias, mesas))
    else:
        materias = get_materias()
    eventos = get_eventos(materias, params)
    html = render_to_string('tntapp/scroll-list-content.html',
                            {'materias': materias,
                            'notifications': False,
                            'eventos':eventos})
    return HttpResponse(html)

def get_materias():
    """ Prefiltrado de materias por cuatrimestre.
        Devuelve las del cuatrimestre actual
    """
    mes_actual = datetime.now().month
    cuatrimestre_actual = 1 if mes_actual < 8 else 2
    return Materia.objects.filter(cuatrimestre=cuatrimestre_actual)

def parse_params(query_string):
    result = parse_qs(query_string, keep_blank_values=True)
    return result

def get_eventos(materias_qset, params):
    """
        Devuelve una lista con los eventos de las materias indicadas y
        con los filtros indicados en params
    """
    materias = filter(lambda m: len(m.eventos.all()) > 0, materias_qset)
    eventos = []
    for m in materias:
        eventos.extend(m.filter_events(params))
    return eventos

#La siguiente vista no lleva url
def watch_calendars_view(urls):
    global events_id, deleted_content
    events_id = []
    threads = []
    for materia_id, url in urls.iteritems():
        args = (url, materia_id)
        threads.append(threading.Thread(target=parse_data, args=args))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    deleted_content = EventoMateria.cleanup(events_id)


def parse_data(ics_url, materia):
    global events_id, new_content
    base_url = "https://calendar.google.com/calendar/ical/{}/public/basic.ics"
    ics_file = urllib2.urlopen(base_url.format(ics_url))
    gcal = Calendar.from_ical(unicode(ics_file.read(), 'UTF-8'))
    eventos = [e for e in gcal.walk('vevent')]
    events_id.extend([e['UID'] for e in eventos])
    if len(eventos) > 0:
        new_content = EventoMateria.update_events(eventos, materia)
    ics_file.close()


@receiver(post_save, sender=Asistencia)
@receiver(post_save, sender=EventoMateria)
@receiver(post_delete, sender=EventoMateria)
def push_notification(**kwargs):
    """Envia una notificacion al cliente para que refresque la lista de eventos
        cuando hay novedades en Google Calendar y
        consecuentemente a nivel local, es decir, avisa a los usuarios si:
            - Se crea un evento
            - Se modifica un evento
            - Se elimina un evento
    """
    notification = {
        "text": json.dumps({'user_need_refresh': 1}),
    }
    Group("notifications").send(notification)

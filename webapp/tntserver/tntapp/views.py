# -*- coding: utf-8 -*-
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from rest_framework import viewsets

# Nuestra app
from .serializers import *
from .models import *
from .utils import *

# Google calendar interaction
import urllib2
import threading
from icalendar import Calendar

events_id = []

def calendarios(request):
    materias = Materia.objects.all()
    return render(request, "calendarios.html",{'materias': materias})

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

#La siguiente vista no lleva url
def watch_calendars_view(urls):
    global events_id
    events_id = []
    threads = []
    for materia_id, url in urls.iteritems():
        args = (url, materia_id)
        threads.append(threading.Thread(target=parse_data, args=args))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    EventoMateria.cleanup(events_id)

#La siguiente vista no lleva url
def parse_data(ics_url, materia):
    global events_id
    base_url = "https://calendar.google.com/calendar/ical/{}/public/basic.ics"
    ics_file = urllib2.urlopen(base_url.format(ics_url))
    gcal = Calendar.from_ical(unicode(ics_file.read(), 'UTF-8'))
    eventos = [e for e in gcal.walk('vevent')]
    events_id.extend([e['UID'] for e in eventos])
    if len(eventos) > 0:
        EventoMateria.update_events(eventos, materia)
    ics_file.close()

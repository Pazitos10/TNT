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

# Nuestra app
from .serializers import *
from .models import *
from .utils import *

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
    html = ''
    if request.is_ajax():
        materias = Materia.objects.all()
        html = render_to_string('tntapp/scroll-list-content.html', {'materias': materias, 'notifications': False})
    return HttpResponse(html)

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
    #print "new?:%s deleted?:%s" % (str(new_content), str(deleted_content))
    deleted_content = EventoMateria.cleanup(events_id)
    # print "new? %s , deleted? %s" % (str(new_content),str(deleted_content))
    # if new_content or deleted_content:
    #     print "llamando a push"
    #     push_notification()

#La siguiente vista no lleva url
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

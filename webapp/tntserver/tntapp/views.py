from __future__ import print_function
from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Materia
from django.core import serializers
from .models import Asistencia
import datetime
from rest_framework import viewsets
from .serializers import *

#Google Calendar
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'tntserver'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credential_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) +  "/tntserver/" #os.path.join(home_dir, '.credentials')
    #print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'client_secret.json')

    print("busco credenciales de " + credential_path)

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def sincronizarConCalendario(request):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    calendarios = service.calendarList().list().execute()
    calendarios = calendarios.values()
    for c in calendarios:
        print(c)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='q4sjke29116cd0ld3275p9ch9g@group.calendar.google.com', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    eventos =[]
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        eventos.append((start, event['summary']))

    return render(request, "tntapp/calendarios.html",{'eventos': eventos, 'calendarios': calendarios})



class MateriaList(ListView):
    model = Materia
    #para sobreescribir ubicacion y nombre de template por defecto
    def get_template_names(self):
            return ['tntapp/listado_materias.html']

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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import datetime

from .serializers import *
from .models import *
from .utils import *


def index(request):
    calendarios_data = fetch_calendarios()
    return render(request, "calendarios.html",
                {'calendarios': calendarios_data})

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

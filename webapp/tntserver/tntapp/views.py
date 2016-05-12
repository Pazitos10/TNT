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


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class MateriaList(ListView):
    model = Materia

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

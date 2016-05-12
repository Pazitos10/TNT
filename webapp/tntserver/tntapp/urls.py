from django.conf.urls import url

from .views import *

urlpatterns = [
    #url(r'^$', index, name='index'),
    url(r'^$', MateriaList.as_view(), name='list'),
    url(r'^nuevo$', MateriaCreation.as_view(), name='new'),
    url(r'^editar/(?P<pk>\d+)$', MateriaUpdate.as_view(), name='edit'),
    url(r'^borrar/(?P<pk>\d+)$', MateriaDelete.as_view(), name='delete'),

]

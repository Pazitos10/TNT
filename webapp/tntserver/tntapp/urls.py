from django.conf.urls import url, include
from .views import *
from rest_framework import routers
from tntapp import views


router = routers.DefaultRouter()
router.register(r'asistencia', views.AsistenciaViewSet)
router.register(r'materia', views.MateriaViewSet)

urlpatterns = [
    #url(r'^$', index, name='index'),
    url(r'^$', MateriaList.as_view(), name='list'),
    url(r'^nuevo$', MateriaCreation.as_view(), name='new'),
    url(r'^editar/(?P<pk>\d+)$', MateriaUpdate.as_view(), name='edit'),
    url(r'^borrar/(?P<pk>\d+)$', MateriaDelete.as_view(), name='delete'),
    url(r'^mapa$', verMapa, name='mapa'),
    url(r'^api/', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]

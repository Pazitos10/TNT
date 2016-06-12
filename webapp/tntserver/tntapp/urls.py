from django.conf.urls import url, include
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'asistencia', AsistenciaViewSet)
router.register(r'materia', MateriaViewSet)

urlpatterns = [
    url(r'^$', MateriaList.as_view(), name='list'),
    url(r'^sync$', sincronizarConCalendario, name='sync'),
    url(r'^nuevo$', MateriaCreation.as_view(), name='new'),
    url(r'^editar/(?P<pk>\d+)$', MateriaUpdate.as_view(), name='edit'),
    url(r'^borrar/(?P<pk>\d+)$', MateriaDelete.as_view(), name='delete'),
    url(r'^mapa$', verMapa, name='mapa'),
    url(r'^api/', include(router.urls)),
    url(r'^calendarios/$', calendarios, name='calendarios'),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]

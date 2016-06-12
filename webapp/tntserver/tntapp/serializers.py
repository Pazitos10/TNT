from .models import Materia, Asistencia
from rest_framework import serializers


class MateriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Materia
        fields = ('anio_de_cursado', 'lugar_de_dictado', 'nombre', 'id_calendario')

class AsistenciaSerializer(serializers.HyperlinkedModelSerializer):
    materias = serializers.PrimaryKeyRelatedField(queryset=Materia.objects.all())

    class Meta:
        model = Asistencia
        fields = ('id_alumno', 'materias','fecha', 'latitud', 'longitud')

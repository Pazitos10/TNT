from .models import Materia, Asistencia
from rest_framework import serializers


class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = ('codigo', 'nombre', 'anio', 'cuatrimestre', 'descripcion', 'id_calendario')

class AsistenciaSerializer(serializers.ModelSerializer):
    materias = MateriaSerializer(many=True, read_only=True)

    class Meta:
        model = Asistencia
        fields = ('id_alumno','fecha', 'materias', 'latitud', 'longitud', 'id_materia')

    def create(self, validated_data):
        asistencia = Asistencia.objects.create(**validated_data)
        asistencia.save()
        return asistencia

from django.test import TestCase

# Create your tests here.
from tntapp.models import Materia, EventoMateria
from datetime import tzinfo, timedelta, datetime

ZERO = timedelta(0)
HOUR = timedelta(hours=1)

class FixedOffset(tzinfo):
    """Fixed offset in minutes east from UTC."""
    def __init__(self, offset, name):
        self.__offset = timedelta(minutes = offset)
        self.__name = name

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name
    def dst(self, dt):
        return ZERO


class EventoMateriaCase(TestCase):

    def setUp(self):
        UTC = FixedOffset(0, 'UTC')
        Argentina = FixedOffset(-3*60, 'UTC-3')
        self.timestamp = datetime.now(UTC).astimezone(Argentina)
        materia = Materia.objects.create(codigo = "IF050",
                                        nombre = "MateriaTest",
                                        id_calendario = "asdasdasd")

        self.evento_no_hoy = EventoMateria.objects.create(
            id_evento = "asdasd@google.com",
            comienzo = str(self.timestamp.replace(day=self.timestamp.day+2)) ,
            fin = str(self.timestamp.replace(day=self.timestamp.day+2)),
            se_repite = True,
            materia = materia,
            ts_last_modified = "2016-07-03 22:31:17")

        self.evento_hoy_no_ahora = EventoMateria.objects.create(
            id_evento = "asdasq9@google.com",
            comienzo = str(self.timestamp.replace(hour=self.timestamp.hour+3)),
            fin = str(self.timestamp.replace(hour=self.timestamp.hour+6)),
            se_repite = True,
            materia = materia,
            ts_last_modified = "2016-07-03 22:31:17")

        self.evento_hoy_ahora = EventoMateria.objects.create(
            id_evento = "asdasw@google.com",
            comienzo = str(self.timestamp.replace(hour=self.timestamp.hour-1)),
            fin = str(self.timestamp.replace(hour=self.timestamp.hour+1)),
            se_repite = True,
            materia = materia,
            ts_last_modified = "2016-07-03 22:31:17")

    def test_evento_no_hoy_no_en_curso(self):
        self.assertEqual(
            self.evento_no_hoy.en_curso(fecha_actual=self.timestamp), False)

    def test_evento_hoy_en_curso(self):
        self.assertEqual(
            self.evento_hoy_ahora.en_curso(fecha_actual=self.timestamp), True)

    def test_evento_hoy_no_en_curso(self):
        self.assertEqual(
            self.evento_hoy_no_ahora.en_curso(fecha_actual=self.timestamp), False)

    def test_evento_es_hoy(self):
        self.assertEqual(self.evento_hoy_no_ahora.es_hoy(fecha_actual=self.timestamp), True)

    def test_evento_no_es_hoy(self):
        self.assertEqual(self.evento_no_hoy.es_hoy(fecha_actual=self.timestamp), False)

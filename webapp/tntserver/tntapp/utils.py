import json
import urllib2
import datetime
from icalendar import Calendar, Event, vDatetime

def get_simple_events(eventos):
    """
        Retorna una lista de eventos, donde cada uno de ellos
        contiene al menos los siguientes datos:
            comienzo: dia/hora de inicio del evento
            fin: dia/hora de fin del evento
            direccion: ubicacion geografica del evento
            resumen: titulo del evento
            descripcion: los datos necesarios para confeccionar la info de
                las materias. A saber:
                    Aula: '(numero de aula | msg: "a designar")'
                    Lugar: '(CC|Edificio Aulas)'
                    Profesor: listado con el formato
                                Apellido, nombres[; Apellido Nombres ...]
    """
    event_list = []
    for event in eventos:
        #print event
        simple_event = {
            'comienzo'  : str(event['DTSTART'].dt),
            'fin'       : str(event['DTEND'].dt),
            'direccion' : unicode(event['LOCATION']),
            'titulo'    : unicode(event['SUMMARY']),
            'descrip'   : unicode(event['DESCRIPTION']),
            'se_repite' : True if event.has_key('RRULE') else False
        }
        event_list.append(simple_event)
    return event_list

def fetch_calendarios():
    CHARSET = 'UTF-8'
    base_url = "https://calendar.google.com/calendar/ical/{}@group.calendar.google.com/public/basic.ics"
    # ics_urls = {
    #     "RTxDatos"  : "db46rsturhg72kaon3bkjtp638",
    #     "TNT"       : "q4sjke29116cd0ld3275p9ch9g"
    #     "AyP-II"    : "nubkn5itvfi3n25bpv0mkgps84",
    #     "AyG"       : "h2hpa8j9ndn3kinjqvchtkgr64"
    # }
    ics_urls = {"TNT": "1dgvl4utp25atd5s3nj9dfkbn8", "AW": "4rlbiggjp3u4k2cr1bvcsk5mi4"} #calendars -> bruno
    calendarios_data = []
    calendarios_events = []
    for materia, ics_url in ics_urls.iteritems():
        inicio_lectura = datetime.datetime.now()
        print "[%s] inicio lectura: %s\n" % (str(inicio_lectura), ics_url)
        ics_file = urllib2.urlopen(base_url.format(ics_url))
        gcal = Calendar.from_ical(unicode(ics_file.read(), CHARSET))
        meta = gcal.walk('vcalendar')[0]['X-WR-CALDESC']
        events = get_simple_events([e for e in gcal.walk('vevent')])
        calendarios_events.append({materia: events})
        calendarios_data.append({materia: meta})
        ics_file.close()
        fin_lectura = datetime.datetime.now()
        delta = fin_lectura - inicio_lectura
        print "[%s] fin lectura: %s - Delta: %s\n" % (str(fin_lectura), ics_url , str(delta))
    return zip(calendarios_events, calendarios_data)

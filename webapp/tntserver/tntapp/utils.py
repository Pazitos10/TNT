#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sqlite3
import urllib2
import datetime
from icalendar import Calendar, Event, vDatetime
import threading
import Queue

calendarios_data = []
calendarios_events = []

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

def fetch_calendarios(ics_urls):
    global calendarios_data, calendarios_events
    calendarios_data = []
    calendarios_events = []
    fetch_parallel(ics_urls)
    result = zip(calendarios_events, calendarios_data)
    print result
    print "From calendar.google"
    #corregir el modo de apendear a las listas
    return result


def parse_data(ics_url, materia, queue):
    global calendarios_data, calendarios_events
    CHARSET = 'UTF-8'
    base_url = "https://calendar.google.com/calendar/ical/{}/public/basic.ics"
    #ics_urls = {"TNT": "1dgvl4utp25atd5s3nj9dfkbn8", "AW": "4rlbiggjp3u4k2cr1bvcsk5mi4"} #calendars -> bruno
    #inicio_lectura = datetime.datetime.now()
    #print "[%s] inicio lectura: %s\n" % (str(inicio_lectura), ics_url)
    ics_file = urllib2.urlopen(base_url.format(ics_url))
    gcal = Calendar.from_ical(unicode(ics_file.read(), CHARSET))
    meta = gcal.walk('vcalendar')[0]['X-WR-CALDESC']
    events = get_simple_events([e for e in gcal.walk('vevent')])
    calendarios_events.append({materia: events})
    calendarios_data.append({materia: meta})
    #fin_lectura = datetime.datetime.now()
    ics_file.close()
    #delta = fin_lectura - inicio_lectura
    #print "[%s] fin lectura: %s - Delta: %s\n" % (str(fin_lectura), ics_url , str(delta))

    #queue.put(zip(calendarios_events, calendarios_data))


def materias_json_to_sqlite():
    materias = json.load(open('../materias.json'))
    db = sqlite3.connect("../db.sqlite3")
    columnas = map(lambda nombre: str(nombre), materias[0].keys())
    str_col = "(" + ",".join(columnas) + ")"
    query = 'insert into tntapp_materia '+ str_col + ' values (?,?,?,?,?,?)'
    for materia in materias:
        c = db.cursor()
        c.execute(query, materia.values())
        c.execute("select * from tntapp_materia")
        print c.fetchall()
        db.commit()
        c.close()

def fetch_parallel(urls):
    result = Queue.Queue()
    threads = [threading.Thread(target=parse_data, args = (url, materia, result)) for materia, url in urls.iteritems()]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return result

def queue_get_all(q):
    items = []
    maxItemsToRetreive = 10
    for numOfItemsRetrieved in range(0, maxItemsToRetreive):
        try:
            if numOfItemsRetrieved == maxItemsToRetreive:
                break
            items.append(q.get_nowait())
        except Empty, e:
            break
    return items
#if __name__=='__main__':
    #materias_json_to_sqlite()

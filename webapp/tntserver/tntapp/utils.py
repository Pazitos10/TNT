#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sqlite3
import urllib2
import datetime
from icalendar import Calendar, Event, vDatetime
import threading
import Queue
from models import Materia

calendarios_data = []
calendarios_events = []
BASE_ICS_URL = "https://calendar.google.com/calendar/ical/{}/public/basic.ics"

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

def get_meta(materia):
    meta = {
        'nombre': materia.nombre,
        'cuatrimestre': materia.cuatrimestre,
        'anio': materia.anio
    }
    return meta

def fetch_calendarios(ics_urls):
    global calendarios_data, calendarios_events
    calendarios_data = []
    calendarios_events = []
    fetch_parallel(ics_urls)
    result = zip(calendarios_events, calendarios_data)
    #corregir el modo de apendear a las listas
    return result


def parse_data(ics_url, materia, queue):
    global calendarios_data, calendarios_events
    ics_file = urllib2.urlopen(BASE_ICS_URL.format(ics_url))
    gcal = Calendar.from_ical(unicode(ics_file.read(), 'UTF-8'))
    materia_obj = Materia.objects.filter(codigo=materia).first()
    meta = get_meta(materia_obj) #gcal.walk('vcalendar')[0]['X-WR-CALDESC']
    events = get_simple_events([e for e in gcal.walk('vevent')])
    calendarios_events.append({materia: events})
    calendarios_data.append({materia: meta})
    ics_file.close()


def feed_db():
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

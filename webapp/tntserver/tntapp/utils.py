#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sqlite3
import urllib2
import datetime
import threading
from icalendar import Calendar
from models import Materia, EventoMateria

BASE_ICS_URL = "https://calendar.google.com/calendar/ical/{}/public/basic.ics"
events_id = []

def update_events(eventos, materia_id):
    """
        Verifica si los eventos de una materia fueron modificados en
        google calendar y actualiza la informacion local.
    """
    global events_id
    for event in eventos:
        events_id.append(str(event['UID']))
        defaults = {'comienzo' : event['DTSTART'].dt,
                    'fin'       : event['DTEND'].dt,
                    'direccion' : unicode(event['LOCATION']),
                    'titulo'    : unicode(event['SUMMARY']),
                    'descrip'   : unicode(event['DESCRIPTION']),
                    'se_repite' : True if event.has_key('RRULE') else False,
                    'ts_last_modified': event['LAST-MODIFIED'].dt,
                    'materia_id': materia_id }

        ev_materia, created = EventoMateria.objects.get_or_create(
            id_evento = str(event['UID']),
            defaults  = defaults
        )
        if ev_materia:
            if event['LAST-MODIFIED'].dt > ev_materia.ts_last_modified:
                ev_materia.update(defaults)
                print "Evento " + str(event['UID']) +" materia: "+ materia_id +" fue modificado!"
        else:
            print "Evento " + str(event['UID']) +" materia: "+ materia_id +" creado!"

def fetch_calendarios(urls):
    global events_id
    events_id = []
    threads = [threading.Thread(target=parse_data, args = (url, materia_id)) for materia_id, url in urls.iteritems()]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    EventoMateria.cleanup(events_id)

def parse_data(ics_url, materia):
    ics_file = urllib2.urlopen(BASE_ICS_URL.format(ics_url))
    gcal = Calendar.from_ical(unicode(ics_file.read(), 'UTF-8'))
    eventos = [e for e in gcal.walk('vevent')]
    if len(eventos) > 0:
        events_id = update_events(eventos, materia)
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

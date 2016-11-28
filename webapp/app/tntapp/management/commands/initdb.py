# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import json
import sqlite3

class Command(BaseCommand):
    help = 'Carga inicial para la tabla Materia'

    def add_arguments(self, parser):
        parser.add_argument('--src',
                    help="""Especifica de donde se obtienen los datos.
                            El archivo debe tener extension json""",
                    default='materias.json')
        parser.add_argument('--db',
                    help="""Especifica el path a la base de datos sqlite3
                        donde residiran los datos cargados""",
                    default='db.sqlite3')

    def handle(self, *args, **options):
        try:
            json_path = str(options['src'])
            db_path = str(options['db'])
            materias = json.load(open(json_path))
            db = sqlite3.connect(db_path)
            columnas = map(lambda nombre: str(nombre), materias[0].keys())
            str_col = "(" + ",".join(columnas) + ")"
            query = 'insert into tntapp_materia '+ str_col + ' values (?,?,?,?,?,?)'
            for materia in materias:
                c = db.cursor()
                c.execute(query, materia.values())
                db.commit()
                c.close()
            self.stdout.write(self.style.SUCCESS('Datos cargados exitosamente!'))
        except Exception as e:
            raise CommandError(u'[InitDB] Algo salió mal - %s ' % e)

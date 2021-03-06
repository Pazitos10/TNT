# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-16 20:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tntapp', '0002_auto_20160527_1234'),
    ]

    operations = [
        migrations.RenameField(
            model_name='materia',
            old_name='anio_de_cursado',
            new_name='anio',
        ),
        migrations.RemoveField(
            model_name='materia',
            name='lugar_de_dictado',
        ),
        migrations.AddField(
            model_name='materia',
            name='codigo',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='materia',
            name='cuatrimestre',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='materia',
            name='descripcion',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='materia',
            name='id_calendario',
            field=models.CharField(max_length=100),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-17 00:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tntapp', '0003_auto_20160616_2016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materia',
            name='id',
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='id_materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materias', to='tntapp.Materia'),
        ),
        migrations.AlterField(
            model_name='materia',
            name='codigo',
            field=models.CharField(max_length=5, primary_key=True, serialize=False),
        ),
    ]

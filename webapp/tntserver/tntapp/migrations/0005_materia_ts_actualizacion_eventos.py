# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-04 03:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tntapp', '0004_auto_20160617_0048'),
    ]

    operations = [
        migrations.AddField(
            model_name='materia',
            name='ts_actualizacion_eventos',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 4, 3, 1, 56, 940110, tzinfo=utc)),
        ),
    ]

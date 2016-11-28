from __future__ import absolute_import
from celery import shared_task
from .views import watch_calendars_view
from .models import Materia

@shared_task
def watch_calendars_task():
    urls = Materia.get_calendars_url()
    watch_calendars_view(urls)

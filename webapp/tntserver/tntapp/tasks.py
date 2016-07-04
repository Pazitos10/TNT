from __future__ import absolute_import
from celery import shared_task
from .utils import fetch_calendarios

@shared_task
def fetch_async(urls):
    fetch_calendarios(urls)

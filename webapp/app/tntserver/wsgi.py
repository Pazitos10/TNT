"""
WSGI config for tntserver project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import sys

if hasattr(sys, 'real_prefix'):
    if hasattr(sys, 'prefix'):
        print 'dentro de un virtualenv'
    else:
        print 'fuera de un virtualenv'
else:
    print 'fuera de un virtualenv'
#application = get_wsgi_application()
application = Cling(get_wsgi_application())

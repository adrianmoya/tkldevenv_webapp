import os
import sys

path = '/opt'
if path not in sys.path:
        sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'tkldevenv-webapp.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

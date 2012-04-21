import os
import sys

from django.core.handlers.wsgi import WSGIHandler

os.environ['DJANGO_SETTINGS_MODULE'] = 'halal.settings'
application = WSGIHandler()

from django.conf import settings

if settings.DEBUG:
    import wsgi_monitor
    wsgi_monitor.start(interval=1.0)

    from werkzeug.debug import DebuggedApplication
    application = DebuggedApplication(application, evalex=True)

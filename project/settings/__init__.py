"""Settings package entrypoint.

By default we expose development settings so existing references to
`DJANGO_SETTINGS_MODULE='project.settings'` continue to work for manage.py,
ASGI/WSGI, tests, and scripts.

In production (e.g. Docker/hosting) you should instead point
`DJANGO_SETTINGS_MODULE` at `project.settings.production`.
"""

from .development import *  # noqa

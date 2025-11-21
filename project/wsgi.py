"""
WSGI config for dog_dating_project project.
"""

import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
application = get_wsgi_application()

if settings.MEDIA_ROOT:
    application = WhiteNoise(
        application,
        root=str(settings.MEDIA_ROOT),
        prefix=settings.MEDIA_URL,
    )

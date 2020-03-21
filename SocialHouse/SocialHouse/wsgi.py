"""
WSGI config for SocialHouse project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SocialHouse.settings.dev')

application = get_wsgi_application()

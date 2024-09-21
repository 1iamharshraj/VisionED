# celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VisionED.settings')

app = Celery('VisionED')

# Using a string here means the worker will not need to pickle the object
app.config_from_object('django.conf:settings', namespace='CELERY')


# Load task modules from all registered Django app configs
app.autodiscover_tasks()
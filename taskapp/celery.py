from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tooltip_analytics.settings_production')

app = Celery('tooltip_analytics')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()



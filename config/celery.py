"""
Celery configuration for Investment Platform project.
"""

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('investment_platform')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

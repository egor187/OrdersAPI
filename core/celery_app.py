from __future__ import absolute_import

from celery import Celery


app = Celery('core', broker='redis://localhost:6379')
app.config_from_object('settings.settings', namespace='CELERY')
app.autodiscover_tasks()

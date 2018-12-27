from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from navel import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'navel.settings')

app = Celery('navel', backend='redis://localhost', broker='redis://localhost')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

app.conf.beat_schedule = {
    'update-stock-info at 15:30': {
        'task': 'storage.tasks.update_all',
        'schedule': crontab(hour=15, minute=30, day_of_week='mon-fri'),
        'args': ()
    },
}

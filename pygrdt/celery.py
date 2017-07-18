from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pygrdt.settings')

app = Celery('pygrdt')

app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    'run-nasdaq-scraper': {
        'task': 'analysisportal.tasks.scrapeNasdaqWebsite',
        # Execute every hour between 3pm and 9pm on weekdays only
        #'schedule': crontab(), # for testing
        'schedule': crontab(hour='*/1,15-21', day_of_week='mon,tue,wed,thu,fri'), # for production
    },
    'add-every-monday-morning': {
        'task': 'analysisportal.tasks.add',
        'schedule': crontab(),
        'args': (16, 16),
    },
}


app.autodiscover_tasks()
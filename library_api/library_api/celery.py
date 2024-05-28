# library_api/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_api.settings')

app = Celery('library_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-daily-emails': {
        'task': 'library.tasks.send_daily_emails',
        'schedule': crontab(hour=6, minute=35)  #8:00 AM everyday
    },
    # "print_time":{
    #     "task": 'library.tasks.print_time',
    #     'schedule':timedelta(seconds=1)
    # }
}

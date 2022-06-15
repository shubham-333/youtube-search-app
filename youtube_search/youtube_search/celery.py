from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_search.settings')

app = Celery('youtube_search')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

# CELERY BEAT SETTINGS

@app.task(bing=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogapiproject.settings')

app = Celery('blogapiproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

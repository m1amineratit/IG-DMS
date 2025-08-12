import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insta_dm_bot.settings')
app = Celery('insta_dm_bot')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()



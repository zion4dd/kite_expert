# RUN: celery -A kite_expert worker --loglevel=info --pool=solo
# RUN: celery -A kite_expert flower # URL: localhost:5555

from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kite_expert.settings')

celery_app = Celery('celery_tasks')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()


# @celery_app.task
# def task_celery_app():
#     pass

# Periodic tasks
# https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html

# from celery.schedules import crontab

# celery_app.conf.beat_schedule = {
#     # Executes every Monday morning at 7:30 a.m.
#     'add-every-monday-morning': {
#         'task': 'kites.tasks.resize_photo_kite',
#         'schedule': crontab(hour=7, minute=30, day_of_week=1),
#         'args': (16, 16),
#     },
# }
# 
# RUN: celery -A kite_expert beat -l info OR celery -A kite_expert worker -B -l info

# RUN celery -A kite_expert.celery:celery_app worker --loglevel=info --pool=solo
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kite_expert.settings')
celery_app = Celery('tasks', broker='redis://localhost:6379')
# celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()


# @celery_app.task
# def task_celery_app():
#     pass
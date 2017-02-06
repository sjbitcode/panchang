from celery import Celery

results = []
celery = Celery()
celery.config_from_object('celeryconfig')


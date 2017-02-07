import logging
import logging.config

from celery import Celery

from .settings import LOG_SETTINGS


# Configure celery
celery = Celery('panchang')
# app = celery.config_from_object(CELERY_CONFIG)
# import pdb; pdb.set_trace();
# app.autodiscover_tasks()
celery.config_from_object('panchang.settings')
celery.autodiscover_tasks(['panchang'])

# Configure logger
logging.config.dictConfig(LOG_SETTINGS)
# logger = logging.getLogger('panchang.tasks')

# Run celery worker server
# celery -A panchang.main worker --loglevel=info --beat

import logging
import logging.config

from celery import Celery

from .settings import LOG_SETTINGS, MODULE_NAME


# Configure celery
celery = Celery(MODULE_NAME)
celery.config_from_object('{}.{}'.format(MODULE_NAME, 'settings'))
celery.autodiscover_tasks([MODULE_NAME])

# Configure logger
logging.config.dictConfig(LOG_SETTINGS)


# Run celery worker server
# celery -A panchang.main worker --loglevel=info --beat

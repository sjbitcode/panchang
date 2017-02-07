import logging
import logging.config

from celery import Celery

from .settings import MODULE_NAME, LOG_SETTINGS


# Configure celery
celery = Celery('MODULE_NAME')
# app = celery.config_from_object(CELERY_CONFIG)
# import pdb; pdb.set_trace();
# app.autodiscover_tasks()
celery.config_from_object('{}.{}'.format(MODULE_NAME, 'settings'))
celery.autodiscover_tasks(['MODULE_NAME'])

# Configure logger
logging.config.dictConfig(LOG_SETTINGS)
# logger = logging.getLogger('panchang.tasks')

# Run celery worker server
# celery -A panchang.main worker --loglevel=info --beat

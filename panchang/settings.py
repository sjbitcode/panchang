import os

from celery.schedules import crontab


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, 'log')

MODULE_NAME = 'panchang'

# Replace these values with your own!
SENDER_EMAIL = 'bob@example.com'
SENDER_PASSWORD = 'mypassword'
SEND_TO = ['bob@example.com', 'jen@example.com']


# Celery settings
CELERY_IGNORE_RESULT = False
CELERY_BROKER_HOST = '127.0.0.1'
CELERY_BROKER_PORT = 5672
CELERY_BROKER_URL = 'amqp://'
CELERY_RESULT_BACKEND = "rpc"
CELERY_TIMEZONE = 'America/New_York'
# Use celery autodiscover_tasks or CELERY_IMPORTS
# CELERY_IMPORTS = ('panchang.tasks',)


CELERYBEAT_SCHEDULE = {
    'send-panchang-email': {
        'task': '{}.tasks.send_panchang_email'.format(MODULE_NAME),
        'schedule': crontab(hour=6, minute=30)
    },
}

# Name loggers
LOGGER_1 = '{}.tasks'.format(MODULE_NAME)
LOGGER_2 = '{}.helpers.mailer'.format(MODULE_NAME)

# Log settings
LOG_SETTINGS = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%m-%d-%Y %H:%M:%S'
        }
    },

    'handlers': {
        'email_task': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 512000,
            'backupCount': 5,
            'filename': os.path.join(LOG_PATH, 'email-sender.log')
        }
    },

    'loggers': {
        LOGGER_1: {
            'handlers': ['email_task'],
            'level': 'INFO',
            'propagate': True,
        },

        LOGGER_2: {
            'handlers': ['email_task'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}

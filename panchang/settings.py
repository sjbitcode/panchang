import os

from celery.schedules import crontab

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, 'log')

MODULE_NAME = 'panchang'

SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')
SEND_TO = os.environ.get('SEND_TO').split(',')

BROKER_URL = 'amqp://guest:guest@rabbit:5672'
CELERY_RESULT_BACKEND = 'rpc'
CELERY_IGNORE_RESULT = False
CELERY_TIMEZONE = 'America/New_York'

CELERYBEAT_SCHEDULE = {
    'email-panchang-report': {
        'task': '{}.tasks.send_panchang_email'.format(MODULE_NAME),
        'schedule': crontab(hour=6, minute=30)
        # 'schedule': crontab(minute='*/2')
    }
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
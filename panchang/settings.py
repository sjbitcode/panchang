import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, 'log')


# Replace these values with your own!
# SENDER_EMAIL = 'bob@example.com'
# SENDER_PASSWORD = 'mypassword'
# SEND_TO = ['bob@example.com', 'jen@example.com']


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
        'panchang.tasks': {
            'handlers': ['email_task'],
            'level': 'INFO',
            'propagate': True,
        },

        'panchang.helpers.mailer': {
            'handlers': ['email_task'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}

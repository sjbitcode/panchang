from celery.schedules import crontab

CELERY_IGNORE_RESULT = False
# IP address of the server running RabbitMQ and Celery
BROKER_HOST = '127.0.0.1'
BROKER_PORT = 5672
BROKER_URL = 'amqp://'
CELERY_RESULT_BACKEND = "rpc"
CELERY_TIMEZONE = 'America/New_York'
CELERY_IMPORTS = ("tasks",)


CELERYBEAT_SCHEDULE = {
    'multiply-every-30-seconds': {
        # 'task': 'tasks.multiply',
        'task': 'tasks.send_panchang_email',
        'schedule': crontab(hour=0, minute=47),
        # 'schedule': 30.0,
        # 'args': (1, 2)
    },
}

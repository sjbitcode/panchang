from celery.schedules import crontab


# CELERYBEAT_SCHEDULE = {
#     'send-panchang-email': {
#         'task': 'tasks.send_panchang_email',
#         'schedule': crontab(hour=16, minute=48)
#     },
# }

CELERYBEAT_SCHEDULE = {
    'send-panchang-email': {
        'task': 'tasks.add',
        'schedule': 30.0,
        'args': (16, 16)
    },
}

# Run celery worker server:
# celery -A tasks worker --loglevel=info --beat

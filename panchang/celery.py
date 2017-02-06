from celery import Celery

app = Celery('panchang',
            broker='',
            backend='',
            include=['panchang.tasks']
            )
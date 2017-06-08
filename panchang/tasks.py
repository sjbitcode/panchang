import logging
from celery import task

from .helpers.mailer import Mailer
from .helpers.scraper import Panchang
from .helpers.utils import update_params
from .settings import LOGGER_1, SENDER_EMAIL, SENDER_PASSWORD, SEND_TO

logger = logging.getLogger(LOGGER_1)


@task
def send_panchang_email():
    url = 'http://www.mypanchang.com/phppanchang.php'
    query_params = {
        'monthtype': '0',
        'cityhead': 'New York, NY',
        'yr': '',
        'mn': '',
        'cityname': 'NewYork-NY'
    }

    # Update params with current date and instantiate Panchang instance.
    update_params(query_params)
    p = Panchang(url, query_params)
    data = p.aggregate_data()

    # Prepare data to create email.
    email_data = {
        'subject': data['subject'],
        'receivers': SEND_TO,
        'images': ['diya.gif'],
        'data': data
    }

    # Instantiate Mailer class and send email with data and a template.
    m = Mailer(SENDER_EMAIL, SENDER_PASSWORD, 'smtp.gmail.com')
    logger.info('About to send email')
    m.send_email(email_data, 'email-body.html')

from .main import celery
from .tasks import send_panchang_email

if __name__ == '__main__':
    print('Sending emails')
    send_panchang_email.delay()

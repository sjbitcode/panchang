from .tasks import send_panchang_email

if __name__ == '__main__':
    send_panchang_email.delay()
    print('Finish send email')

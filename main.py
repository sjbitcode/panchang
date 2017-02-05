from mailer import Mailer
from scraper import Panchang
from settings import SENDER_EMAIL, SENDER_PASSWORD, SEND_TO
from utils import update_params


# url and corresponding parameters
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
p = Panchang(url, **query_params)
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
m.send_email(email_data, 'email-body2.html')

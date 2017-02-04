from mailer import Mailer
from scraper import Panchang
from settings import SENDER_EMAIL, SENDER_PASSWORD, SEND_TO
from utils import (
    get_date_obj, update_params,
    string_padding, create_string_from_dict
)


# url and corresponding parameters
url = 'http://www.mypanchang.com/phppanchang.php'
query_params = {
    'monthtype': '0',
    'cityhead': 'New York, NY',
    'yr': '',
    'mn': '',
    'cityname': 'NewYork-NY'
}


# Email body template
MSG = """
Good morning! Here's your panchang for today, {}.


SUNRISE & SUNSET
{}

AUSPICIOUS TIMES
{}

INAUSPICIOUS TIMES
{}

All data taken from:
{}


Have a great day!
"""


# Update params with current date and instantiate Panchang.
update_params(query_params)
p = Panchang(url, **query_params)
data = p.aggregate_data()


# Organize data from Panchang instance.
# data = p.aggregate_data()
# heading, sun, ausp, inausp, url = data


# Create string from data for email.
# sun_text = create_string_from_dict(sun)
# ausp_text = create_string_from_dict(ausp)
# inausp_text = create_string_from_dict(inausp)


# Format MSG with strings.
# MSG = MSG.format(
#     get_date_obj().strftime('%B %d, %Y'),
#     sun_text, ausp_text, inausp_text, url
# )

heading = 'test heading'
# Instantiate Mailer and send emails!
# m = Mailer(SENDER_EMAIL, SENDER_PASSWORD, SEND_TO, heading, MSG)
m = Mailer(SENDER_EMAIL, SENDER_PASSWORD, SEND_TO, heading, 'some text')
# m.send_email()
# m.send_html_email()
m.jinja_email(data)

from bs4 import BeautifulSoup
import datetime
import requests
import smtplib
# import pytz

from settings import SENDER_EMAIL, SENDER_PASSWORD, SEND_TO
from utils import format_time_ranges

url = 'http://www.mypanchang.com/phppanchang.php'
query_params = {
    'monthtype': '0',
    'cityhead': 'New York, NY',
    'yr': '',
    'mn': '',
    'cityname': 'NewYork-NY'
}


def get_date_obj():
    # datetime.datetime.now(pytz.timezone('America/New_York'))
    return datetime.date.today()


def update_params(query_params):
    '''
    Get datetime object and
    modify query params values with
    year, month, and day.

    Months are 0-based.
    Example of parameters:
    "?yr=2017&cityhead=New%20York,%20NY&cityname=NewYork-NY&monthtype=0&mn=8#2"
    '''
    date_obj = get_date_obj()
    query_params['mn'] = date_obj.month-1
    query_params['yr'] = date_obj.year

    return query_params


class Downloader:
    '''
    This class is to retrieve html code
    from a specific website.
    '''

    def __init__(self, url, **kwargs):
        self.url = url
        self.queryparams = kwargs
        self.content = ''

    def download(self):
        request_obj = requests.get(self.url, params=self.queryparams)
        if request_obj.status_code == 200:
            self.content = request_obj.content


class Panchang(Downloader):
    def __init__(self, url, **kwargs):
        super(Panchang, self).__init__(url, **kwargs)

    def get_html(self):
        self.download()
        soup = BeautifulSoup(self.content, 'html.parser')
        return soup

    def get_tables(self):
        day = get_date_obj().day
        soup = self.get_html()
        a_tag = soup.find('a', {'name': day})
        tables = a_tag.find_next_siblings('table')

        return tables

    def aggregate_data(self):
        tables = self.get_tables()

        heading = tables[3].text
        sun = self.get_sun_times(tables[4])
        auspicious = self.get_auspicious_times(tables[5])
        inauspicious = self.get_inauspicious_times(tables[5])

        return (heading, sun, auspicious, inauspicious)

    def get_sun_times(self, table):
        keys = ['Sunrise', 'Sunset']
        return self.from_table(keys, table)

    def get_auspicious_times(self, table):
        keys = ['Abhijit Muhurta', 'Amritkalam']
        return self.from_table(keys, table)

    def get_inauspicious_times(self, table):
        keys = [
            'Rahukalam', 'Yamagandam', 'Gulikai',
            'Varjyam', 'Durmuhurtham'
        ]
        return self.from_table(keys, table)

    def from_table(self, keys, table):
        '''
        Given keys (search terms) and a table,
        create and return dictionary with keys
        their respective times in the table.

        Ex: {'Sunrise': '07:07:56', 'Sunset': '17:11:30'}
        '''

        info_dict = {}

        for key in keys:
            # Returns list of bs4 tag elements.
            elements = table.find_all(text='{}:'.format(key))

            if len(elements) == 1:
                # If only one element found, get the time and store in dict.
                # info_dict[key] = elements[0].next_element.text
                # print(elements[0].next_element.text)
                info_dict[key] = format_time_ranges(elements[0].next_element.text)
            else:
                # If multiple elements found with same key,
                # iterate through each element's next_element.
                times = ''
                for tag in elements:
                    # concatenate string with each elements' times
                    # times += ', {}'.format(tag.next_element.text)
                    times += ', {}'.format(format_time_ranges(tag.next_element.text))
                times = times.lstrip(', ')
                info_dict[key] = times

        return info_dict


update_params(query_params)
d = Panchang(url, **query_params)

tt = d.aggregate_data()

heading = tt[0]
sun = tt[1]
ausp = tt[2]
inausp = tt[3]

sun_text = ''
for key in sun:
    sun_text += '{}: {}'.format(key, sun[key])
    sun_text += '\n'


ausp_text = ''
for key in ausp:
    ausp_text += '{}: {}'.format(key, ausp[key])
    ausp_text += '\n'


inausp_text = ''
for key in inausp:
    inausp_text += '{}: {}'.format(key, inausp[key])
    inausp_text += '\n'


MSG = """
Good morning! Here's your panchang for today, {}.


SUNRISE & SUNSET
{}

AUSPICIOUS TIMES
{}

INAUSPICIOUS TIMES
{}


Have a great day!
"""
MSG = MSG.format(
    get_date_obj().strftime('%B %d, %Y'),
    sun_text, ausp_text, inausp_text
)

gmail_user = SENDER_EMAIL
gmail_password = SENDER_PASSWORD

to_email = SEND_TO
subject = heading
body = MSG

email_text = 'Subject: {}\n\n{}'.format(subject, body)

# try:
#     server_ssl = smtplib.SMTP_SSL('smtp.gmail.com')
#     server_ssl.ehlo()
#     server_ssl.login(gmail_user, gmail_password)

#     # Send emails!
#     server_ssl.sendmail(gmail_user, to_email, email_text)
#     server_ssl.close()
#     print('Email sent!')
# except:
#     print('Something went wrong!')

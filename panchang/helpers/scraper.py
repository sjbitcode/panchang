from bs4 import BeautifulSoup
import requests

from .utils import (get_date_obj, format_time_ranges)


class Downloader:
    '''
    The Download class is to retrieve html code
    from a specific website.
    '''

    def __init__(self, url, **kwargs):
        self.url = url
        self.encoded_url = ''
        self.queryparams = kwargs
        self.content = ''

    def download(self):
        request_obj = requests.get(self.url, params=self.queryparams)
        if request_obj.status_code == 200:
            self.content = request_obj.content
            self.encoded_url = request_obj.url


class Panchang(Downloader):
    '''
    The Panchang class is for retrieving data
    specifically from MyPanchang.com.

    Initialize instance with url and query parameters.

    Call aggregate_data() to see final tuple of
    data to be injected in email message.
    '''
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
        '''
        Return a dictionary of dictionaries.

        Ex. {
            'subject': 'Panchang for January 20, 2017',
            'sun': {'Sunrise':'6:07', 'Sunset':'5:20'},
            'auspicious': {'Amritkalam': '12:20-2:20', 'Abhijit': '3:20-4:08'},
            'inauspicious': {'Rahukalam': '9:38-10:00'},
            'encoded_url': 'http://mypanchang.com/mn=0&city=New%20York'
        }
        '''
        tables = self.get_tables()

        today = get_date_obj().strftime('%B %d, %Y')
        subject = tables[3].text
        sun = self.get_sun_times(tables[4])
        auspicious = self.get_auspicious_times(tables[5])
        inauspicious = self.get_inauspicious_times(tables[5])
        encoded_url = '{}#{}'.format(self.encoded_url, get_date_obj().day)

        return {
            'today': today,
            'subject': subject,
            'sun': sun,
            'auspicious': auspicious,
            'inauspicious': inauspicious,
            'encoded_url': encoded_url
        }

    def get_sun_times(self, table):
        '''
        Given table, return dict
        with times for each key.
        '''

        keys = ['Sunrise', 'Sunset']

        return self.from_table(keys, table)

    def get_auspicious_times(self, table):
        '''
        Given table, return dict
        with times for each key.
        '''

        keys = ['Abhijit Muhurta', 'Amritkalam']

        return self.from_table(keys, table)

    def get_inauspicious_times(self, table):
        '''
        Given table, return dict
        with times for each key.
        '''

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

            # If elements nonempty
            if elements:

                # If only one element found, get the time and store in dict.
                if len(elements) == 1:
                    try:
                        info_dict[key] = format_time_ranges(
                            elements[0].next_element.text
                        )
                    except:
                        info_dict[key] = 'None'

                # If multiple elements found with same key, concatenate times.
                # ex. ['Amritkalam', 'Amritkalam']
                else:
                    times = ''

                    # concatenate string with each element's times
                    for tag in elements:
                        try:
                            time = format_time_ranges(tag.next_element.text)
                            times += ', {}'.format(time)
                        except:
                            pass

                    times = times.lstrip(', ')
                    info_dict[key] = times

            # If no elements, make value 'None'
            else:
                info_dict[key] = 'None'

        return info_dict

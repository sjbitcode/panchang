from bs4 import BeautifulSoup
import requests

from .utils import (get_date_obj, format_time_ranges, get_first_time)


class Downloader:
    '''
    The Download class is to retrieve html code
    from a specific website.
    '''

    def __init__(self, url, queryparams):
        self.url = url
        self.encoded_url = ''
        self.queryparams = queryparams
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
    def __init__(self, url, options):
        super(Panchang, self).__init__(url, queryparams=options)

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
        Return a dictionary of the following data.

        Ex. {
            'today': 'June 07, 2017',
            'subject': 'Panchang for June 07, 2017',
            'sun_keys': ['Sunrise', 'Sunset'],
            'ausp_keys': ['Abhijit Muhurta', 'Amritkalam'],
            'inausp_keys': ['Rahukalam', 'Yamagandam', 'Gulikai',
                            'Varjyam', 'Durmuhurtham'],
            'times': [
                ('12:30:42', '12:30:42 PM - 01:18:42 PM', 'Rahukalam'),
                ('13:24:34', '01:24:34 PM - 02:24:16 PM', 'Durmuhurtham'),
                ('14:30:51', '02:30:51 PM - 04:17:32 PM', 'Varjyam')
            ]
            'encoded_url': 'http://mypanchang.com/mn=0&city=New%20York'
        }
        '''
        tables = self.get_tables()

        today = get_date_obj().strftime('%B %d, %Y')
        subject = tables[3].text
        encoded_url = '{}#{}'.format(self.encoded_url, get_date_obj().day)

        # Get lists for each category of time.
        sun = self.get_sun_times(tables[4])
        auspicious = self.get_auspicious_times(tables[5])
        inauspicious = self.get_inauspicious_times(tables[5])

        # Create complete sorted list of all time categories.
        complete_times = self.combine_sort_times(sun, auspicious, inauspicious)

        return {
            'today': today,
            'subject': subject,
            'times': complete_times,
            'sun_keys': ['Sunrise', 'Sunset'],
            'ausp_keys': ['Abhijit Muhurta', 'Amritkalam'],
            'inausp_keys': ['Rahukalam', 'Yamagandam', 'Gulikai',
                            'Varjyam', 'Durmuhurtham'],
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
        return list of tuples in the form:

        (starting_time, formatted_time_range, name_of_time_period)

        [
            ('13:24:34', '01:24:34 PM - 02:24:16 PM', 'Durmuhurtham'),
            ('14:30:51', '02:30:51 PM - 04:17:32 PM', 'Varjyam'),
            ('12:30:42', '12:30:42 PM - 01:18:42 PM', 'Rahukalam')
        ]
        '''
        info_list = []

        for key in keys:
            # Returns list of bs4 tag elements.
            elements = table.find_all(text='{}:'.format(key))

            if elements:
                # If there are multiple of same key, iterate.
                for tag in elements:
                    try:
                        time = tag.next_element.text
                        info_list.append(
                            (
                                get_first_time(time),
                                format_time_ranges(time),
                                key
                            )
                        )
                    except:
                        pass
            else:
                continue

        return info_list

    def combine_sort_times(self, *time_lists):
        '''
        Takes arbitrary number of lists.

        Each list is of the form:
        [
            ('09:24:34', '09:24:34 PM - 10:24:16 PM', 'Amritkalam'),
            ('18:40:51', '06:40:51 PM - 08:19:32 PM', 'Varjyam')
        ]

        Combines lists into a complete list.
        Return sorted list. Sorted based on first element of the tuple.
        '''
        complete_list = []

        # Build one list from all lists inputted.
        for time_list in time_lists:
            complete_list.extend(time_list)

        # Sort complete list by first element of each tuple.
        complete_list = sorted(complete_list, key=lambda x: x[0])

        return complete_list

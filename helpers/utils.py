import datetime


def get_date_obj():
    return datetime.date.today()


def string_padding(key, width=21):
    '''
    Returns appropriate whitespace string
    for left padding.
    '''
    padding = ' ' * abs(width - len(key))

    return padding


def create_string_from_dict(d):
    '''
    Given a dict, create a string from keys and values.

    Ex. {'Red': 'cherry, apple', 'Yellow': 'banana, lemon'}
    return the following string depending on what width string_padding set to

    "Yellow:         banana, lemon\nRed:         cherry, apple\n"
    '''
    text = ''
    for key in d:
        text += '{}:{}{}'.format(key, string_padding(key), d[key])
        text += '\n'
    return text


def update_params(query_params):
    '''
    Get datetime object and
    modify query params values with
    year, month, and day.

    Months are 0-based.
    Example of parameters (mypanchang page for September, 2017):
    "?yr=2017&cityhead=New%20York,%20NY&cityname=NewYork-NY&monthtype=0&mn=8"
    '''
    date_obj = get_date_obj()
    query_params['mn'] = date_obj.month-1
    query_params['yr'] = date_obj.year

    return query_params


def military_to_standard(time):
    '''
    Given a time in string format,
    return standardized time string.

    Ex.
        '13:25:34' -> '01:25:34 PM'
        '08:22:41' -> '08:22:41 AM'
        '24:41:22' -> '12:41:22 AM (tomorrow)'
        '75:30:12' -> '03:30:12 AM (3 days from today)'
    '''
    time_list = time.split(':')
    days = 0

    # Convert the hour to a 12-hour value, store days quotient.
    if (int(time_list[0]) >= 24):
        hour = int(time_list[0])
        days, remainder_hours = divmod(hour, 24)
        time_list[0] = str(remainder_hours)
        time = ':'.join(time_list)

    # Convert string to datetime object, then format datetime object.
    datetime_obj = datetime.datetime.strptime(str(time), '%H:%M:%S')
    formatted_time = datetime_obj.strftime("%I:%M:%S %p")

    # Format days string depending on if day=1 or more.
    if days:
        day_string = ''
        if days == 1:
            day_string = '(tomorrow)'
        else:
            day_string = '({} days from today)'.format(days)
        return '{} {}'.format(formatted_time, day_string)

    return formatted_time


def format_time_ranges(time):
    '''
    If given a range of times, ex. '08:20:10-10:25:16',
    call military_to_standard() for each time.

    Else, call military_to_standard for a single time.
    '''
    if '-' in time:
        time_list = time.split('-')
        return '{} - {}'.format(
            military_to_standard(time_list[0]),
            military_to_standard(time_list[1])
        )
    else:
        return military_to_standard(time)

import datetime


def military_to_standard(time):

    time_list = time.split(':')
    days = 0

    print(time)
    print(time_list)
    print(time_list[0])
    
    if (int(time_list[0]) > 24):
        hour = int(time_list[0])
        days, remainder_hours = divmod(hour, 24)
        time_list[0] = str(remainder_hours)
        time = ':'.join(time_list)

    datetime_obj = datetime.datetime.strptime(str(time), '%H:%M:%S')
    formatted_time = datetime_obj.strftime("%I:%M:%S %p")

    if days:
        day_string = ''
        if days == 1:
            day_string = '(the next day)'
        else:
            day_string = '({} days from now)'.format(days)
        return '{} {}'.format(formatted_time, day_string)
    return formatted_time


def format_time_ranges(time):
    if '-' in time:
        time_list = time.split('-')
        return '{} - {}'.format(
            military_to_standard(time_list[0]),
            military_to_standard(time_list[1])
        )
    else:
        return military_to_standard(time)

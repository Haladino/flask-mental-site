import os
from collections import namedtuple
from datetime import datetime, timedelta

from app import app


LOC = os.path.dirname(os.path.realpath(__file__))


Event = namedtuple('Event', ['start', 'end'])


SE_EVENTS = [Event(datetime(2020, 7, 7, 8), datetime(2020, 7, 7, 9)),
            Event(datetime(2020, 7, 10, 10), datetime(2020, 7, 10, 11))]


def read_text_content(filename, split_on=None):
    path = os.path.join(LOC, 'static', 'text', filename) + '.txt'
    with open(path, 'r', encoding='utf-8') as f:
        if split_on:
            return [line.split(split_on) for line in f]
        else:
            return [line for line in f]



CITATION_TEXT = {'hu': read_text_content('citation'),
                'en': read_text_content('citation_en')}

HELP_TEXT = {'hu': read_text_content('help'),
            'en': read_text_content('help_en')}

SERVICES = {'hu': read_text_content('services', split_on=','),
            'en': read_text_content('services_en', split_on=',')}


def full_hours(name, days):
    res = {hour: {day : False for day in days.values()} for hour in range(8, 17)}
    for event in SE_EVENTS:
        start = event.start
        end = event.end
        day = start.date()
        hour = start.hour
        if hour in res.keys() and day in res[hour].keys():
            res[hour][day] = True
    return res

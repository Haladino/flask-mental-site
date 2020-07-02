import os
from app import app


LOC = os.path.dirname(os.path.realpath(__file__))


def read_text_content(filename, split_on=None):
    with open(os.path.join(LOC, 'static', 'text', filename) + '.txt') as f:
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
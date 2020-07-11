import os
import config
from flask import json
from datetime import date, timedelta

def read_file(filepath, file_type=None, encode='utf-8'):
    
    ROOT = config.ROOT
    PATH = os.path.join(config.STATIC_ROOT ,filepath) # Only read files from static

    FILE = open(PATH, "r", encoding=encode)

    if file_type==json:
        DATA = json.load(FILE) # Read as JSON as database
    else:
        DATA = FILE.read() # Read text files

    return DATA


def current_weekdays():

    days_hu = ['Hétfő', 'Kedd', 'Szerda', 'Csütörtök', 'Péntek', 'Szombat', 'Vasárnap']
    today = date.today()
    week_no = today.weekday()
    monday = today - timedelta(days=week_no)

    return {days_hu[i]: monday + timedelta(days=i) for i in range(7)}

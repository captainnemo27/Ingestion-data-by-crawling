from time import time
from datetime import datetime
from datetime import timedelta
import datetime
import os
import os.path
import sys

folder = os.getcwd()


def create_today_string():
    '''
    Returns the string of today from command line arguments in Python

        Parameters:
                None

        Returns:
                today (str): String of date

        Format date: YYYYMMDD
                Example: 20200826
                        Year 2020
                        Month 08
                        Day 26

        Example command line arguments:
                python3 youhomes_helper.py 20200826
                Returns: 20200826
    '''
    for i in range(0, len(sys.argv)):
        if sys.argv[i].isnumeric():
            return sys.argv[i]
        if sys.argv[i].find("argument") >= 0:
            number_string = ''
            for char in sys.argv[i]:
                if char.isnumeric():
                    number_string = number_string + char
            return number_string


def create_folder():
    return (
        folder,
        today,
        today_folder,
        all_folder,
        delta_folder,
        list_mode,
        sale_folder,
        lease_folder,
        to_buy_to_lease_folder)


today = create_today_string()
if (str(type(today)).find('None') >= 0):
    date = datetime.datetime.now()
    today = date.strftime('%Y') + date.strftime('%m') \
        + date.strftime('%d')
today_folder = folder + '/' + today
all_folder = folder + '/' + today + '/ALL'
delta_folder = folder + '/' + today + '/DELTA'
list_mode = folder + '/' + today + '/LIST_MODE'
sale_folder = list_mode + '/' + 'FOR_SALE'
lease_folder = list_mode + '/' + 'FOR_LEASE'
to_buy_to_lease_folder = list_mode + '/' + 'TO_BUY_TO_LEASE'

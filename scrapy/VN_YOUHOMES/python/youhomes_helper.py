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
        if sys.argv[i].isnumeric() == True :
            return sys.argv[i]
        if sys.argv[i].find("argument") >= 0 :
            number_string = ''
            for char in sys.argv[i]:
                if char.isnumeric() == True:
                    number_string = number_string + char
            return number_string


def create_folder():
    return (
        folder,
        today,
        today_folder,
        spider_folder,
        all_folder,
        delta_folder,
        list_mode,
        sale_folder,
        lease_folder,
        house_sale_folder,
        apartment_sale_folder,
        house_lease_folder,
        apartment_lease_folder)


today = create_today_string()
spider_folder = folder + '/python/download_site/download_site/spiders'
all_folder = folder + '/' + today + '/ALL'
delta_folder = folder + '/' + today + '/DELTA'
list_mode = folder + '/' + today + '/LIST_MODE'
sale_folder = list_mode + '/' + 'mua'
lease_folder = list_mode + '/' + 'thue'
house_sale_folder = sale_folder + '/' + 'nha'
apartment_sale_folder = sale_folder + '/can_ho'
house_lease_folder = lease_folder + '/nha'
apartment_lease_folder = lease_folder + '/can_ho'
today_folder = folder + '/' + today

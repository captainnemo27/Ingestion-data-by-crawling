from time import time
from datetime import datetime
from datetime import timedelta
import datetime
import os
import os.path
import wget
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
                python3 chotot_helper.py 20200826
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
    '''
    Returns path to folders

            Parameters:
                    None

            Returns:
                    folder, today, spider_folder, all_folder, delta_folder, list_mode (str): String of path to folders
    '''
    return (folder, today, today_folder, spider_folder, all_folder, delta_folder, list_mode)


today = create_today_string()
spider_folder = folder + '/python/download_site/download_site/spiders'
print(folder, today)
all_folder = folder + '/' + today + '/ALL'
delta_folder = folder + '/' + today + '/DELTA'
list_mode = folder + '/' + today + '/LIST_MODE'
today_folder = folder + '/' + today

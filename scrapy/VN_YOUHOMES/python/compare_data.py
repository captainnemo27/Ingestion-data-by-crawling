#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import time
from datetime import timedelta
import datetime
import os
import os.path
import sys
import youhomes_helper


def create_yesterday_string(today):
    '''
    Returns the string of yesterday

        Parameters:
                today (string): String of date

        Returns:
                yesterday (str): String of yesterday

        Format date: YYYYMMDD
            Example: 20200826
                    Year 2020
                    Month 08
                    Day 26

        Suppose today is 20200826. Call function create_yesterday_string(20200826), result is 20200825.
    '''
    date = datetime.datetime(int(today[0:4]), int(today[4:6]), int(today[6:8]))
    yesterday = date - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%Y') + yesterday.strftime('%m') \
        + yesterday.strftime('%d')
    return yesterday


def compare_data(yesterday_delta_folder, today_delta_folder):
    '''
    Returns new ads's id_client of today compared to yesterday

        Parameters:
                yesterday_delta_folder (str): String of path to yesterday delta folder
                today_delta_folder (str): String of path to today delta folder

        Returns:
                new_dictionary_id (dict): Key is id_client. If key exist, value = 1 else default value = 0.
    '''

    yesterday_dictionary_id = {}
    new_dictionary_id = {}
    path_to_file = yesterday_delta_folder + '/list_id.txt'
    print(path_to_file)
    yesterday_delta_file = open(path_to_file, 'r')

    for line in yesterday_delta_file.readlines():
        yesterday_dictionary_id[line.replace('\n', '')] = 1

    path_to_file = today_delta_folder + '/list_id.txt'
    print(path_to_file)
    today_delta_file = open(path_to_file, 'r')
    for line in today_delta_file.readlines():
        if line.replace('\n', '') not in yesterday_dictionary_id:
            new_dictionary_id[line.replace('\n', '')] = 1

    yesterday_delta_file.close()
    today_delta_file.close()
    return new_dictionary_id


def create_list_new_id(new_dictionary_id):
    '''
    Creates list_new_id.txt file in DELTA folder

            Parameters:
                    new_dictionary_id (dict): Dictionary of new ads's id_client

            Returns:
                    None
    '''

    new_list_id_file = open(delta_folder + '/list_new_id.txt', 'w')
    if len(new_dictionary_id) > 0:
        for (key, value) in new_dictionary_id.items():
            new_list_id_file.write(key + '\n')
    else:
        new_list_id_file.write('0')
    new_list_id_file.close()
    return None


folder, today, today_folder, spider_folder, all_folder, delta_folder, list_mode, sale_folder, lease_folder, house_sale_folder, apartment_sale_folder, house_lease_folder, apartment_lease_folder = youhomes_helper.create_folder()
yesterday = create_yesterday_string(today)

# ------------ YESTERDAY FOLDER -----------
# Check if a Directory exists

if os.path.isdir(folder + '/' + yesterday) == False:
    print("PATH TO YESTERDAY FOLDER ", folder + '/' + yesterday)
    print("PATH TO TODAY FOLDER ", delta_folder + '/list_new_id.txt')
    f = open(delta_folder + '/list_new_id.txt', 'w')
    f.write('-1')
    f.close()
    sys.exit('Yesterday folder has not exist')

# Check if a File exists

yesterday_delta_folder = folder + '/' + yesterday + '/DELTA'
if os.path.isfile(yesterday_delta_folder + '/list_id.txt') == False:
    f = open(delta_folder + '/list_new_id.txt', 'w')
    f.write('-1')
    f.close()
    sys.exit('Yesterday list id.txt has not exist')

new_dictionary_id = compare_data(yesterday_delta_folder, delta_folder)
create_list_new_id(new_dictionary_id)
print('DONE COMPARE DATA')

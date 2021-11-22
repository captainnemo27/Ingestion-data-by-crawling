#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import glob
from time import time
from os import path
import muabannhadat_helper
import json
import unidecode

#   Function to check whether given key already exists in a dictionary


def check_key(dict, key):
    '''
    Returns true if key exist in dictionary, false if key has not exist

            Parameters:
                    dict (dictionary): A dictionary of json files
                    key (str): String key of dictionary

            Returns:
                    True: If key exist in dictionary
                    False: If not exist
    '''

    if key in dict.keys():
        return True
    else:
        return False


def delete_special_character(string):
    '''
    Returns the string deleted special character

        Parameters:
                string (str): The string has many character (number, char, ...)

        Returns:
                string (str): The string after being deleted special character
    '''
    string = string.replace('\n', '')
    string = string.replace('"', '')
    string = string.replace("'", "")
    string = string.replace(";", "")
    character = ''.join(chr(92))  # chr(92) character in ASCII TABLE is \
    string = string.replace(character, '')
    string = string.replace('  ', '')
    return string


def delete_icon(string):
    '''
    Returns string after deleting the emotion symbol, stickers in message

            Parameters:
                    string (str): The string of message or paragraphs.

            Returns:
                    string (str): The string after processing
    '''
    icon = []
    for i in range(0, len(string)):
        if ord(string[i]) > 9000:
            icon.append(string[i])
    for i in range(0, len(icon)):
        string = string.replace(icon[i], ' ')
    return string


def extract(json_file):
    '''
    Returns the fields of site
            Parameters:
                    json_file (string): File html contains ads's details

            Returns:
                    data (dict): Dictionary of ads's details with key is the fields and value is the field's value
    '''
    ads = []
    # file_name = []
    # file_name.append(glob.glob(sale_folder + '/*.json'))
    # file_name.append(glob.glob(lease_folder + '/*.json'))
    # for folder in range(0, len(file_name)):
    #     for position_json_file_in_folder in range(
    #             0, len(file_name[folder])):
    #         with open(file_name[folder][position_json_file_in_folder], 'r') as file:
    #             json_file = json.load(file)
    for ads_index in range(len(json_file['data'])):
        data = {}
        if check_key(json_file['data'][ads_index], 'id'):
            data['ID_CLIENT'] = json_file['data'][ads_index]['id']
        data['SITE'] = 'muabannhadat.vn'
        data['CREATED_DATE'] = today
        data['PRO_FLAG'] = 0 
        if check_key(
            json_file['data'][ads_index],
                'offer_type'):
            if json_file['data'][ads_index]['offer_type'].find(
                    "sell") > -1:
                data['FOR_SALE'] = 1
            if json_file['data'][ads_index]['offer_type'].find(
                    "rent") > -1:
                data['FOR_LEASE'] = 1
        if check_key(
                json_file['data'][ads_index]['category'],
                'title'):
            data['LAND_TYPE'] = json_file['data'][ads_index]['category']['title']
        elif check_key(json_file['data'][ads_index]['category'], 'slug'):
            data['LAND_TYPE'] = json_file['data'][ads_index]['category']['slug'].split(
                '-')[0]
        if check_key(json_file['data'][ads_index], 'online-at'):
            data['ADS_DATE'] = json_file['data'][ads_index]['online-at']
            data['ADS_DATE_ORIGINAL'] = data['ADS_DATE']
        for properties_index in range(
                len(json_file['data'][ads_index]['data_properties'])):
            properties = json_file['data'][ads_index]['data_properties'][properties_index]
            if properties['field'].find("area_value") > -1:
                data['USED_SURFACE'] = properties['value']
            if properties['field'].find("area_unit") > -1:
                data['USED_SURFACE_UNIT'] = properties['value']
            if properties['field'].find("width") > -1:
                data['PRO_WIDTH'] = properties['value']
            if properties['field'].find("length") > -1:
                data['PRO_LENGTH'] = properties['value']
            if properties['field'].find("direction") > -1:
                data['PRO_DIRECTION'] = properties['display_value']
            if properties['field'].find("legal_document") > -1:
                data['LEGAL_STATUS'] = properties['display_value']
            if properties['field'].find("points_of_interest") > -1:
                utilities = ''
                for utility_index in range(len(properties['value'])):
                    if utility_index < len(properties['value']) - 1:
                        utilities = utilities + \
                            properties['value'][utility_index]['label'] + ', '
                    else:
                        utilities = utilities + \
                            properties['value'][utility_index]['label']
                data['PRO_UTILITIES'] = utilities
                if utilities.find("Siêu thị") >= 0:
                    data['SUPERMARKET'] = 1
                if utilities.find("Bệnh viện") >= 0:
                    data['HOSPITAL'] = 1
                if utilities.find("Công viên") >= 0:
                    data['PARK'] = 1
                if utilities.find("Trường học") >= 0:
                    data['SCHOOL'] = 1
            if properties['field'].find("level_count") > -1:
                data['NB_FLOORS'] = properties['value']
            if properties['field'].find("bedroom_count") > -1:
                data['BEDROOM'] = properties['value']
            if properties['field'].find("bathroom_count") > -1:
                data['BATHROOM'] = properties['value']
            if properties['field'].find("latitude") > -1:
                data['LAT'] = properties['value']
            if properties['field'].find("longitude") > -1:
                data['LON'] = properties['value']
            if properties['field'].find("alley") > -1:
                data['ALLEY_ACCESS'] = properties['value']

        if check_key(json_file['data'][ads_index], 'price'):
            data['PRICE_ORIGINAL'] = json_file['data'][ads_index]['price']
        if check_key(
                json_file['data'][ads_index]['address'],
                'street_name'):
            if json_file['data'][ads_index]['address']['street_number'] is not None and json_file[
                    'data'][ads_index]['address']['street_name'] is not None:
                if unidecode.unidecode(json_file['data'][ads_index]['address']['street_name'].lower()).find(
                        "duong") >= 0 or json_file['data'][ads_index]['address']['street_number'].isnumeric():
                    data['STREET'] = json_file['data'][ads_index]['address']['street_number'] + \
                        ' ' + json_file['data'][ads_index]['address']['street_name']
                else:
                    data['STREET'] = json_file['data'][ads_index]['address']['street_name'] + \
                        ' ' + json_file['data'][ads_index]['address']['street_number']
            elif json_file['data'][ads_index]['address']['street_number'] is not None:
                data['STREET'] = json_file['data'][ads_index]['address']['street_number']
            elif json_file['data'][ads_index]['address']['street_name'] is not None:
                data['STREET'] = json_file['data'][ads_index]['address']['street_name']
        if check_key(
                json_file['data'][ads_index]['location'],
                'title'):
            data['WARD'] = json_file['data'][ads_index]['location']['titles']['vi']
        if check_key(
                json_file['data'][ads_index]['location']['parent'],
                'title'):
            data['DISTRICT'] = json_file['data'][ads_index]['location']['parent']['titles']['vi']
        if check_key(
                json_file['data'][ads_index]['location']['parent']['parent'],
                'title'):
            data['CITY'] = json_file['data'][ads_index]['location']['parent']['parent']['titles']['vi']
        if check_key(json_file['data'][ads_index], 'path'):
            data['ADS_LINK'] = 'https://www.muabannhadat.vn' + \
                json_file['data'][ads_index]['path']
        if check_key(json_file['data'][ads_index], 'title'):
            data['ADS_TITLE'] = json_file['data'][ads_index]['title']
        if check_key(json_file['data'][ads_index], 'description'):
            data['DETAILED_BRIEF'] = json_file['data'][ads_index]['description']
        # if check_key(json_file['data'][ads_index], 'heading'):
        #     data['BRIEF'] = json_file['data'][ads_index]['heading']
        if check_key(json_file['data'][ads_index], 'images'):
            data['PHOTOS'] = len(
                json_file['data'][ads_index]['images'])
        if check_key(
                json_file['data'][ads_index],
                'created_by') and check_key(
                json_file['data'][ads_index]['created_by'],
                'chat_id'):
            data['DEALER_ID'] = json_file['data'][ads_index]['created_by']['chat_id']
        if check_key(
                json_file['data'][ads_index],
                'created_by') and check_key(
                json_file['data'][ads_index]['created_by'],
                'name'):
            data['DEALER_NAME'] = json_file['data'][ads_index]['created_by']['name']
        if check_key(
                json_file['data'][ads_index],
                'created_by') and check_key(
                json_file['data'][ads_index]['created_by'],
                'mobile_number'):
            data['DEALER_TEL'] = json_file['data'][ads_index]['created_by']['mobile_number']
        dealer_address = json_file['data'][ads_index]['created_by']['address']
        dealer_full_address = ''
        if dealer_address is not None:
            if dealer_address['street_number'] is not None and dealer_address['street_name'] is not None:
                if unidecode.unidecode(dealer_address['street_name'].lower()).find(
                        "duong") >= 0 or dealer_address['street_number'].isnumeric():
                    # data['DEALER_ADDRESS'] = dealer_address['street_number'] + ' ' +\
                    #     dealer_address['street_name']
                    dealer_full_address = dealer_address['street_number'] + \
                        ' ' + dealer_address['street_name']
                else:
                    dealer_full_address = dealer_address['street_name'] + \
                        ' ' + dealer_address['street_number']
            elif dealer_address['street_number'] is not None:
                dealer_full_address = dealer_address['street_number']
            elif dealer_address['street_name'] is not None:
                dealer_full_address = dealer_address['street_name']
            try:
                if dealer_address['location']['titles'] is not None:
                    dealer_full_address = dealer_full_address + \
                        ', ' + dealer_address['location']['titles']['vi']
            except:
                pass
            try:
                if dealer_address['location']['parent']['titles'] is not None:
                    dealer_full_address = dealer_full_address + \
                        ', ' + dealer_address['location']['parent']['titles']['vi']
            except:
                pass
            try:
                if dealer_address['location']['parent']['parent']['titles'] is not None:
                    dealer_full_address = dealer_full_address + ', ' + \
                        dealer_address['location']['parent']['parent']['titles']['vi']
            except:
                pass
            if len(dealer_full_address) > 0 and dealer_full_address[0] == ',':
                dealer_full_address = dealer_full_address.replace(", ", "", 1)
            data['DEALER_ADDRESS'] = dealer_full_address
        features_is_none = []
        for (key, value) in data.items():
            if value is None:
                features_is_none.append(key)
                continue
            if str(type(value)).find('str') >= 0:
                data[key] = delete_special_character(value)
                data[key] = delete_icon(data[key])
        for feature in features_is_none:
            del data[feature]
        ads.append(data)
    return ads


def store(ads):
    '''
    Returns SQL command line to insert datas into database

        Parameters:
                ads (list of dictionary): The list of ads's fields

        Returns:
                total_sql_query (str): The string of SQL command line

    '''
    total_sql_query = ''
    for ads_index in range(len(ads)):
        result = 'INSERT IGNORE INTO MUABANNHADAT set '
        for (key, value) in ads[ads_index].items():
            result = result + str(key) + '=' + '"' + str(value) + '",'
        result = result[0:len(result) - 1] + ' ;'
        if ads_index < len(ads) - 1:
            result = result + '\n'
        total_sql_query = total_sql_query + result
    return total_sql_query


start = time()

folder, today, today_folder, spider_folder, all_folder, delta_folder, list_mode, sale_folder, lease_folder = muabannhadat_helper.create_folder()

# Total json files in ALL folder
json_files = glob.glob(sale_folder + '/*.json') + \
    glob.glob(lease_folder + '/*.json')

print("Total json files:", len(json_files))
with open(delta_folder + '/VO_ANNONCE_insert.sql', 'w') as f:
    for i in range(0, len(json_files)):
        if os.path.isfile(json_files[i]) == False:
            continue
        print(i + 1, json_files[i])
        with open(json_files[i], 'r') as file:
            ads = extract(json.load(file))
        #   WRITE SQL FILE INTO VO_ANNOUNCE_INTO.SQL
        f.write(store(ads))
f.close()
print('DONE PUT HTML INTO DELTA AND CREATE FILE INSERT SQL')
delta = time()
print('------%s SECONDS-------' % (delta - start))

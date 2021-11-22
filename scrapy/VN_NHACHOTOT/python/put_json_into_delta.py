#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import glob
from datetime import datetime, date
from time import time
import unidecode
import json
from os import path
import chotot_helper

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


def create_ads_link(
    region_name,
    area_name,
    category_name,
    list_id,
    type,
):
    '''
    Returns ads's link

            Parameters:
                    region_name (str): Region's name (Example: Tp Hồ Chí Minh, ...)
                    area_name (str): Area's name (Example: Quận 9, ...)
                    category_name (str): Category's name (Example: Đất, ...)
                    list_id (str): Ads's id_client (Example: 65257683)
                    type (char): Type of real estate (Example: s (Cần bán) or u (Thuê))

            Returns:
                    ads_link (str): String of ads's link
    '''
    category_name = unidecode.unidecode(category_name)
    region_name = unidecode.unidecode(region_name).lower()
    area_name = unidecode.unidecode(area_name).lower()

    convert_category_name = {
        'Nha o': 'nha-dat',
        'Can ho/Chung cu': 'can-ho-chung-cu',
        'Dat': 'dat',
        'Van phong, Mat bang kinh doanh': 'van-phong-mat-bang-kinh-doanh',
        'Phong tro': 'phong-tro',
    }
    convert_type = {'s': 'mua-ban', 'u': 'thue'}
    region_name = region_name.replace(' ', '_')
    area_name = area_name.replace(' ', '_')
    ads_link = str('nha.chotot.com/' + region_name + '/' + area_name
                   + '/' + convert_type[type] + '-'
                   + convert_category_name[category_name] + '/'
                   + str(list_id) + '.htm')

    return ads_link

# Function convert unix timestamp to datetime


def print_date(timestamp):
    '''
    Returns date (Format: YYYYMMDD)

            Parameters:
                    timestamp (int): A sequence of characters or encoded information identifying when a certain event occurred,
                    usually giving date and time of day, sometimes accurate to a small fraction of a second.

            Returns:
                    datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d") (str): String of date
    '''

    return datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d")


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


def extract(ads_details):
    '''
    Returns the fields of site

            Parameters:
                    ads_details (dict): Ads's details

            Returns:
                    data (dict): Dictionary of ads's details with key is the fields and value is the field's value
    '''
    data = {}
    if check_key(ads_details['ad'], 'list_id'):
        data['ID_CLIENT'] = str(ads_details['ad']['list_id'])
    data['SITE'] = 'nha.chotot.com'
    data['FOR_SALE'] = 0
    data['FOR_LEASE'] = 0
    data['PRO_FLAG'] = 0 
    if ads_details['ad']['type'] == 's':
        data['FOR_SALE'] = 1
    else:
        data['FOR_LEASE'] = 1
    data['TO_BUY'] = 0
    data['TO_LEASE'] = 0
    data['CREATED_DATE'] = update_date.strftime("%Y-%m-%d")
    data['DATE_ORIGINAL'] = chotot_helper.create_today_string()
    if (check_key(ads_details['ad'], 'category_name')):
        try:
            data['LAND_TYPE'] = ads_details['ad']['category_name']
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad_params'], 'land_type'):
        try:
            data['LAND_TYPE'] = ads_details['ad_params']['land_type'
                                                         ]['value']
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad_params'], 'house_type'):
        try:
            data['LAND_TYPE'] = ads_details['ad_params']['house_type'
                                                         ]['value']
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad_params'], 'apartment_type'):
        try:
            data['LAND_TYPE'] = ads_details['ad_params']['apartment_type'
                                                         ]['value']
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad'], 'list_time'):
        try:
            data['ADS_DATE'] = print_date(ads_details['ad']['list_time'])
            data['ADS_DATE_ORIGINAL'] = ads_details['ad']['list_time']
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad_params'], 'living_size'):
        try:
            surface = ads_details['ad_params']['living_size']['value']
            data['USED_SURFACE_ORIGINAL'] = surface
        except BaseException:
            print("Data Error")

    if check_key(ads_details['ad_params'], 'size'):
        try:
            surface = ads_details['ad_params']['size']['value']
            data['SURFACE_ORIGINAL'] = surface
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad_params'], 'width'):
        try:
            data['PRO_WIDTH'] = (ads_details['ad_params']['width']['value'])[
                0:ads_details['ad_params']['width']['value'].find(' ')]
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad_params'], 'length'):
        try:
            data['PRO_LENGTH'] = (ads_details['ad_params']['length']['value'])[
                0:ads_details['ad_params']['length']['value'].find(' ')]
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad_params'], 'direction'):
        try:
            data['PRO_DIRECTION'] = ads_details['ad_params']['direction']['value']
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad'], 'price_string'):
        try:
            data['PRICE_ORIGINAL'] = ads_details['ad']['price_string']
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad_params'], 'property_legal_document'):
        try:
            data['LEGAL_STATUS'] = ads_details['ad_params'
                                               ]['property_legal_document']['value']
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad_params'], 'floors'):
        try:
            data['NB_FLOORS'] = ads_details['ad_params']['floors']['value']
            if data['NB_FLOORS'].isnumeric() == False:
                data.pop('NB_FLOORS')
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad_params'], 'rooms'):
        try:
            data['BEDROOM'] = (ads_details['ad_params']['rooms']['value'])[
                0:ads_details['ad_params']['rooms']['value'].find(' ')]
            if data['BEDROOM'].isnumeric() == False:
                data.pop('BEDROOM')
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad_params'], 'toilets'):
        try:
            data['TOILET'] = (ads_details['ad_params']['toilets']['value'])[
                0:ads_details['ad_params']['toilets']['value'].find(' ')]
            if data['TOILET'].isnumeric() == False:
                data.pop('TOILET')
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad_params'], 'lproperty_road_condition'):
        try:
            data['ALLEY_ACCESS'] = ads_details['ad_params'
                                               ]['property_road_condition']['value']
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad_params'], 'address'):
        try:
            data['FULL_ADDRESS'] = ads_details['ad_params']['address']['value']
            
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad_params'], 'ward'):
        try:
            data['WARD'] = ads_details['ad_params']['ward']['value']
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad_params'], 'area'):
        try:
            data['DISTRICT'] = ads_details['ad_params']['area']['value']
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad_params'], 'region'):
        try:
            data['CITY'] = ads_details['ad_params']['region']['value']
        except BaseException:
            print("Data Error")
    try:
        data['ADS_LINK'] = create_ads_link(
            data['CITY'],
            data['DISTRICT'],
            ads_details['ad']['category_name'],
            data['ID_CLIENT'],
            ads_details['ad']['type'])
    except BaseException:
        print('Can not create ads link')
    if check_key(ads_details['ad'], 'subject'):
        try:
            data['ADS_TITLE'] = ads_details['ad']['subject']
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad'], 'body'):
        try:
            data['DETAILED_BRIEF'] = ads_details['ad']['body']
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad'], 'images'):
        try:
            data['PHOTOS'] = len(ads_details['ad']['images'])
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad'], 'account_oid'):
        try:
            data['DEALER_ID'] = ads_details['ad']['account_oid']
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad'], 'account_name'):
        try:
            data['DEALER_NAME'] = ads_details['ad']['account_name']
        except BaseException:
            print("Data Error")
    if check_key(ads_details['ad'], 'phone'):
        try:
            data['DEALER_TEL'] = ads_details['ad']['phone']
        except BaseException:
            print("Data Error")

    for (key, value) in data.items():
        if (str(type(value)).find('int') >= 0):
            continue
        data[key] = data[key].replace('\n', '')
        data[key] = data[key].replace('"', '')
        data[key] = data[key].replace("'", "")
        # data[key] = data[key].replace(",","")
        data[key] = data[key].replace(";", "")
        character = ''.join(chr(92))  # chr(92) character in ASCII TABLE is \
        data[key] = data[key].replace(character, '')
        data[key] = delete_icon(data[key])
    return data


def store(ads):
    '''
    Returns SQL command line to insert datas into database

        Parameters:
                ads (dict): The dictionary of ads's fields

        Returns:
                result[0:len(result) - 1] + ' ;' (str): The string of SQL command line
                Example: INSERT IGNORE INTO NHACHOTOT set ID_CLIENT="72113738",SITE="nha.chotot.com",FOR_SALE="1",FOR_LEASE="0",
                TO_BUY="0",TO_LEASE="0",CREATED_DATE="20200826",LAND_TYPE="Đất thổ cư",ADS_DATE="2020-08-26",SURFACE="154",
                SURFACE_UNIT="m2",PRO_WIDTH="6",PRO_LENGTH="30",PRO_DIRECTION="Tây Bắc",PRICE="4.9",PRICE_UNIT="tỷ",LEGAL_STATUS="Đã có sổ",
                FULL_ADDRESS="Đường Mỹ Huề, Xã Trung Chánh, Huyện Hóc Môn, Tp Hồ Chí Minh",STREET="Đường Mỹ Huề",WARD="Xã Trung Chánh",
                DISTRICT="Huyện Hóc Môn",CITY="Tp Hồ Chí Minh",ADS_LINK="nha.chotot.com/tp_ho_chi_minh/huyen_hoc_mon/mua-ban-dat/72113738.htm",
                ADS_TITLE="Bán đất mặt tiền mỹ huề trung chánh hóc môn",
                DETAILED_BRIEF="Bán đất mặt tiền MỸ HUỀ Trung Chánh Hóc Môn*Ngang 6 dài 30 chuyển đất ở 128m2 chuyển cập nhật trang sau * Đường nhựa hiện hữu 12m* Khu dân cư hiện hữu dân cư đông đúc không mồ mả, cách tô ký 100m , đã chuyển lên đất ở cập nhật phía sau !!!",
                PHOTOS="7",DEALER_ID="96f5e8fb2f50288adedb8f312ec44305", DEALER_NAME="Cục Gold",DEALER_TEL="0903340938" ;

    '''
    result = 'INSERT IGNORE INTO NHACHOTOT set '
    for (key, value) in ads.items():
        result += str(key) + '=' + '"' + str(value) + '",'
    return result[0:len(result) - 1] + ' ;'

def update_ads(ads):
    '''
    Returns SQL command line to insert datas into database

        Parameters:
                ads (dict): The dictionary of ads's fields

        Returns:
                result[0:len(result) - 1] + ' ;' (str): The string of SQL command line
                
    '''
    result = 'UPDATE IGNORE NHACHOTOT SET '
    option = '  WHERE ID_CLIENT=' + '"' + str(ads['ID_CLIENT']) + '"'
    for (key, value) in ads.items():
        result += str(key) + '=' + '"' + str(value) + '",'
    return result[0:len(result) - 1] + option + ' ;'


start = time()
update_date = date.today()
folder, today, today_folder, spider_folder, all_folder, delta_folder, list_mode = chotot_helper.create_folder()

file_name = glob.glob(all_folder + '/*.json')
print("Total json files: ", len(file_name))
count_rent = 0
f =  open(delta_folder + '/VO_ANNONCE_insert.sql', 'w+')
fw = open(delta_folder + '/VO_ANNONCE_update.sql', 'w+')


for i in range(0, len(file_name)):
    if os.path.isfile(file_name[i]) == False:
        continue
    print(file_name[i])
    with open(file_name[i], 'r') as file:
        try:
            ads_details = json.load(file, encoding='utf-8')
            print(
                "Read json data successfully ",
                i + 1,
                ads_details['ad']['list_id'])
        except BaseException:
            print('Fail', i + 1)
    file.close()
    if (ads_details['ad']['type'] !=
            's' and ads_details['ad']['type'] != 'u'):
        print("Passed Data Illegal", ads_details['ad']['type'], i + 1)
        count_rent = count_rent + 1
        continue
    ads = extract(ads_details)
    if len(ads['ID_CLIENT']) > 0:
        # WRITE SQL FILE INTO VO_ANNOUNCE_INTO.SQL
        f.write(store(ads) + '\n')
        fw.write(update_ads(ads) + '\n')


f.close()
fw.close()
print('DONE PUT JSON INTO DELTA AND CREATE FILE INSERT SQL')
print('Rent is ', count_rent)
delta = time()
print('------%s SECONDS-------' % (delta - start))

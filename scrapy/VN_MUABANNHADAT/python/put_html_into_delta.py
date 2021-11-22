#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import glob
from time import time
from os import path
import muabannhadat_helper
import codecs
from lxml import etree
from io import StringIO, BytesIO
from bs4 import BeautifulSoup

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


def extract(html_file):
    '''
    Returns the fields of site
            Parameters:
                    html_file (string): File html contains ads's details

            Returns:
                    data (dict): Dictionary of ads's details with key is the fields and value is the field's value
    '''
    data = {}
    ads_details = []
    content_file = codecs.open(html_file, 'r')
    soup = BeautifulSoup(content_file, 'lxml')
    id_client = soup.find(
        "span", class_='text-lg md:text-2xl inline font-bold')
    if (str(type(id_client)).find('None') < 0):
        id_client = delete_special_character(id_client.get_text())
        id_client = id_client[id_client.find(':') + 1:id_client.find(')')]
        data['ID_CLIENT'] = id_client
    data['SITE'] = 'muabannhadat.vn'
    data['CREATED_DATE'] = today
    data['DATE_ORIGINAL'] = today
    data['FOR_SALE'] = 0
    data['FOR_LEASE'] = 0
    data['PRO_FLAG'] = 0 
    data['DISTRICT'] = ""
    land_type = soup.select(
        'ul.items-center > li:nth-child(2) > a:nth-child(2)')
    if len(land_type) > 0:
        land_type = land_type[0]
        if (str(type(land_type)).find('None') < 0):
            land_type = delete_special_character(land_type.get_text())
            if land_type.find('thuê') >= 0:
                data['FOR_LEASE'] = 1
                land_type = land_type[land_type.find(
                    'ê') + 2:len(land_type)]  # ê trong thuê
            else:
                data['FOR_SALE'] = 1
                land_type = land_type[land_type.find(
                    'n') + 2:len(land_type)]  # n trong mua bán
            data['LAND_TYPE'] = land_type
    used_surface = soup.find("span", attrs={
        "aria-label": "area"})
    if (str(type(used_surface)).find('None') < 0):
        used_surface = delete_special_character(used_surface.get_text())
        data['USED_SURFACE_ORIGINAL'] = used_surface
    bedroom = soup.find("span", attrs={
        "aria-label": "bedrooms"})
    if (str(type(bedroom)).find('None') < 0):
        bedroom = delete_special_character(bedroom.get_text())
        data['BEDROOM'] = bedroom
    pro_direction = soup.find("span", attrs={
        "aria-label": "direction"})
    if (str(type(pro_direction)).find('None') < 0):
        pro_direction = delete_special_character(pro_direction.get_text())
        data['PRO_DIRECTION'] = pro_direction
    bathroom = soup.find("span", attrs={
        "aria-label": "bathrooms"})
    if (str(type(bathroom)).find('None') < 0):
        bathroom = delete_special_character(bathroom.get_text())
        data['BATHROOM'] = bathroom
    full_address = soup.find("h4", attrs={"data-cy": "listing-address"})
    if (str(type(full_address)).find('None') < 0):
        full_address = delete_special_character(full_address.get_text())
        data['FULL_ADDRESS'] = full_address
    
    city = soup.select("ul.items-center > li:nth-child(3) > a:nth-child(2)")
    if len(city) > 0:
        city = delete_special_character(city[0].get_text())
        data['CITY'] = city
    ads_link = soup.find(
        "meta",
        attrs={
            "data-vmid": "og:url",
            "property": "og:url"})
    if (str(type(ads_link)).find('None') < 0):
        data['ADS_LINK'] = ads_link['content']
    ads_title = soup.find("h1", attrs={"data-cy": "listing-heading"})
    if (str(type(ads_title)).find('None') < 0):
        ads_title = delete_special_character(ads_title.get_text())
        data['ADS_TITLE'] = ads_title
    brief = soup.find("h2", attrs={"data-cy": "listing-title"})
    if (str(type(brief)).find('None') < 0):
        brief = delete_special_character(brief.get_text())
        data['BRIEF'] = brief
    detailed_brief = soup.find(
        "div", class_="mb-2 leading-normal text-justify")
    if (str(type(detailed_brief)).find('None') < 0):
        detailed_brief = delete_special_character(detailed_brief.get_text())
        data['DETAILED_BRIEF'] = detailed_brief
    photos = soup.find(
        "div",
        class_="flex h-auto overflow-y-hidden overflow-x-scroll gallery_scroller relative items-center")
    if (str(type(photos)).find('None') < 0):
        data['PHOTOS'] = len(photos)
    dealer_name = soup.find(
        "p", class_='text-center my-2 break-words font-semibold mb-4')
    if (str(type(dealer_name)).find('None') < 0):
        dealer_name = delete_special_character(dealer_name.get_text())
        data['DEALER_NAME'] = dealer_name
    pro_utilities_tag = soup.find(
        "ul", class_="list-reset flex flex-wrap justify-between")  # .find_all("li")
    if (str(type(pro_utilities_tag)).find('None') < 0):
        pro_utilities = ''
        pro_utilities_tag = pro_utilities_tag.find_all("li")
        for text in pro_utilities_tag:
            pro_utilities = pro_utilities + \
                delete_special_character(text.get_text()) + ', '
        pro_utilities = pro_utilities[0:len(pro_utilities) - 2]
        data['PRO_UTILITIES'] = pro_utilities
        if pro_utilities.find("Siêu thị") >= 0:
            data['SUPERMARKET'] = 1
        if pro_utilities.find("Bệnh viện") >= 0:
            data['HOSPITAL'] = 1
        if pro_utilities.find("Công viên") >= 0:
            data['PARK'] = 1
        if pro_utilities.find("Trường học") >= 0:
            data['SCHOOL'] = 1
    price = soup.find("span", attrs={"aria-label": "price"})
    if str(type(price)).find('None') < 0:
        price = delete_special_character(price.get_text())
        data['PRICE_ORIGINAL'] = price
    ul_tag = soup.find_all(
        "ul", attrs={
            "class": "list-reset flex flex-wrap md:-mr-5"})
    if len(ul_tag) > 0:
        for li_tag in ul_tag[0].find_all('li'):
            span_tag = li_tag.find_all('span')
            text_of_span_tag_1 = delete_special_character(span_tag[0].get_text())
            text_of_span_tag_2 = delete_special_character(span_tag[1].get_text())
            ads_details.append((text_of_span_tag_1, text_of_span_tag_2))
    for i in range(0, len(ads_details)):
        if ads_details[i][0].find('Ngày đăng') >= 0:
            data['ADS_DATE_ORIGINAL'] = ads_details[i][1]
            date = ads_details[i][1].split('/')
            data['ADS_DATE'] = date[2] + '-' + date[0] + '-' + date[1]
        if (ads_details[i][0].find('Bề dài') >= 0):
            data['PRO_LENGTH'] = (ads_details[i][1])[
                0:ads_details[i][1].find('m')]
        if (ads_details[i][0].find('Bề rộng') >= 0):
            data['PRO_WIDTH'] = (ads_details[i][1])[
                0:ads_details[i][1].find('m')]
        if (ads_details[i][0].find('Số tầng') >= 0):
            data['NB_FLOORS'] = ads_details[i][1]
        if (ads_details[i][0].find('Pháp lý') >= 0):
            data['LEGAL_STATUS'] = ads_details[i][1]
    phone_number_hide = soup.find("button", attrs={"data-cy": "phone-button"})
    if str(type(phone_number_hide)).find('None') < 0:
        phone_number_hide = delete_special_character(
            phone_number_hide.get_text())
        phone_number_hide = phone_number_hide.replace(" ", "")
        phone_number_hide = phone_number_hide.replace('*', '')
        phone_number_position = soup.prettify().find(phone_number_hide)
        phone_number = soup.prettify()[
            phone_number_position:phone_number_position + 15]
        str_phone_number = '+84'
        for i in range(3, len(phone_number)):
            if phone_number[i].isnumeric():
                str_phone_number = str_phone_number + phone_number[i]
        data['DEALER_TEL'] = str_phone_number
    for (key, value) in data.items():
        if (str(type(value)).find('int') >= 0):
            continue
        # data[key] = delete_special_character(data[key])
        data[key] = delete_icon(data[key])
    return data


def store(ads):
    '''
    Returns SQL command line to insert datas into database

        Parameters:
                ads (dict): The dictionary of ads's fields

        Returns:
                result[0:len(result) - 1] + ' ;' (str): The string of SQL command line

    '''
    result = 'INSERT IGNORE INTO MUABANNHADAT set '
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
    result = 'UPDATE MUABANNHADAT set '
    option = ""
    if 'ID_CLIENT' in ads:
        option = '  WHERE ID_CLIENT=' + '"' + str(ads['ID_CLIENT']) + '"'
    for (key, value) in ads.items():
        result += str(key) + '=' + '"' + str(value) + '",'
    return result[0:len(result) - 1] + option + ' ;'


start = time()

folder, today, today_folder, spider_folder, all_folder, delta_folder, list_mode, sale_folder, lease_folder = muabannhadat_helper.create_folder()

html_files = glob.glob(all_folder + '/*.html')  # Total html files in ALL folder

print("Total html files:", len(html_files))
f =  open(delta_folder + '/VO_ANNONCE_insert.sql', 'w+')
fw = open(delta_folder + '/VO_ANNONCE_update.sql', 'w+')



for i in range(0, len(html_files)):
    if os.path.isfile(html_files[i]) == False:
        continue
    print(i + 1, html_files[i])
    ads = extract(html_files[i])
    try:
        if len(ads['ID_CLIENT']) > 0:
            #   WRITE SQL FILE INTO VO_ANNOUNCE_INTO.SQL
            f.write(store(ads) + '\n')
            fw.write(update_ads(ads) + '\n')
    except:   
        pass

f.close()
fw.close()

print('DONE PUT HTML INTO DELTA AND CREATE FILE INSERT SQL')
delta = time()
print('------%s SECONDS-------' % (delta - start))

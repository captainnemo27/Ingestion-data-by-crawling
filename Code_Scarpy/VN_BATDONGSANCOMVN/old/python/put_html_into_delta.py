#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import glob
from time import time
from os import path
import batdongsancomvn_helper
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
    data['SITE'] = 'batdongsan.com.vn'
    data['CREATED_DATE'] = today
    data['FOR_SALE'] = 0
    data['FOR_LEASE'] = 0
    data['TO_BUY'] = 0
    data['TO_LEASE'] = 0
    data['PRO_FLAG'] = 0 
    category = soup.find("div", class_="breadcrumb all-grey-7 link-hover-blue")
    if str(type(category)).find('None') < 0:
        if category.get_text().find('Bán') > -1:
            data['FOR_SALE'] = 1
        if category.get_text().find('Cho thuê') > -1:
            data['FOR_LEASE'] = 1
    else:
        try:
            category = soup.find(
                "div", class_='kqchitiet').find(
                "strong", class_='greencolor')
            if category.get_text().find("Mua") > -1:
                data['TO_BUY'] = 1
            else:
                data['TO_LEASE'] = 1
        except:
            print("Has no land type (to_buy and to_lease).")
            pass
    try:
        ads_link = soup.find('link', attrs={"rel": "alternate"})['href']
        if str(type(ads_link)).find('None') < 0:
            data['ADS_LINK'] = ads_link.replace('m.', '', 1)
    except:
        print("Cannot take ads_link")
        pass
    #==================================================#
    if data['FOR_SALE'] == 1 or data['FOR_LEASE'] == 1:
        short_detail = soup.find(
            "ul",
            class_='short-detail-2 list2 clearfix').find_all("span")  # ID_CLIENT, ADS_DATE
        for i in range(0, len(short_detail), 2):
            ads_details.append(
                (short_detail[i].get_text(), short_detail[i + 1].get_text()))

        title_detail = soup.find_all("div", class_="box-round-grey3")
        for i in range(0, len(title_detail)):
            span_tag = title_detail[i].find_all("span", class_={"r1", "r2"})
            for i in range(0, len(span_tag), 2):
                ads_details.append(
                    (span_tag[i].get_text(), span_tag[i + 1].get_text()))
        # PRICE, PRICE_UNIT, USED_SURFACE, BEDROOM
        short_detail = soup.find(
            "ul", class_="short-detail-2 clearfix pad-16").find_all("span")
        for i in range(0, len(short_detail), 2):
            ads_details.append(
                (short_detail[i].get_text(), short_detail[i + 1].get_text()))
        for i in range(0, len(ads_details)):
            if ads_details[i][0].find('Mã tin') >= 0:
                data['ID_CLIENT'] = ads_details[i][1]
            if ads_details[i][0].find('Loại tin đăng') >= 0:
                data['LAND_TYPE'] = ads_details[i][1].replace('Bán ', '')
                data['LAND_TYPE'] = ads_details[i][1].replace('Cho thuê ', '')
            if ads_details[i][0].find('Ngày đăng') >= 0:
                data['ADS_DATE'] = ads_details[i][1]
            if ads_details[i][0].find('Diện tích') >= 0:
                data['USED_SURFACE'] = ads_details[i][1].replace(' m²', '')
                data['USED_SURFACE'] = data['USED_SURFACE'].replace(
                    "Trên ", "")
                data['USED_SURFACE'] = data['USED_SURFACE'].replace(
                    "Dưới ", "")
                data['USED_SURFACE'] = data['USED_SURFACE'].replace(" ", "")
                data['USED_SURFACE'] = data['USED_SURFACE'].replace(' ', '')
                if data['USED_SURFACE'].find('-') > -1:
                	data['USED_SURFACE'] = data['USED_SURFACE'][data['USED_SURFACE'].find('-') + 1 : len(data['USED_SURFACE'])]
                data['USED_SURFACE_UNIT'] = 'm2'
            if ads_details[i][0].find('Hướng nhà') >= 0:
                data['PRO_DIRECTION'] = ads_details[i][1]
            if ads_details[i][0].find('Mức giá') >= 0:
                data['PRICE'] = ads_details[i][1]
                # data['PRICE'] = data['PRICE'].replace("  ", "")
                if data['PRICE'][0] == ' ':
                    data['PRICE'] = data['PRICE'].replace(" ", "", 1)
                if data['PRICE'].find("Thỏa thuận") >= 0:
                    data['PRICE'] = 0
                else:
                    data['PRICE_UNIT'] = data['PRICE'][data['PRICE'].find(
                        " ") + 1: len(data['PRICE'])]
                    data['PRICE'] = data['PRICE'][0:data['PRICE'].find(" ")]
            if ads_details[i][0].find('Pháp lý') >= 0:
                data['LEGAL_STATUS'] = ads_details[i][1]
            if ads_details[i][0].find('Số tầng') >= 0:
                data['NB_FLOORS'] = ads_details[i][1].replace(' (tầng)', '')
            if ads_details[i][0].find('Số phòng ngủ') >= 0:
                data['BEDROOM'] = ads_details[i][1].replace(" (phòng)", '')
            if ads_details[i][0].find('toilet') >= 0:
                data['TOILET'] = ads_details[i][1].replace(" (phòng)", '')
            if ads_details[i][0].find('Mặt tiền') >= 0:
                data['FRONTAGE'] = ads_details[i][1]
                data['FRONTAGE'] = data['FRONTAGE'][0:data['FRONTAGE'].find(
                    ' ')]
                data['FRONTAGE'] = data['FRONTAGE'].replace(",","")
            if ads_details[i][0].find('Địa chỉ') >= 0:
                data['FULL_ADDRESS'] = ads_details[i][1]
                full_address = ads_details[i][1].split(', ')
                if len(full_address) > 1:
                    data['DISTRICT'] = full_address[-2]
                if len(full_address) > 0:
                    data['CITY'] = full_address[-1]
            if ads_details[i][0].find('Tên dự án') >= 0:
                data['PROJECT_NAME'] = ads_details[i][1].replace('·', '')
                data['PROJECT_NAME'] = data['PROJECT_NAME'].replace(
                    'Xem dự án', '')
                data['PROJECT_NAME'] = delete_special_character(
                    data['PROJECT_NAME'])
        coordinates_detail = soup.find(
            "div", class_='map').find('iframe')['src']
        if str(type(coordinates_detail)).find('None') < 0:
            latitude = coordinates_detail[coordinates_detail.find(
                "q=") + 2: coordinates_detail.find(',')]
            longitude = ''
            for i in range(
                    coordinates_detail.find(',') + 1,
                    len(coordinates_detail)):
                if coordinates_detail[i].isnumeric(
                ) == False and coordinates_detail[i] != '.':
                    break
                longitude = longitude + coordinates_detail[i]
        detailed_brief = soup.find('div', class_='des-product')
        if str(type(detailed_brief)).find('None') < 0:
            data['DETAILED_BRIEF'] = detailed_brief.get_text()
            data['DETAILED_BRIEF'] = delete_special_character(
                data['DETAILED_BRIEF'])
        try:
            photos = soup.select(".gallery-thumbs > div:nth-child(1)")
            if len(photos) > 0:
                data['PHOTOS'] = len(photos[0].find_all("div"))
        except BaseException:
            print("NO PHOTOS")
        try:
            dealer_name = soup.find(
                "div", class_='user').find(
                'div', class_='name')
            if str(type(dealer_name)).find('None') < 0:
                data['DEALER_NAME'] = dealer_name.get_text()
        except BaseException:
            print("Dont have name of dealer")
        try:
            dealer_tel = soup.find("div", class_='user').find(
                'div', class_='phone text-center').find("span")['raw']
            if str(type(dealer_tel)).find('None') < 0:
                data['DEALER_TEL'] = dealer_tel
        except BaseException:
            print("Dont have phone of dealer")
        try:
            dealer_email = soup.find(
                "div", class_="mail btn-border-grey text-center").find('a')['data-email']
            if str(type(dealer_email)).find('None') < 0:
                data['DEALER_EMAIL'] = dealer_email
        except BaseException:
            print("Dont have email of dealer")
        try:
            mini_site = soup.find(
                "div", class_='user').find(
                'div', class_='info').find('a')['href']
            if str(type(mini_site)).find('None') < 0:
                data['MINI_SITE'] = 'https://batdongsan.com.vn' + mini_site
        except BaseException:
            print("Dont have minisite of dealer")
    else:
        # ================== TO BUY TO LEASE =======================
        photos = soup.select("#thumbs")
        if len(photos) > 0:
            photos = photos[0].find_all("img")
            data['PHOTOS'] = len(photos)
        try:
            title_detail = soup.find("div",
                                    class_='left-detail').find_all('div',
                                                                    class_={'left',
                                                                            'right'})  # Address, land_type, id_client
            for i in range(0, len(title_detail), 2):
                if title_detail[i].get_text().find("Địa chỉ") >= 0:
                    ads_details.append(
                        ("Địachỉ bds", title_detail[i + 1].get_text()))    
                else:
                    ads_details.append(
                        (title_detail[i].get_text(), title_detail[i + 1].get_text()))
        except:
            print("No title detail")
            pass
        try:
            customer_info = soup.find(
                "div", attrs={
                    'id': 'divCustomerInfoAd'}).find_all(
                'div', class_={
                    'normalblue left', 'right'})
            if str(type(customer_info)).find('None') < 0:
                for i in range(0, len(customer_info), 2):
                    ads_details.append(
                        (customer_info[i].get_text(), customer_info[i + 1].get_text()))
        except:
            print("No customer info")
            pass
        detailed_brief = soup.find("div", class_='pm-content stat')
        if str(type(detailed_brief)).find('None') < 0:
            data['DETAILED_BRIEF'] = detailed_brief.get_text()
            data['DETAILED_BRIEF'] = delete_special_character(
                data['DETAILED_BRIEF'])
        try:
            price = soup.find(
                'span', class_='gia-title mar-right-15').find("strong")
            if str(type(price)).find('None') < 0:
                price = price.get_text()
                price = price.replace('Dưới ', '')
                price = price.replace('Trên ', '')
                # data['PRICE'] = price
                if price.find("Thỏa thuận") >= 0:
                    data['PRICE'] = 0
                elif price.find('-') >= 0:
                    data['PRICE'] = price[price.find(
                        '-') + 2: price.find(' ', price.find('-') + 2, len(price))]
                    data['PRICE_UNIT'] = price[price.find(
                        ' ') + 1: price.find("-") - 1]
                else:
                    data['PRICE'] = price[0:price.find(' ')]
                    data['PRICE_UNIT'] = price[price.find(' ') + 1: len(price)]
        except:
            print("No price")
            pass
        used_surface = soup.select(
            "span.gia-title:nth-child(2) > strong:nth-child(2)")
        if len(used_surface) > 0:
            used_surface = used_surface[0].get_text()
            if used_surface.find("Không xác định") >= 0:
                data['USED_SURFACE'] = 0
            else:
                if used_surface.find('m') >= 0:
                    data['USED_SURFACE_UNIT'] = 'm2'
                data['USED_SURFACE'] = used_surface
                data['USED_SURFACE'] = data['USED_SURFACE'].replace(
                    "Trên ", "")
                data['USED_SURFACE'] = data['USED_SURFACE'].replace(
                    "Dưới ", "")
                data['USED_SURFACE'] = data['USED_SURFACE'].replace("m²", '')
                data['USED_SURFACE'] = data['USED_SURFACE'].replace(" ", "")
                data['USED_SURFACE'] = data['USED_SURFACE'].replace(' ', '')
                if data['USED_SURFACE'].find('-') > -1:
                	data['USED_SURFACE'] = data['USED_SURFACE'][data['USED_SURFACE'].find('-') + 1 : len(data['USED_SURFACE'])]

        for i in range(0, len(ads_details)):
            if ads_details[i][0].find("Địachỉ bds") >= 0:
                data['FULL_ADDRESS'] = ads_details[i][1].replace('  ', '')
            if ads_details[i][0].find("Địa chỉ") >= 0:
                data['DEALER_ADDRESS'] = ads_details[i][1].replace('  ', '')
            if ads_details[i][0].find("Mã số") >= 0:
                data['ID_CLIENT'] = ads_details[i][1]
            if ads_details[i][0].find("Loại tin rao") >= 0:
                data['LAND_TYPE'] = ads_details[i][1].replace("Cần thuê ", "")
                data['LAND_TYPE'] = ads_details[i][1].replace("Mua ", "")
                data['LAND_TYPE'] = ads_details[i][1].replace("Cần thuê ", "")
            if ads_details[i][0].find("Ngày đăng tin") >= 0:
                data['ADS_DATE'] = ads_details[i][1]
            if ads_details[i][0].find("Tên liên lạc") >= 0:
                data['DEALER_NAME'] = ads_details[i][1]
            if ads_details[i][0].find("Mobile") >= 0:
                data['DEALER_TEL'] = ads_details[i][1]
            if ads_details[i][0].find("Email") >= 0:
                data['DEALER_EMAIL'] = ads_details[i][1].replace(
                    "Địa chỉ email này được bảo vệ bởi JavaScript.Bạn cần kích hoạt Javascript để có thể xem.", "")
        # city = soup.select(".diadiem")
        # if len(city) > 0:
        #     data['CITY'] = city[0].contents[len(city[0]) - 1]
        #     data['CITY'] = data['CITY'].replace(' - ', ', ')
        #     data['CITY'] = data['CITY'].replace(', ','',1)
    for (key, value) in data.items():
        if (str(type(value)).find('int') >= 0):
            continue
        data[key] = delete_special_character(data[key])
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
    result = 'INSERT IGNORE INTO BATDONGSANCOMVN set '
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
    result = 'UPDATE BATDONGSANCOMVN set '
    option = '  WHERE ID_CLIENT=' + '"' + str(ads['ID_CLIENT']) + '"'
    for (key, value) in ads.items():
        result += str(key) + '=' + '"' + str(value) + '",'
    return result[0:len(result) - 1] +  option + ' ;'

start = time()

folder, today, today_folder, all_folder, delta_folder, list_mode, sale_folder, lease_folder, to_buy_to_lease_folder = batdongsancomvn_helper.create_folder()
# Total html files in ALL folder
html_files = glob.glob(all_folder + '/*.html')
print("Total html files:", len(html_files))
f =  open(delta_folder + '/VO_ANNONCE_insert.sql', 'w+')
fw = open(delta_folder + '/VO_ANNONCE_update.sql', 'w+')


for i in range(0, len(html_files)):
# for i in range(0, 1):
    if os.path.isfile(html_files[i]) == False:
        continue
    # html_files[i] = '/media/hoangthongvo/3A0477200476DDF7/oreal-crawling/VN_BATDONGSANCOMVN/20200911/ALL/102090.html'
    print(i + 1, html_files[i])
    ads = extract(html_files[i])

    #   WRITE SQL FILE INTO VO_ANNOUNCE_INTO.SQL
    if len(ads['ID_CLIENT']) > 0:
        f.write(store(ads) + '\n')
        fw.write(update_ads(ads) + '\n')

f.close()
fw.close()
print('DONE PUT HTML INTO DELTA AND CREATE FILE INSERT SQL')
delta = time()
print('------%s SECONDS-------' % (delta - start))

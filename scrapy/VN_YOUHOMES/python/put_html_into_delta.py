#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import glob
from time import time
from os import path
import youhomes_helper
import codecs
from lxml import etree
from io import StringIO, BytesIO
from bs4 import BeautifulSoup
from datetime import datetime, date

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
    try:
        data['PRO_FLAG'] = 0 
        for li_tag in soup.select("#content > div.topicpath.bread_crumbs > ul")[
                0].find_all('li'):
            if li_tag.get_text().find("BAN") >= 0 or li_tag.get_text().find("THUE") >= 0:
                data['ID_CLIENT'] = li_tag.get_text()
        data['SITE'] = 'youhomes.vn'
        data['CREATED_DATE'] = update_date.strftime("%Y-%m-%d")
        data['DATE_ORIGINAL'] = today
        data['FOR_SALE'] = 0
        data['FOR_LEASE'] = 0
    except:
        pass
    if check_key(data,'ID_CLIENT') and data['ID_CLIENT'].find('BAN') >= 0:
        data['FOR_SALE'] = 1
    if check_key(data,'ID_CLIENT') and data['ID_CLIENT'].find('THUE') >= 0:
        data['FOR_LEASE'] = 1
    price = soup.select('.row-price-sc > div:nth-child(2)')
    if (len(price) > 0):
        price = price[0].get_text()
        data['PRICE_ORIGINAL'] = price
    else:
        price = soup.select('.left-top-price > b:nth-child(2)')
        if (len(price) > 0):
            price = price[0].get_text()
            data['PRICE_ORIGINAL'] = price
    try:
        for p_tag in soup.select('#content > div.row.overview')[
                0].find_all('p'):
            ads_details.append(
                (p_tag.contents[0], p_tag.contents[1].get_text()))
    except BaseException:
        print("Apartment Detail Ads")
    pro_utilities = ''
    try:
        for li_tag in soup.select('.list-utility-around')[0].find_all('li'):
            pro_utilities = pro_utilities + li_tag.get_text() + ','
    except BaseException:
        print("Special pro_utilities Ads")
    pro_utilities = pro_utilities[0:len(pro_utilities) - 1]
    data['PRO_UTILITIES'] = pro_utilities
    try: 
        full_address = soup.select(
            '#content > div.product-title > div > div')[0].find('span').contents[0]
        data['FULL_ADDRESS'] = full_address
      
    except BaseException:
        print("No full address")
    try:
        ads_link = soup.find(attrs={"rel": "canonical"})['href']
        data['ADS_LINK'] = ads_link
    except: 
        print("No ads link")
    try: 
        data['ADS_TITLE'] = soup.select(
            "#content > div.product-title > div > h1")[0].get_text()
    except BaseException:
        print("No ads title")
    try:
        data['DETAILED_BRIEF'] = soup.select(
            '#content > div.description > p')[0].get_text()
    except BaseException:
        print("Special detailed_brief ads")
    try:
        photos = soup.select("#content > div.item > div")[0].find_all("li")
        data['PHOTOS'] = len(photos)
    except BaseException:
        print("NO PHOTOS")
    try:
        data['DEALER_NAME'] = soup.select('.name-employees-cs')[0].get_text()
    except BaseException:
        print("NO DEADLER_NAME")
    if pro_utilities.find("Siêu thị") >= 0:
        data['SUPERMARKET'] = 1
    if pro_utilities.find("Bệnh viện") >= 0:
        data['HOSPITAL'] = 1
    if pro_utilities.find("Công viên") >= 0:
        data['PARK'] = 1
    if pro_utilities.find("Trường học") >= 0:
        data["SCHOOL"] = 1
    for i in range(0, len(ads_details)):
        if ads_details[i][0].find('Loại căn hộ') >= 0:
            data['LAND_TYPE'] = ads_details[i][1]
        if (ads_details[i][0].find('Diện tích xây dựng') >=
                0 or ads_details[i][0].find('Diện tích') >= 0):
            data['USED_SURFACE_ORIGINAL'] = ads_details[i][1]
        if (ads_details[i][0].find('Diện tích đất') >= 0):
            data['SURFACE_ORIGINAL'] = ads_details[i][1]
        if (ads_details[i][0].find('Chiều dài mảnh đất') >= 0):
            data['PRO_LENGTH'] = (ads_details[i][1])[
                0:ads_details[i][1].find(' ')]
        if ads_details[i][0].find('Hướng nhà') >= 0 or ads_details[i][0].find(
                'Hướng bán công') >= 0 or ads_details[i][0].find('Hướng') >= 0:
            data['PRO_DIRECTION'] = ads_details[i][1]
        if (ads_details[i][0].find('Pháp lý') >= 0):
            data['LEGAL_STATUS'] = ads_details[i][1]
            data['LEGAL_STATUS'] = data['LEGAL_STATUS'].replace('-', '')
        if (ads_details[i][0].find('Số tầng') >= 0):
            if (ads_details[i][1].replace('-', '') != ""):
                data['NB_FLOORS'] = ads_details[i][1].replace('-', '')
        if (ads_details[i][0].find('Số phòng ngủ') >=
                0 or ads_details[i][0].find('Phòng ngủ') >= 0):
            number_bedroom = ''
            for char in ads_details[i][1]:
                if char.isnumeric() == False:
                    break
                number_bedroom = number_bedroom + char
            if (number_bedroom != ""):
                data['BEDROOM'] = number_bedroom
        if (ads_details[i][0].find("Số phòng vệ sinh")
                >= 0 or ads_details[i][0].find("WC") >= 0):
            data['TOILET'] = ads_details[i][1]
        if ads_details[i][0].find("Mặt tiền") >= 0:
            if (ads_details[i][1])[0:ads_details[i][1].find(' ')].replace('-', '') != "" :
                data['FRONTAGE'] = ads_details[i][1]
            
    if check_key(data, 'LAND_TYPE') and data['LAND_TYPE'].find("Căn hộ") >= 0:
        try:
            data['PROJECT_NAME'] = soup.select(
                '#content > div.topicpath.bread_crumbs > ul > li:nth-child(7) > a')[0].get_text()
        except BaseException:
            print("No project name")
    for (key, value) in data.items():
        if (str(type(value)).find('int') >= 0):
            continue
        data[key] = delete_special_character(data[key])
    return data


def store(ads):
    '''
    Returns SQL command line to insert datas into database

        Parameters:
                ads (dict): The dictionary of ads's fields

        Returns:
                result[0:len(result) - 1] + ' ;' (str): The string of SQL command line
                Example:
                INSERT IGNORE INTO YOUHOMES set ID_CLIENT="BAN23653",SITE="youhomes.vn",CREATED_DATE="20200827",FOR_SALE="1",FOR_LEASE="0",PRICE="9.9",
                PRICE_UNIT="tỷ",PRO_UTILITIES="Trường học ,Bệnh viện ,Siêu thị ,Cây ATM ,Công viên ",FULL_ADDRESS="NGUYỄN CẢNH CHÂN, Cầu Kho, Quận 1, Tp Hồ Chí Minh ",
                STREET="NGUYỄN CẢNH CHÂN",WARD=" Cầu Kho",DISTRICT=" Quận 1",CITY=" Tp Hồ Chí Minh ",
                ADS_LINK="https://youhomes.vn/ban/23653-nha-rieng-nguyen-canh-chan-quan-1-39m2-nhieu-anh-sang.html",
                ADS_TITLE=" Bán nhà riêng NGUYỄN CẢNH CHÂN Quận 1 - 39m2 - Nhiều ánh sáng",
                DETAIL_BRIEF="- Chính chủ cần bán nhà xx/27 Nguyễn Cảnh Chân, Q1, cách mặt tiền Trần Hưng Đạo 40m- Kết cấu: 1 trệt, 1 lửng, 3 lầu, 1 sân thượng, sân phơi đồ, trồng rau, cây cảnh thoải mái- Nhà xây từ 2011, vuông vức, cực kiên cố, - Nội thất tiện nghi đầy đủ, dọn vào ở ngay ko cần chỉnh sửa- Hẻm cụt nên rất yên tĩnh, hẻm rộng rãi, - Nằm ngay vị trí trung tâm nên dễ dàng di chuyển giữa Q5, Q1, Q8 gần Nguyễn Văn Cừ, Công An TP, Bệnh viện, Trường học, Phố Tây Bùi Viện, Chợ Bến Thành, Trung Tâm Phố đi bộ Quận 1.- Thích hợp gia đình dọn vào ở ngay, cho thuê AirBnB, bán hàng online..... - Giấy tờ pháp lý, sổ hồng chính chủ, giấy hoàn công rõ ràng. - Gía bán có thương lượng,=> Liên hệ tôi chính chủ (Bán nhà riêng NGUYỄN CẢNH CHÂN Quận 1 - 39m2 - Nhiều ánh sáng - Mua nhà riêng dưới 10 tỷ) ",
                PHOTOS="6",DEALER_NAME="Phạm Lợi (chủ nhà)",AGENCY_WEBSITE="youhomes.vn",AGENCY_NAME="Công Ty TNHH CT Toàn Cầu",
                AGENCY_ADDRESS="Tầng 12 toà Hồ Gươm Plaza, 102 Trần Phú, Phường Mộ Lao, Hà Đông, Hà Nội + VPKD Hà Nội: Toà C2, Vinhomes DCapitale, 119 Trần Duy Hưng, Cầu Giấy, Hà Nội + VPKD HCM: Toà Indocchina Park Tower, Nguyễn Đình Chiểu, Quận 1, TP HCM",AGENCY_CITY="Hà Nội, Hồ Chí Minh",
                AGENCY_TEL="0968654865",SUPERMARKET="1",HOSPITAL="1",PARK="1",SCHOOL="1",LAND_TYPE="Nhà riêng",USED_SURFACE="195",USED_SURFACE_UNIT="m2",
                SURFACE="39",SURFACE_UNIT="m2",FRONTAGE="3",NB_FLOORS="3", LEGAL_STATUS="Sổ hồng",PRO_DIRECTION="Tây Nam",PRO_LENGTH="13",BEDROOM="5",TOILET="3" ;
    '''
    result = 'INSERT IGNORE INTO YOUHOMES set '
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
                Example:
                UPDATE YOUHOMES set ID_CLIENT="BAN23653",SITE="youhomes.vn",CREATED_DATE="20200827",FOR_SALE="1",FOR_LEASE="0",PRICE="9.9" WHERE ID_CLIENT="BAN23653" ;
    '''
    result = 'UPDATE IGNORE YOUHOMES set '
    option = '  WHERE ID_CLIENT=' + '"' + str(ads['ID_CLIENT']) + '"'
    for (key, value) in ads.items():
        result += str(key) + '=' + '"' + str(value) + '",'
    return result[0:len(result) - 1] + option + ' ;'


start = time()
update_date = date.today()
folder, today, today_folder, spider_folder, all_folder, delta_folder, list_mode, sale_folder, lease_folder, house_sale_folder, apartment_sale_folder, house_lease_folder, apartment_lease_folder = youhomes_helper.create_folder()

html_files = glob.glob(all_folder + '/*.html')  # Total html files in ALL folder

print("Total html files:", len(html_files))
f =  open(delta_folder + '/VO_ANNONCE_insert.sql', 'w+')
fw = open(delta_folder + '/VO_ANNONCE_update.sql', 'w+')
for i in range(0, len(html_files)):
    if os.path.isfile(html_files[i]) == False:
        continue
    print(i + 1, html_files[i])
    ads = extract(html_files[i])
    if len(ads['ID_CLIENT']) > 0:
        #   WRITE SQL FILE INTO VO_ANNOUNCE_INTO.SQL
        f.write(store(ads) + '\n')
        fw.write(update_ads(ads) + '\n')
f.close()
fw.close()
print('DONE PUT HTML INTO DELTA AND CREATE FILE INSERT SQL')
delta = time()
print('------%s SECONDS-------' % (delta - start))
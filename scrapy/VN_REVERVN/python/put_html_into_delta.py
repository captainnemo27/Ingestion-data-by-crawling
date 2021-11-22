#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import glob
from time import time
from datetime import datetime, date
from os import path
import revervn_helper
import codecs
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


def extract(html_file):
    '''
    Returns the fields of site
            Parameters:
                    html_file (string): File html contains ads's details

            Returns:
                    data (dict): Dictionary of ads's details with key is the fields and value is the field's value
    '''

    content_file = codecs.open(html_file, 'r')
    soup = BeautifulSoup(content_file, 'html.parser')
    ads_details = []
    data = {}
    try:
        p = soup.find("ul", class_='detail-more').find("p")
    except BaseException:
        print("NO DETAIL-MORE")
    try:
        for i in range(
            0, len(
                soup.find(
                "ul", class_='detail-more').find_all("p")), 2):
            ads_details.append((p.get_text(), p.find_next('p').get_text()))
            p = p.find_next('p')
            p = p.find_next('p')
    except:
        pass
    for i in range(0, len(ads_details)):
        if (ads_details[i][0].find('Loại hình') > -1 or ads_details[i][0].find('Loại hình nhà đất') > -1 ):
            data['LAND_TYPE'] = ads_details[i][1]
        if (ads_details[i][0].find('Diện tích sử dụng') > -1):
            data['USED_SURFACE_ORIGINAL'] = ads_details[i][1]
            continue
        if (ads_details[i][0].find('Diện tích') > -1):
            data['SURFACE_ORIGINAL'] = ads_details[i][1]
        if (ads_details[i][0].find('Chiều dài') > -1):
            data['PRO_LENGTH'] = (ads_details[i][1])[
                0:ads_details[i][1].find(' ')]
        if (ads_details[i][0].find('Chiều rộng') > -1):
            data['PRO_WIDTH'] = (ads_details[i][1])[
                0:ads_details[i][1].find(' ')]
        if (ads_details[i][0].find('Giá bán') > -1 or ads_details[i][0].find('Giá thuê') > -1 or ads_details[i][0].find('Giá đăng')  > -1 ):
            data['PRICE_ORIGINAL'] = ads_details[i][1]
        if (ads_details[i][0].find('Loại chủ quyền') > -1):
            data['LEGAL_STATUS'] = ads_details[i][1]
        if (ads_details[i][0].find('Số tầng') > -1):
            data['NB_FLOORS'] = ads_details[i][1]
        if (ads_details[i][0].find('Phòng ngủ') > -1 or ads_details[i][0].find('Số  Phòng ngủ') > -1 ):
            data['BEDROOM'] = ads_details[i][1]
        if (ads_details[i][0].find('Phòng tắm') > -1 or ads_details[i][0].find('Số phòng tắm') > -1):
            data['BATHROOM'] = ads_details[i][1]
        if (ads_details[i][0].find('Dự án') > -1):
            data['PROJECT_NAME'] = ads_details[i][1]
        if (ads_details[i][0].find('Thời gian bắt đầu') > -1 or ads_details[i][0].find('Ngày Đăng') > -1):
            data['ADS_DATE_ORIGINAL'] = ads_details[i][1]
            data['ADS_DATE'] = ads_details[i][1]
            if "-" in ads_details[i][1]:
                data['ADS_DATE'] = ads_details[i][1].split("-")[-1]
        if (ads_details[i][0].find('Hướng cửa') > -1):
            data['PRO_DIRECTION'] = ads_details[i][1]

    id_client = soup.select('.listing-id > span:nth-child(2)')
    if len(id_client) == 0 :
        id_client = soup.select('.detail-more > li:nth-child(1) > p:nth-child(2)')

    id_client = id_client[0].get_text()
    data['ID_CLIENT'] = id_client
    data['SITE'] = 'rever.vn'
    data['CREATED_DATE'] = update_date.strftime("%Y-%m-%d")
    data['DATE_ORIGINAL'] = today
    data['PRO_FLAG'] = 0 
    try:
        pro_direction = soup.select('.detailroom')[0].find('li', title='Hướng nhà')
        if (str(pro_direction) != 'None'):
            data['PRO_DIRECTION'] = pro_direction.get_text().replace(
                '\n', '').replace(
                ' ', '', 1)
    except BaseException:
        print("NO PRO_DIRECTION")
    try:
        pro_utility = ''
        for p in soup.select(
                '#details-amenities > ul')[0].find_all('p', class_="left"):
            pro_utility += p.get_text() + ','
        pro_utility = pro_utility[0:len(pro_utility) - 1]
        data['PRO_UTILITIES'] = pro_utility
    except BaseException:
        print("NO PRO_UTILITIES")
    try:
        #.mls--head__left > div:nth-child(2)
        street = ""
        #html body div#wrap section#sticky.msl-listing-detail-app.page-listing-detail.page__mls div.container div.page__mls--head div.mls--head__left 
        if len(soup.select('div.address > h2:nth-child(1) > a:nth-child(1)')) > 0:
            street = soup.select(
                'div.address > h2:nth-child(1) > a:nth-child(1)')[0].get_text().replace(',', '')
        else:
            street = soup.select('.mls--head__left > div:nth-child(2) > h4:nth-child(1) > a:nth-child(1)')[0].get_text().replace(',', '')
        data['STREET'] = street
    except BaseException:
        print("NO STREET")
    try:
        ward = ""
        if len(soup.select('div.address > h2:nth-child(2) > a:nth-child(1)')) > 0:
            ward = soup.select('div.address > h2:nth-child(2) > a:nth-child(1)')[0].get_text().replace(',', '')
        else:
            # .mls--head__left > div:nth-child(2) > h4:nth-child(2) > a:nth-child(1)
            ward = soup.select('.mls--head__left > div:nth-child(2) > h4:nth-child(2) > a:nth-child(1)')[0].get_text().replace(',', '')
        data['WARD'] = ward
    except BaseException:
        print("NO WARD")
    try:
        district = ""
        if len(soup.select("div.address > h2:nth-child(3) > a:nth-child(1)")) > 0:
            district = soup.select("div.address > h2:nth-child(3) > a:nth-child(1)")[0].get_text()
        else:
            district = soup.select(".mls--head__left > div:nth-child(2) > h4:nth-child(3) > a:nth-child(1)")[0].get_text()
        data['DISTRICT'] = district
    except BaseException:
        print("NO DISTRICT")
    # try:
    #     city = soup.select("form.hidden > input:nth-child(24)")[0]['value']
    #     data['CITY'] = city
    # except BaseException:
    #     print("NO CITY")
    try:
        city = soup.select(".mls--head__left > div:nth-child(2) > h4:nth-child(4) > a:nth-child(1)")[0].get_text()
        data['CITY'] = city
    except BaseException:
        print("NO CITY")
    try:
        full_address = soup.select(".left-70 > strong:nth-child(2)")[0].get_text()
        data['FULL_ADDRESS'] = full_address
    except BaseException:
        print("NO FULL ADDRESS")
    try:
        lon = ""
        if len(soup.select("form.hidden > input:nth-child(27)")) > 0:
            lon = soup.select("form.hidden > input:nth-child(27)")[0]['value']
        else:
            lon = soup.find('input', {'name':'lon'})['value']
        data['LON'] = lon
    except BaseException:
        print("NO LON")
    try:
        lat = ""
        if len(soup.select("form.hidden > input:nth-child(26)")) > 0:
            lat = soup.select("form.hidden > input:nth-child(26)")[0]['value']
        else:
            lat = soup.find('input', {'name':'lat'})['value']
        data['LAT'] = lat
    except BaseException:
        print("NO LAT")
    try:
        ads_link = soup.find(attrs={"rel": "canonical"})['href']
        data['ADS_LINK'] = ads_link
        data['FOR_SALE'] = 0
        data['FOR_LEASE'] = 0
        if (ads_link.find('mua') >= 0):
            data['FOR_SALE'] = 1
        else:
            data['FOR_LEASE'] = 1
    except BaseException:
        print("NO ADS_LINK")
    try:
        ads_title = ""
        if len(soup.select(".detail-house > h1:nth-child(2)")) > 0:
            ads_title = soup.select(
                ".detail-house > h1:nth-child(2)")[0].get_text()
        else:
            ads_title = soup.select("h1.heading-01")[0].get_text()
            
        data['ADS_TITLE'] = ads_title
    except BaseException:
        print("NO ADS_TITLE")
    try:
        detailed_brief = ""
        if len(soup.select(".summary")) > 0:
             detailed_brief = soup.select(".summary")[0].get_text()
        else:
             detailed_brief = soup.select(".listing__description")[0].get_text()
            
        data['DETAILED_BRIEF'] = detailed_brief
    except BaseException:
        print("NO DETAILED_BRIEF")
    try:
        photos = 0
        if len(soup.select('.gallery-property')) > 0:
             photos = len(soup.select('.gallery-property')[0].find_all('div')) - 1
        else:
             photos = len((soup.select('#listing__gallery--carousel')[0].find_all('li')))

        data['PHOTOS'] = photos
    except BaseException:
        print("NO PHOTOS")
    if (len(soup.select("div.list-advantage:nth-child(5) > div:nth-child(2)")) > 0):
        data['SCHOOL'] = 1
    if (pro_utility.find('Gym') >= 0):
        data['GYM'] = 1
    if (pro_utility.find('Chỗ đậu xe hơi') >= 0):
        data['PARKING'] = 1
        data['GARAGE'] = 1
    for (key, value) in data.items():
        if (str(type(value)).find('int') >= 0):
            continue
        data[key] = data[key].replace('\n', '')
        data[key] = data[key].replace('"', '')
        data[key] = data[key].replace("'", "")
        data[key] = data[key].replace(";", "")
        character = ''.join(chr(92))  # chr(92) character in ASCII TABLE is \
        data[key] = data[key].replace(character, '')
    return data


def store(ads):
    '''
    Returns SQL command line to insert datas into database

        Parameters:
                ads (dict): The dictionary of ads's fields

        Returns:
                result[0:len(result) - 1] + ' ;' (str): The string of SQL command line
                Example:
                INSERT IGNORE INTO REVERVN set LAND_TYPE="Đất nền",SURFACE="185.5",SURFACE_UNIT="m2",PRO_LENGTH="18",USED_SURFACE="185.5",
                USED_SURFACE_UNIT="m2",PRO_WIDTH="10",LEGAL_STATUS="Sổ đỏ",PRICE="10.2",PRICE_UNIT="tỷ",ID_CLIENT="PUN59385",SITE="rever.vn",CREATED_DATE="20200826",
                AGENCY_NAME="Rever",AGENCY_WEBSITE="Rever.vn",AGENCY_ADDRESS="ST01, LakeView 1, Đường Ven Hồ Trung Tâm, P. An Khánh, Quận 2, TP. Hồ Chí Minh",
                AGENCY_CITY="TP. Hồ Chí Minh",AGENCY_TEL="1800 234 546",
                PRO_UTILITIES="Ban công,Phòng cho giúp việc,Sân vườn,Phòng giải trí,Chỗ đậu xe hơi,Hồ bơi riêng,Quầy minibar,Tầng hầm,Góc làm việc,Nhà kho,Nuôi thú cưng,Gym",STREET="Số 7",WARD="Phước Kiển",DISTRICT="Nhà Bè",CITY="Hồ Chí Minh",LON="106.6954865",LAT="10.7210109",ADS_LINK="https://rever.vn/mua/ban-gap-lo-dat-biet-thu-duong-so-7-so-hong-day-du-dien-tich-dat-185-5m2",
                FOR_SALE="1",FOR_LEASE="0",ADS_TITLE="Bán gấp lô đất biệt thự đường số 7, sổ hồng đầy đủ, diện tích đất 185.5m2.",DETAILED_BRIEF="Bán gấp lô đất biệt thự đường số 7, xã Phước Kiển, huyện Nhà Bè, diện tích đất 185.5m2. Sổ hồng pháp lý đầy đủ, sang tên ngay trong ngày cho khách có thiện chí.Vị trí đất nền nằm tại huyện Nhà Bè, nằm trên đường số 7, giao với đường lộ Nguyễn Hữu Thọ, cách khu biệt thự Nine South và khu biệt thự Lavila khoảng 100m, , di chuyển vào trung tâm Quận 7 mất 15 phút xe máy. Khu vực xung quanh có nhiều tiện ích như: chợ, siêu thị My Market lavila, các hàng quán lớn nhỏ, xung quanh hiện hữu nhiều khu dân cư hiện đại.",
                PHOTOS="3",SCHOOL="1",GYM="1",PARKING="1",GARAGE="1" ;

    '''
    result = 'INSERT IGNORE INTO REVERVN set '
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
    result = 'UPDATE IGNORE REVERVN set '
    option = ""
    if 'ID_CLIENT' in ads:
        option = '  WHERE ID_CLIENT=' + '"' + str(ads['ID_CLIENT']) + '"'
    for (key, value) in ads.items():
        result += str(key) + '=' + '"' + str(value) + '",'
    return result[0:len(result) - 1] + option + ' ;'

start = time()
update_date = date.today()
folder, today, today_folder, spider_folder, all_folder, delta_folder, list_mode, sale_folder, lease_folder = revervn_helper.create_folder()

html_files = glob.glob(all_folder + '/*.html') # Total html files in ALL folder

print("Total html files:", len(html_files))
f =  open(delta_folder + '/VO_ANNONCE_insert.sql', 'w+')
fw = open(delta_folder + '/VO_ANNONCE_update.sql', 'w+')

for i in range(0, len(html_files)):
    if os.path.isfile(html_files[i]) == False:
        continue
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

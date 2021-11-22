import re
#used to scrap URLs
from lxml import etree
import yaml
import sys
import html
import unicodedata
from data_parser import * 
import time

# Input: HTML FILE AND YAML FILE
html_file = str(sys.argv[1])
config_file = str(sys.argv[2])
created_day = time.strftime("%Y-%m-%d")


# Run: python3 real_estate_data_parser.py annonce_ban-can-ho-chung-cu-bien-hoa-universe-complexmua-nha-chuan-5-saobien-hoa-univers-complex-tp-bien-hoa-co-hoi-trung-ngay-xe-hoi-mazda-luxury-pr13514974.html ./configs/dothinet.yml 
# Output: UPDATE IGNORE DOTHINET set ID_CLIENT="13514974",ADS_LINK="https://dothi.net/ban-can-ho-chung-cu-bien-hoa-universe-complex/mua-nha-chuan-5-saobien-hoa-univers-complex-tp-bien-hoa-co-hoi-trung-ngay-xe-hoi-mazda-luxury-pr13514974.htm",ADS_TITLE="Mua nhà chuẩn 5 SaoBiên Hòa Univers Complex TP Biên Hòa, cơ hội trúng ngay xe hơi Mazda Luxury. Liên hệ: 0906608683",
# PRICE_ORIGINAL="31 Triệu/m2",SURFACE_ORIGINAL="66 m2",DETAILED_BRIEF="Đăng ký nhận chương trình chiết khấu, ưu đãi lớn nhất dự án Biên Hòa Universe Complex - căn hộ phân khúc cao cấp đầu tiên tại trung tâm TP. Biên Hòa:",LAND_TYPE="Bán căn hộ chung cư",ADS_DATE_ORIGINAL="21/08/2021",PRO_DIRECTION="KXĐ",NB_ROOMS="2"
# ,ALLEY_ACCESS="",FRONTAGE="",NB_FLOORS="",BATHROOM="",DEALER_NAME="Lê Ngọc Tuấn",DEALER_TEL="0906608683",
# FULL_ADDRESS="Dự án Biên Hoà Universe Complex, Đường Xa Lộ Hà Nội, Phường Hố Nai, Biên Hòa, Đồng Nai",LAT="10.9661483",LON="106.8860308",PHOTOS="8"  WHERE ID_CLIENT="13514974" ;




with open(config_file) as yml_file:
    try:
        ads = {}
        config = yaml.safe_load(yml_file)
        fields = config['fields']
        site = config['SITE'] 
        table = config['TABLE_NAME'] 
        ads = extract(html_file, fields)
        row = ""
        ads['FOR_SALE'] = "0"
        ads['FOR_LEASE'] = "0"
        if len(ads['ID_CLIENT'])>0:
            if 'TOILET' in ads:
                ads['TOILET'] = ''.join(filter(str.isdigit, ads['TOILET']))
            if 'BEDROOM' in ads:
                ads['BEDROOM'] = ''.join(filter(str.isdigit, ads['BEDROOM']))
            if 'BATHROOM' in ads:
                ads['BATHROOM'] = ''.join(filter(str.isdigit, ads['BATHROOM']))
            
            if '/mua/' in ads['ADS_LINK']:
                ads['FOR_SALE'] = "1"
            elif '/thue/' in ads['ADS_LINK']:
                ads['FOR_LEASE'] = "1"
            
            option = "INSERT IGNORE INTO " + str(table) + ' set PRO_FLAG=0, CREATED_DATE=' + '"' + str(created_day) + '", '
            row = option + sql_query(ads) + ";"
            print(row)
    except:
        pass


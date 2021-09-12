import re
#used to scrap URLs
from lxml import etree
import yaml
import sys
import html
import unicodedata
from real_estate_data_parser import * 

html_file = str(sys.argv[1])
config_file = str(sys.argv[2])

with open(config_file) as yml_file:
    try:
        config = yaml.safe_load(yml_file)
        fields = config['fields']
        ads = extract(html_file, fields)
        option = "INSERT IGNORE INTO DOTHNET set "
        row = option + sql_query(ads) + ";"
        print(row)
    except Exception as e:
        # for just the message, or str(e), since print calls str under the hood
        print(e)

# Run: python3 dothinet_parser.py annonce_ban-can-ho-chung-cu-bien-hoa-universe-complexmua-nha-chuan-5-saobien-hoa-univers-complex-tp-bien-hoa-co-hoi-trung-ngay-xe-hoi-mazda-luxury-pr13514974.html ./configs/dothinet.yml 
# Output: UPDATE IGNORE DOTHINET set ID_CLIENT="13514974",ADS_LINK="https://dothi.net/ban-can-ho-chung-cu-bien-hoa-universe-complex/mua-nha-chuan-5-saobien-hoa-univers-complex-tp-bien-hoa-co-hoi-trung-ngay-xe-hoi-mazda-luxury-pr13514974.htm",ADS_TITLE="Mua nhà chuẩn 5 SaoBiên Hòa Univers Complex TP Biên Hòa, cơ hội trúng ngay xe hơi Mazda Luxury. Liên hệ: 0906608683",
# PRICE_ORIGINAL="31 Triệu/m2",SURFACE_ORIGINAL="66 m2",DETAILED_BRIEF="Đăng ký nhận chương trình chiết khấu, ưu đãi lớn nhất dự án Biên Hòa Universe Complex - căn hộ phân khúc cao cấp đầu tiên tại trung tâm TP. Biên Hòa:",LAND_TYPE="Bán căn hộ chung cư",ADS_DATE_ORIGINAL="21/08/2021",PRO_DIRECTION="KXĐ",NB_ROOMS="2"
# ,ALLEY_ACCESS="",FRONTAGE="",NB_FLOORS="",BATHROOM="",DEALER_NAME="Lê Ngọc Tuấn",DEALER_TEL="0906608683",
# FULL_ADDRESS="Dự án Biên Hoà Universe Complex, Đường Xa Lộ Hà Nội, Phường Hố Nai, Biên Hòa, Đồng Nai",LAT="10.9661483",LON="106.8860308",PHOTOS="8"  WHERE ID_CLIENT="13514974" ;
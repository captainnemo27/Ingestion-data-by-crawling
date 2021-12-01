import pandas as pd
import json
from unidecode import unidecode
import re
import os
import numpy as np
from time import time
import warnings
warnings.filterwarnings('ignore')
import urllib.parse
import urllib.request
import sys
import argparse
import datetime
from datetime import date, timedelta
from operator import itemgetter
from difflib import SequenceMatcher
from prettytable import PrettyTable
from geopy.geocoders import Nominatim
from collections import defaultdict
from collections import Counter
import html

global DIC_SYNONYM, DIC_SYNONYM_ORIGINAL
global DIC_CITY, DIC_DISTRICT, DIC_WARD
global LS_DELIMITER, LS_PREFIX, LS_PREFIX_ORIGINAL
global LS_LEVEL_CITY, LS_LEVEL_DISTRICT, LS_LEVEL_WARD
global LS_LEVEL_CITY_ORIGINAL, LS_LEVEL_DISTRICT_ORIGINAL, LS_LEVEL_WARD_ORIGINAL
global DIC_CITY_DISTRICT_WARD, DIC_CITY_DISTRICT_STREET

DIC_SYNONYM_ORIGINAL = {
    'thanh pho ho chi minh':["tp.hcm","tphcm"],
    'ho chi minh': ["HCMinh", "hcminh","Hồ Chí Minh."],
    'ha noi': ["hnội"],
    'ba ria vung tau': ["Bà Rịa - Vũng Tàu", "br-vt", "br - vt", "brvt"],
    'nha trang': ["nha trag"],
    'cam ranh': ["cm ranh"],
    'phan rang thap cham': ['phan rang - thap cham'],
    'pleiku': ['plei ku'],
    'kon tum': ["kontum"],
    'buon ma thuot': ['Buôn Mê Thuột','bmt'],
    "tam ky": ["tam ki"],
    "qui nhon": ["quy nhon"],
    "thanh pho" : [ "thanhpho"],
    "thi tran" : ["thitran"],
    '3/2': ["3 thang 2","3-2"],
    '2/9': ["2 thang 9","2/09","02/09"],
    '30/4': ["30 thang 4","30/04"],
    '19/5': ["19 thang 5","19/05"],
    '23/9': ["23 thang 9","23/09"],
    '23/10': ["23 thang 10"],
    '26/3': ["26 thang 3","26/03"],
    '27/3': ["27 thang 3","27/03"],
    '20/10': ["20 thang 10"],
    'cach mang thang tam': ["CMT8","cach mang thang 8"],
    'go vap': ["govap","gv"],
    'la gi': ["lagi"],
    'tinh lo': ['duong tinh lo'], 'quoc lo': ['duong quoc lo','q lo'],
    'phu qui': ["phu quy"],
}

DIC_SYNONYM =  {k.lower().strip(): [unidecode(i).lower().strip() for i in v] for k, v in DIC_SYNONYM_ORIGINAL.items()}

DIC_REPLACE= {'tl.':'tinh lo','tp.':'thanh pho','tl':'tinh lo','tp':'thanh pho','tt.':'thi tran','tx.':'thi xa',\
                'ql.':'quoc lo','ql':'quoc lo','q.':'quan','h.':'huyen','d.':'duong','x.':'xa','p.':'phuong',\
                    'tx':'thi xa','tt':'thi tran','h':'huyen','p':'phuong',\
                    'hn':'ha noi','hcm':'ho chi minh'}

DIC_PREFIX = {'thanh pho': 'Thành phố', 'tinh': 'Tỉnh', 
                'quan': 'Quận', 'huyen': 'Huyện', 'thi xa': 'Thị xã', 'thi tran': 'Thị trấn',
                'phuong': 'Phường', 'xa':'Xã',
                'duong':'Đường','tinh lo':'Tỉnh lộ','quoc lo':'Quốc lộ'}

LS_PREFIX_ORIGINAL = ['thành phố','thị xã','tỉnh lộ','quốc lộ','thị trấn','quận','xã','tỉnh','huyện','phường','đường']
LS_PREFIX = [unidecode(x.lower()) for x in LS_PREFIX_ORIGINAL]

LS_DELIMITER = [',','|',';','_','-','.']

LS_LEVEL_CITY_ORIGINAL = ['Thành phố', 'Tỉnh']
LS_LEVEL_DISTRICT_ORIGINAL = ["Quận", "Huyện", 'Thành Phố', "Thành phố", "Thị Xã", "Thị xã","huyện","quận","thành phố","thị xã"]
LS_LEVEL_WARD_ORIGINAL = ['Phường', 'Xã','Thị Trấn', 'Thị trấn']
LS_LEVEL_STREET_ORIGINAL = ['Tỉnh lộ','Tỉnh Lộ' ,'Quốc lộ','Quốc Lộ','']

LS_LEVEL_CITY = list(set([unidecode(x.lower()) for x in LS_LEVEL_CITY_ORIGINAL]))
LS_LEVEL_DISTRICT = list(set([unidecode(x.lower()) for x in LS_LEVEL_DISTRICT_ORIGINAL]))
LS_LEVEL_WARD = list(set([unidecode(x.lower()) for x in LS_LEVEL_WARD_ORIGINAL]))
LS_LEVEL_STREET = list(set([unidecode(x.lower()) for x in LS_LEVEL_STREET_ORIGINAL if x != '']))

LS_NOISE = ["dân cư", "chung cư", "dự án","văn phòng", "phường", "quận","xã","thành phố","việt nam","kdc","công viên",\
            "apartment","saigon","golden","mặt biển","mặt tiền","city","the","q.","tphcm","khu","kp","thị trấn","hẻm",\
            "garden","citi","essco","plaza","cao ốc","boulevard","oto","đất","tdp","bay","xe hơi","kcn","lb","wb2","đhyd","lh",\
            "mét","nhựa","ô tô","thôn","bờ sông",".","`","~","+","tại","trạm","vòng xoay","gần","bệnh viện","bê tông","land","thuộc"]
LS_NOISE_HOUSE_NUM = ['cho thuê','bán','tỉnh lộ','hương lộ','cách','ty','%','gọi','xem nhà','không thể','mặt']
DIC_FORMAT_STREET = {"Đường An Đường Vương": "Đường An Dương Vương",
                    "Đường Kinh Đường Vương": "Đường Kinh Dương Vương",
                    "Đường Nguyễn Duy Đường": "Đường Nguyễn Duy Dương",
                    "Đường Chương Đường": "Đường Chương Dương", "Đường Hướng Đường": "Đường Hướng Dương",
                    "Đường Đại Lộ Bình Đường": "Đường Đại Lộ Bình Dương",
                    "Đường Số": "", "Đường": "", "Phố": "","Đường / Phố": "", "Đường Huế": "",
                    "Đường Ba Tháng Hai": "Đường 3/2",
                    "Đường Hai Tháng Tư": "Đường 2/4",
                    "Đường Hai Tháng Chín": "Đường 2/9",
                    "Đường Mười Chín Tháng Năm": "Đường 19/5",
                    "Đường Tám Tháng Ba": "Đường 8/3",
                    "Đường 1 Tháng 12": "Đường 1/12",
                    "Đường 14 Tháng 9": "Đường 14/9",
                    "Đường 23 Tháng 8": "Đường 23/8",
                    "Đường 22 Tháng 12": "Đường 22/12",
                    "Đường 2 Tháng 4": "Đường 2/4",
                    "Đường 2 Tháng 9": "Đường 2/9",
                    "Đường 27 Tháng 4": "Đường 27/4",
                    "Đường 30 Tháng 4": "Đường 30/4",
                    "Đường 8 Tháng 3": "Đường 8/3",
                    "Đường 22 Tháng 12": "Đường 22/12",
                }
LS_PREFIX_STREET_ORIGINAL = ["đường","phố","quốc lộ","tỉnh lộ","hương lộ"]
LS_PREFIX_STREET = [unidecode(x) for x in LS_PREFIX_STREET_ORIGINAL]
DIC_SYNONYM_STREET = {'3/2': ["3 thang 2","3-2","3/2"],
    'duong 2/9': ["2 thang 9","2 tháng 9","2/09","02/09","2/9"],
    'duong 30/4': ["30 thang 4","30/04","30/4"],
    'duong 19/5': ["19 thang 5","19/05","19/5"],
    'duong 23/9': ["23 thang 9","23/09","23/9"],
    'duong 23/10': ["23 thang 10","23/10"],
    'duong 26/3': ["26 thang 3","26/03","26/3"],
    'duong 27/3': ["27 thang 3","27/03","27/3"],
    'duong 20/10': ["20 thang 10","20/10"],
    'duong cach mang thang tam': ["CMT8","cach mang thang 8","cmt8"],} 

# create dictionary dic_city_ward.json
# generated from VN_tinh_huyen.csv
# with key1 = 'thanhpho', key2 = 'Hà Nội', key3 = 'quan', key4 = 'ba dinh', key5 = 'phuong' and value = list ward
# Example: data["thanhpho"]["Hà Nội"]["quan"]["Ba Đình"]["phuong"] 
# -> ['phuc xa', 'truc bach', 'vinh phuc', 'cong vi', 'lieu giai', 'nguyen trung truc', 'quan thanh', 'ngoc ha', 'dien bien', 'doi can', 'ngoc khanh', 'kim ma', 'giang vo', 'thanh cong'] 
with open("json/DIC_CITY_DISTRICT_WARD.json", "r", encoding="utf8") as f:
    DIC_CITY_DISTRICT_WARD = json.load(f)
with open("json/DIC_CITY_DISTRICT_STREET.json", "r", encoding="utf8") as f:
    DIC_CITY_DISTRICT_STREET = json.load(f)

# create dic city_ward, dic city_street
# key1 = 'thanhpho', key2 = 'Hồ Chí Minh', key3 = 'phuong', value = list ward
# Example: data['thanhpho']['Hồ Chí Minh']['phuong']
with open("json/DIC_CITY_WARD.json", "r", encoding="utf8") as f:
    DIC_CITY_WARD = json.load(f)
with open("json/DIC_CITY_STREET.json", "r", encoding="utf8") as f:
    DIC_CITY_STREET = json.load(f)

# create dic_combine_level
# key1 = 'thanh pho ho chi minh', key2 = 'quan go vap'
# Example: data['thanh pho ho chi minh']['quan go vap']
with open("json/DIC_COMBINE_LEVEL.json", "r", encoding="utf8") as f:
    DIC_COMBINE_LEVEL = json.load(f)

# create DIC_CITY, DIC_DISTRICT, DIC_WARD, DIC_STREET
# DIC_CITY, DIC_DISTRICT, DIC_WARD: generated from VN_tinh_huyen.csv
# DIC_STREET: generated from API 
# with key = prefix and value = list giá trị tương ứng tên dic
# Example: {thanhpho: ['Hồ Chí Minh','Hà Nội'], tinh: ['Ninh Bình','Cà Mau']}
with open("json/DIC_CITY.json", "r", encoding="utf8") as f:
    DIC_CITY = json.load(f)
with open("json/DIC_DISTRICT.json", "r", encoding="utf8") as f:
    DIC_DISTRICT = json.load(f)
with open("json/DIC_WARD.json", "r", encoding="utf8") as f:
    DIC_WARD = json.load(f)
with open("json/DIC_STREET.json", "r", encoding="utf8") as f:
    DIC_STREET = json.load(f)

LOG_FOLDER="/home/itdev/backup_autobiz_data/LOGS"

API_URL = "https://nominatim.openstreetmap.org/search"
API_URL_LOCAL = "http://172.16.0.236:7070/search"

LEGAL_STATUS_DIC_SHORT = {
    'so hong chung': "shc",
    'so do chung': "shc",
    'so hong cc': "shc",
    'so do cc': "shc",
    'so hong': "sh",
    'so do': "sh",
    'bia do':'sh',
    'so vuong':'sh',
    'hop dong': 'hd',
    'giay to':'gt',
    'giay tay':'gt',
    'giay phep':'gt',
    '1/500': 'gpxd_1500',
    '1/200': 'gpxd_1200',
    'youtube':'da',
    'da co so': 'sh',
    'phap ly day du':'da',
    'phap ly 50 nam':'hd50',
    'cho tach thua':'gt',
    'dang ban giao':'da',
    'du an':'da',
    'giay chu quyen':'gt',
    'phap ly hoan thien':'da',
    'phap ly co ban':'da',
    'uy quyen':'da',
    'shr':'sh',
    'hdmb':'hd',
    'gpxd':'gt',
    'cc': "gt",
    'gcn':'gt',
    'so san':'sh',
    'so chung':'shc',
}

PRO_DIRECTION_DIC_SHORT = {
    'dong bac': 'db',
    'dong nam': 'dn',
    'tay bac': 'tb',
    'tay nam': 'tn',
    'dong': 'd',
    'tay': 't',
    'nam': 'n',
    'bac':'b',
}

LAND_TYPE_DIC_SHORT = {
    'nha mat tien': 'nmt',
    'nha rieng': 'nr',
    'trang trai':'ttnd',
    'homestay':'ttnd',
    'biet thu': 'bt',
    'villa': 'bt',
    'mat bang':'vp',
    'van phong': 'vp',
    'nha tro': 'npt',
    'phong tro': 'npt',
    'dat nen': 'dn',
    'dat cong nghiep': 'dcn',
    'dat nong nghiep':'dnn',
    'can ho cao cap':'chcc',
    'can ho dich vu':'chdv',
    'can ho chung cu':'cc',
    'nha xuong':'kx',
}

ADS_LINK_DIC = {
    "nha": "nr",
    "chung cu": "cc",
    "shophouse": "sh",
    "dat": "d",
    "can": "cc",
    "can ho": "cc",
    "phong tro": "npt",
    "mat tien": "nmt",
    "lo dat": "d",
    "phong tro nha xuong": "kx",
    "biet thu": "bt",
    "vp": "vp",
    "van phong": "vp"
}

LS_SITE = ["dothinet","batdongsancomvn","diaoconline","homedy","mogivn",\
    "nhachotot","nhadatcafeland","propzyvn","revervn",\
        "sosanhnha","tinbatdongsan","batdongsan","youhomes","alonhadat","rongbay"]


LS_ROOT = ["ADS_DATE",'LAND_TYPE','LEGAL_STATUS','PRO_DIRECTION',\
           'CITY','DISTRICT','WARD','STREET',"FULL_ADDRESS","LAT","LON",\
           'USED_SURFACE','SURFACE','SURFACE_UNIT','PRICE','PRICE_UNIT',\
           'PRO_LENGTH','PRO_WIDTH','ALLEY_ACCESS', 'FRONTAGE','NB_ROOMS','NB_FLOORS', 'BEDROOM','BATHROOM',\
           'DEALER_TEL','DEALER_EMAIL','DEALER_JOINED_DATE',\
            'ADS_DATE_ORIGINAL','DATE_ORIGINAL','PRICE_ORIGINAL','SURFACE_ORIGINAL'
          ]

LS_CLEAN = ["ADS_DATE",'LAND_TYPE','LEGAL_STATUS','PRO_DIRECTION',\
            'SPLIT_CITY','SPLIT_DISTRICT','SPLIT_WARD','FORMAT_STREET',"FORMAT_HS","FULL_ADDRESS","LAT","LON",\
            'SURFACE','PRICE','PRICE_M2','SURFACE_TEXT','PRICE_TEXT','DATE_ORIGINAL',\
            'PRO_LENGTH','PRO_WIDTH','ALLEY_ACCESS', 'FRONTAGE',\
            'PRO_LENGTH_TEXT','PRO_WIDTH_TEXT','ALLEY_TEXT', 'FRONTAGE_TEXT',\
            'NB_ROOMS','NB_FLOORS', 'BEDROOM', 'DEALER_TEL']

LS_DUPLICATE = ['SPLIT_CITY', 'SPLIT_DISTRICT', 'SPLIT_WARD', 'FORMAT_STREET', 'FORMAT_HS', 'SURFACE', 'PRICE', 'PRO_WIDTH', 'PRO_LENGTH']

LS_167 = ["alonhadat","batdongsan","batdongsancomvn","diaoconline","dothinet",\
        "homedy","mogivn","propzyvn","revervn","tinbatdongsan","youhomes"]

LS_227 = ["nhachotot","nhadatcafeland","sosanhnha","rongbay"]

LS_PR_UNIT = ["ty","ti","trieu","ngan","nghin","usd","tram","dong","tr","d","cayvang"] # updating

LS_SF_UNIT = ["m2","hecta","hec","ha"] # updating

HEM_XEBAGAC=3
HEM_XETAI=5
HEM_XEHOI=4.5
HEM_XEMAY=1

DOLLAR_PRICE = 23200
GOLD_PRICE = 55000000

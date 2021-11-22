#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import sys
import HTMLParser
import re
import io
import unicodedata

# Set the default encoding as utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

# Define variable
file_json = str(sys.argv[1])
prefix_city = str(sys.argv[2])

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

def check_exist_element (words):
	if words in str(io.open(file_json,'r', encoding='utf-8').read()).decode('unicode-escape'):
		return True;
	return False;	

def no_accent_vietnamese(s):
    s = s.decode('utf-8')
    s = re.sub(u'Đ', 'D', s)
    s = re.sub(u'đ', 'd', s)
    return unicodedata.normalize('NFKD', unicode(s)).encode('ASCII', 'ignore')

with open(file_json) as data_file:   
	data = json.load(data_file, encoding='utf-8')

i=0

# Loop parse data

index=0
while (index < len(data)):
    city_name = data[index]["Text"]
    city_name = no_accent_vietnamese(city_name).lower()
    city_name = re.sub(' ','-', city_name)
    city_name = re.sub('\'','-', city_name)
    city_name = re.sub('\.','', city_name)
     
    if ( prefix_city == "VT" and city_name == "phu-my"):
        city_name = "phu-my_1"
    if ( prefix_city == "DNA" and city_name == "tan-phu"):
            city_name = "tan-phu-dna"
    if ( prefix_city == "CT" and city_name == "-thoi-lai"):
            city_name = "thoi-lai"
    if ( prefix_city == "KT" and city_name == "ia-h-drai"):
            city_name = "ia-hdrai"
    if ( prefix_city == "NA" and city_name == "hoang-mai"):
            city_name = "hoang-mai-1"
    if ( prefix_city == "NT" and city_name == "phan-rang---thap-cham"):
            city_name = "phan-rang-thap-cham"
    if ( prefix_city == "GL" and city_name == "ia-grai"):
            city_name = "ia-grai_1"
    
    query_insert = str(city_name)+'-'+str(prefix_city)
    
    index = index + 1
    print query_insert.lower()
    
    
    

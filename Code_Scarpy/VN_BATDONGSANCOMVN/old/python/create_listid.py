#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import time
import batdongsancomvn_helper
import glob
import codecs
from bs4 import BeautifulSoup
from lxml import etree
from io import StringIO, BytesIO


def create_listid():
    '''
    Creates the list of ads's id_client are not duplicated which saved in list_id.txt in DELTA folder.
    And created the list of ads's id client are duplicated which saved in backup.txt in DELTA folder.

        Parameters:
                None

        Returns:
                None
    '''
    file_name = []
    file_name.append(glob.glob(sale_folder + '/*.html'))
    file_name.append(glob.glob(lease_folder + '/*.html'))
    file_name.append(glob.glob(to_buy_to_lease_folder + '/*.html'))
    for folder in range(0, len(file_name)):
        for position_html_file_in_folder in range(
                0, len(file_name[folder])):
            content_file = codecs.open(
                file_name[folder][position_html_file_in_folder], 'r')
            
            parser = etree.HTMLParser()
            tree = etree.parse(StringIO(str(content_file.read())), parser)
            try:
                elms = tree.xpath("//div[contains(concat(' ',normalize-space(@class),' '),' product-item ')]/a")
                for elm in elms:
                    link = 'https://batdongsan.com.vn' + elm.attrib['href']
                    if "-ad" in link:
                        id_client = link.split("-ad")[-1]
                    if "-pr" in link:
                        id_client = link.split("-pr")[-1]
                    all_list.append((id_client, link))
                    dictionary_id[id_client] = link
                
            except BaseException:
                print("NO ADS!!!!!")
                        

    with open(delta_folder + '/list_id.txt', 'w') as f:
        for (key, value) in dictionary_id.items():
            f.write(str(key) + ' ' + str(value) + '\n')
    f.close()
    with open(delta_folder + '/backup.txt', 'w') as f:
        for i in range(0, len(all_list)):
            f.write(str(all_list[i][0]) + ' ' + str(all_list[i][1]) + '\n')
    f.close()
    return None


start = time()
folder, today, today_folder, all_folder, delta_folder, list_mode, sale_folder, lease_folder, to_buy_to_lease_folder = batdongsancomvn_helper.create_folder()
all_list = []
dictionary_id = {}
create_listid()
delta = time()
print('DONE CREATE LIST ID')
print('================%s SECONDS===================' % (delta - start))
#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import time
import revervn_helper
import os
import os.path
import codecs
from bs4 import BeautifulSoup


def create_listid():
    '''
    Creates the list of ads's id_client are not duplicated which saved in list_id.txt in DELTA folder.
    And created the list of ads's id client are duplicated which saved in backup.txt in DELTA folder.

        Parameters:
                None

        Returns:
                None
    '''

    category = []
    category.append('/page-mua-ban-bat-dong-san-')
    category.append('/page-thue-bat-dong-san-')
    file_count = []
    file_count.append(len(os.listdir(sale_folder)))
    file_count.append(len(os.listdir(lease_folder)))
    for i in range(0, len(file_count)):
        if (i == 0):
            folder = sale_folder
        else:
            folder = lease_folder
        for j in range(0, file_count[i]):
            # for j in range(0,1):
            print(category[i] + str(j + 1))
            file_name = folder + category[i] + str(j + 1) + '.html'
            if os.path.isfile(file_name) == False:
                continue
            content_file = codecs.open(file_name, 'r')
            soup = BeautifulSoup(content_file, 'html.parser')
            
            for ads_index in soup.findAll('div',{'class':'col property-itemz'}):
                try:
                    ##property-rever-1592819277634_6957 > article > div.info-container > div.listing-address > h4:nth-child(1)                                        
                    id_client = ads_index.select_one("h4:nth-child(1)").text.split(" ")[0]
                    #property-rever-1592819277634_6957 > article > div.info-container > h3 > a
                    link_ads = ads_index.select_one("h3 > a")['href']    
                    dictionary_id[id_client] = link_ads
                    all_list.append((id_client, link_ads))
                except BaseException:
                    print("Full Ads !!! Do not crawl :))))))")

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
folder, today, today_folder, spider_folder, all_folder, delta_folder, list_mode, sale_folder, lease_folder = revervn_helper.create_folder()
all_list = []
dictionary_id = {}
create_listid()
delta = time()
print('DONE CREATE LIST ID')
print('================%s SECONDS===================' % (delta - start))

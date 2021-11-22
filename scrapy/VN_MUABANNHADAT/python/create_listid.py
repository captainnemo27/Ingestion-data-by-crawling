#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import time
import muabannhadat_helper
import glob
import json


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
    file_name.append(glob.glob(sale_folder + '/*.json'))
    file_name.append(glob.glob(lease_folder + '/*.json'))
    for folder in range(0, len(file_name)):
        for position_json_file_in_folder in range(
                0, len(file_name[folder])):
            with open(file_name[folder][position_json_file_in_folder], 'r') as json_file:
                content_file = json.load(json_file)
            for ads_index in range(len(content_file['data'])):
                id_client = content_file['data'][ads_index]['id'] 
                link_ads = 'https://www.muabannhadat.vn' + content_file['data'][ads_index]['path']
                all_list.append((id_client, link_ads))
                dictionary_id[id_client] = link_ads

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
folder, today, today_folder, spider_folder, all_folder, delta_folder, list_mode, sale_folder, lease_folder = muabannhadat_helper.create_folder()
all_list = []
dictionary_id = {}
create_listid()
delta = time()
print('DONE CREATE LIST ID')
print('================%s SECONDS===================' % (delta - start))

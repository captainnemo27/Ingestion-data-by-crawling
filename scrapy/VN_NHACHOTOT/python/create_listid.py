#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from time import time
import chotot_helper
import os
import os.path


def create_listid():
    '''
    Creates the list of ads's id_client are not duplicated which saved in list_id.txt in DELTA folder.
    And created the list of ads's id client are duplicated which saved in backup.txt in DELTA folder.

        Parameters:
                None

        Returns:
                None
    '''
    files = os.listdir(list_mode)

    file_count = len(files)
    for i in range(0, file_count):
        print(i + 1)
        file_name = list_mode + \
            '/page-mua-ban-bat-dong-san-' + str(i + 1) + '.json'
        if os.path.isfile(file_name) == False:
            continue
        with open(file_name, 'r') as read_file:
            try:
                read_data = json.load(read_file)
            except BaseException:
                print('Cannot open', i)
        for j in range(0, len(read_data['ads'])):
            dictionary_id[read_data['ads'][j]['list_id']
                          ] = 'https://gateway.chotot.com/v1/public/ad-listing/' + str(read_data['ads'][j]['list_id'])
            all_list.append(
                (read_data['ads'][j]['list_id'],
                 'https://gateway.chotot.com/v1/public/ad-listing/' + str(
                    read_data['ads'][j]['list_id'])))
        read_file.close()

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
folder, today, today_folder, spider_folder, all_folder, delta_folder, list_mode = chotot_helper.create_folder()
all_list = []
dictionary_id = {}
create_listid()
delta = time()
print('DONE CREATE LIST ID')
print('------%s SECONDS-------' % (delta - start))

#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import time
import youhomes_helper
import os
import os.path
import codecs
from lxml import etree
from lxml import html

from io import StringIO, BytesIO
import glob


def rename_file(path_to_html_file, old_file_name, new_file_name):
    '''
    Rename file in folder

            Parameters:
                    path_to_html_file (str): Path to html file which contains old file name
                    old_file_name (str): Name file's present
                    new_file_name (str): The file's new name

            Returns:
                    None
    '''
    os.rename(
        path_to_html_file +
        '/' +
        old_file_name,
        path_to_html_file +
        '/' +
        new_file_name)
    return None


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
    file_name.append(glob.glob(house_sale_folder + '/*.html'))
    file_name.append(glob.glob(apartment_sale_folder + '/*.html'))
    file_name.append(glob.glob(house_lease_folder + '/*.html'))
    file_name.append(glob.glob(apartment_lease_folder + '/*.html'))
    for folder in range(0, len(file_name)):
        for position_html_file_in_folder in range(
                0, len(file_name[folder])):
            content_file = codecs.open(
                file_name[folder][position_html_file_in_folder], 'r')
            parser = etree.HTMLParser()
            tree = etree.parse(StringIO(str(content_file.read())), parser)
            try:
                # xpath full: /html/body/div[2]/div[3]/div[2]/div/div[1]/div[3]/div[1]/div/div/div[2]/h4/a
                # xpath: //*[@id="contents"]/div[2]/div/div[1]/div[3]/div[4]/div/div/div[2]/h4/a
                # class="col-xs-8 col-sm-8 col-md-8 col-lg-8 product-caption product-rent"
                elms = tree.xpath("//div[contains(concat(' ',normalize-space(@class),' '),' product-caption ')]/h4/a")
                for elm in elms:
                    link = elm.attrib['href']
                    all_list.append(link)
                    dictionary_url[link] = 1
            except BaseException:
                print("NO ADS!!!!!")
    
    with open(delta_folder + '/list_id.txt', 'w') as f:
        for (key, value) in dictionary_url.items():
            f.write(str(key) + '\n')
    f.close()
    with open(delta_folder + '/backup.txt', 'w') as f:
        for i in range(0, len(all_list)):
            f.write(str(all_list[i]) + '\n')
    f.close()
    return None


start = time()
folder, today, today_folder, spider_folder, all_folder, delta_folder, list_mode, sale_folder, lease_folder, house_sale_folder, apartment_sale_folder, house_lease_folder, apartment_lease_folder = youhomes_helper.create_folder()
all_list = []
dictionary_url = {}
dictionary_id = {}
create_listid()
delta = time()
print('DONE CREATE LIST ID')
print('================%s SECONDS===================' % (delta - start))

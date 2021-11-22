import sys
from time import time
import scrapy
import os
import os.path
from lxml import etree
from io import StringIO, BytesIO
from bs4 import BeautifulSoup
import glob
import codecs
os.chdir("..")
os.chdir("..")
sys.path.insert(1, os.getcwd() + '/python/')
import batdongsancomvn_helper
folder, today, today_folder, all_folder, delta_folder, list_mode, sale_folder, lease_folder, to_buy_to_lease_folder = batdongsancomvn_helper.create_folder()
max_page_file = open(today_folder + "/max_page_number.txt", "r")
max_page_number = max_page_file.readlines()
for i in range(0, len(max_page_number)):
    max_page_number[i] = max_page_number[i].replace('\n', '')

if os.path.isfile(delta_folder + '/list_id.txt'):
    dictionary_id = {}
    file = open(delta_folder + '/list_new_id.txt', 'r')
    for line in file.readlines():
        data = line.split(' ')
        if len(data)>1 :
            data[1] = data[1].replace('\n', '')
            dictionary_id[data[0]] = data[1]
        else:
            dictionary_id[data[0]] = 0
    file.close()

    if '-1' in dictionary_id.keys():
        dictionary_id.pop('-1')
        file = open(delta_folder + '/list_id.txt', 'r')
        for line in file.readlines():
            data = line.split(' ')
            data[1] = data[1].replace('\n', '')
            dictionary_id[data[0]] = data[1]
        file.close()


class SpiderForDownloadSite(scrapy.Spider):
    """
    Reference link: https://docs.scrapy.org/en/latest/topics/spiders.html
    """

    name = "download_site"

    def requests_site_for_sale(self):
        global max_page_number
        urls = []
        print("MAX PAGE NUMBER FOR SALE: ", max_page_number[0])
        for page_number in range(0, int(max_page_number[0])):
            urls.append(
                "https://batdongsan.com.vn/nha-dat-ban/p" + str(page_number + 1))
        return urls

    def requests_site_for_lease(self):
        global max_page_number
        urls = []
        print("MAX PAGE NUMBER FOR LEASE: ", max_page_number[1])
        for page_number in range(0, int(max_page_number[1])):
            urls.append(
                "https://batdongsan.com.vn/nha-dat-cho-thue/p" + str(page_number + 1))
        return urls

    def requests_site_to_buy_to_lease(self):
        global max_page_number
        urls = []
        print("MAX PAGE NUMBER TO BUY TO LEASE: ", max_page_number[2])
        for page_number in range(0, int(max_page_number[2])):
            urls.append(
                "https://batdongsan.com.vn/can-mua-can-thue/p" + str(page_number + 1))
        return urls

    def start_requests(self):
        print("==================Start download site==================")
        start = time()
        urls_site = self.requests_site_for_sale()
        for url in urls_site:
            filename = 'page-mua-ban-bat-dong-san-'+ str(urls_site.index(url) + 1) + '.html'
            if os.path.isfile(sale_folder + '/' + filename) == True:
                print(filename,' is exist. Dont download')
                continue
            print("Page number for sale: ", urls_site.index(url) + 1)
            yield scrapy.Request(url=url, callback=self.download_list_mode_for_sale)

        urls_site = self.requests_site_for_lease()
        for url in urls_site:
            filename = 'page-thue-bat-dong-san-'+ str(urls_site.index(url) + 1) + '.html'
            if os.path.isfile(lease_folder + '/' + filename) == True:
                print(filename,' is exist. Dont download')
                continue
            print("Page number for lease: ", urls_site.index(url) + 1)
            yield scrapy.Request(url=url, callback=self.download_list_mode_for_lease)

        urls_site = self.requests_site_to_buy_to_lease()
        for url in urls_site:
            filename = 'page-can-mua-can-thue-bat-dong-san-'+ str(urls_site.index(url) + 1) + '.html'
            if os.path.isfile(to_buy_to_lease_folder + '/' + filename) == True:
                print(filename,' is exist. Dont download')
                continue
            print("Page number to buy to lease: ", urls_site.index(url) + 1)
            yield scrapy.Request(url=url, callback=self.download_list_mode_to_buy_to_lease)

        delta = time()
        print(
            '==================%s SECONDS===========================' %
            (delta - start))

    def download_list_mode_for_sale(self, response):
        page = response.url.split("/p")[-1]
        filename = 'page-mua-ban-bat-dong-san-%s.html' % page
        with open(sale_folder + '/' + filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def download_list_mode_for_lease(self, response):
        page = response.url.split("/p")[-1]
        filename = 'page-thue-bat-dong-san-%s.html' % page
        with open(lease_folder + '/' + filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def download_list_mode_to_buy_to_lease(self, response):
        page = response.url.split("/p")[-1]
        filename = 'page-can-mua-can-thue-bat-dong-san-%s.html' % page
        with open(to_buy_to_lease_folder + '/' + filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


class SpiderForDownloadAds(scrapy.Spider):
    """
    Reference link: https://docs.scrapy.org/en/latest/topics/spiders.html
    """

    name = 'download_ads'

    def requests_ads(self):
        # return list(dictionary_id.values())
        return list(dictionary_id.items()) # Include id_client and url of id_client

    def start_requests(self):
        start = time()
        print("==================Start download ads===================")
        # urls_ads = self.requests_ads()
        list_item = self.requests_ads() # Include id_client and url of id_client
        for item in list_item:
            filename = str(item[0]) + '.html'
            if os.path.isfile(all_folder + '/' + filename) == True:
                print("Ads: " + str(list_item.index(item) + 1) + ". " + str(item[0])  + ".html is exist. Don't download")
                continue
            print("Ads: ", list_item.index(item) + 1)
            yield scrapy.Request(url=item[1], callback=self.download_detail_mode)
        delta = time()
        print(
            '==================%s SECONDS===========================' %
            (delta - start))

    def download_detail_mode(self, response):
        id_client = response.url.split("-pr")[-1]
        if id_client.isnumeric()==False:
            id_client = response.url.split("-ad")[-1]
        filename = '%s.html' % str(id_client).replace('.html','')
        with open(all_folder + '/' + filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

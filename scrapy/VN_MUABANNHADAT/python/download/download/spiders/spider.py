import sys
from time import time
import scrapy
import os
import os.path
import glob
os.chdir("..")
os.chdir("..")
sys.path.insert(1, os.getcwd() + '/python/')
import muabannhadat_helper
folder, today, today_folder, spider_folder, all_folder, delta_folder, list_mode, sale_folder, lease_folder = muabannhadat_helper.create_folder()
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
                "https://api.muabannhadat.vn/v1/listings?page=" + str(page_number + 1) + "&offer_type=sell")
        return urls

    def requests_site_for_lease(self):
        global max_page_number
        urls = []
        print("MAX PAGE NUMBER FOR LEASE: ", int(max_page_number[1]))
        urls.append("https://www.muabannhadat.vn/cho-thue-bat-dong-san")
        for page_number in range(0, int(max_page_number[1])):
            urls.append(
                "https://api.muabannhadat.vn/v1/listings?page=" + str(page_number + 1) + "&offer_type=rent")
        return urls

    def start_requests(self):
        print("==================Start download site==================")
        start = time()
        urls_site = self.requests_site_for_sale()
        for url in urls_site:
            print("Page number for sale: ", urls_site.index(url) + 1)
            yield scrapy.Request(url=url, callback=self.download_list_mode_for_sale)

        urls_site = self.requests_site_for_lease()
        for url in urls_site:
            print("Page number for lease: ", urls_site.index(url) + 1)
            yield scrapy.Request(url=url, callback=self.download_list_mode_for_lease)

        delta = time()
        print(
            '==================%s SECONDS===========================' %
            (delta - start))

    def download_list_mode_for_sale(self, response):
        page = response.url.replace("&offer_type=sell", "").split("=")[-1]
        filename = 'page-mua-ban-bat-dong-san-%s.json' % page
        with open(sale_folder + '/' + filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def download_list_mode_for_lease(self, response):
        page = response.url.replace("&offer_type=rent", "").split("=")[-1]
        filename = 'page-thue-bat-dong-san-%s.json' % page
        with open(lease_folder + '/' + filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


class SpiderForDownloadAds(scrapy.Spider):
    """
    Reference link: https://docs.scrapy.org/en/latest/topics/spiders.html
    """

    name = 'download_ads'

    def requests_ads(self):
        return list(dictionary_id.values())


    def start_requests(self):
        start = time()
        print("==================Start download ads===================")
        urls_ads = self.requests_ads()
        for url in urls_ads:
            print("Ads: ", urls_ads.index(url) + 1)
            yield scrapy.Request(url=url, callback=self.download_detail_mode)
        delta = time()
        print(
            '==================%s SECONDS===========================' %
            (delta - start))

    def download_detail_mode(self, response):
        page = response.url.split("-")[-1]
        filename = '%s.html' % str(page)
        with open(all_folder + '/' + filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

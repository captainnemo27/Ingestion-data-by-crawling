import sys
from time import time
import scrapy
import os
import os.path
import glob
os.chdir("..")
os.chdir("..")
sys.path.insert(1, os.getcwd() + '/python/')
import youhomes_helper
folder, today, today_folder, spider_folder, all_folder, delta_folder, list_mode, sale_folder, lease_folder, house_sale_folder, apartment_sale_folder, house_lease_folder, apartment_lease_folder = youhomes_helper.create_folder()
max_page_file = open(today_folder + "/max_page_number.txt", "r")
max_page_number = max_page_file.readlines()
for i in range(0, len(max_page_number)):
    max_page_number[i] = max_page_number[i].replace('\n', '')

id_position = 0

if os.path.isfile(delta_folder + '/list_id.txt'):
    dictionary_url = {}
    file = open(delta_folder + '/list_new_id.txt', 'r')
    for line in file.readlines():
        dictionary_url[line.replace('\n','')] = 1
    file.close()

    if '-1' in dictionary_url.keys():
        dictionary_url.pop('-1')
        file = open(delta_folder + '/list_id.txt', 'r')
        for line in file.readlines():
            dictionary_url[line.replace('\n','')] = 1
        file.close()


class DownloadSiteYouhomesSpider(scrapy.Spider):
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
                "https://youhomes.vn/mua/can-ho-26.html?page=" + str(page_number + 1))

        for page_number in range(0, int(max_page_number[1])):
            urls.append(
                "https://youhomes.vn/mua/nha-tho-cu-48.html?page=" + str(page_number + 1))
        return urls

    def requests_site_for_lease(self):
        global max_page_number
        urls = []
        print("MAX PAGE NUMBER FOR SALE: ", int(max_page_number[2]))
        for page_number in range(0, int(max_page_number[2])):
            urls.append(
                "https://youhomes.vn/thue/can-ho-36.html?page=" + str(page_number + 1))
        for page_number in range(0, int(max_page_number[3])):
            urls.append(
                "https://youhomes.vn/thue/nha-tho-cu-51.html?page=" + str(page_number + 1))
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
        page = response.url.split("=")[-1]
        filename = 'page-mua-ban-bat-dong-san-%s.html' % page
        if (response.url.find('can-ho') > 0):
            with open(apartment_sale_folder + '/' + filename, 'wb') as f:
                f.write(response.body)
        else:
            with open(house_sale_folder + '/' + filename, 'wb') as f:
                f.write(response.body)
        self.log('Saved file %s' % filename)

    def download_list_mode_for_lease(self, response):
        page = response.url.split("=")[-1]
        filename = 'page-thue-bat-dong-san-%s.html' % page
        if (response.url.find('can-ho') > 0):
            with open(apartment_lease_folder + '/' + filename, 'wb') as f:
                f.write(response.body)
        else:
            with open(house_lease_folder + '/' + filename, 'wb') as f:
                f.write(response.body)
        self.log('Saved file %s' % filename)


class DownloadAdsYouhomesSpider(scrapy.Spider):
    """
    Reference link: https://docs.scrapy.org/en/latest/topics/spiders.html
    """

    name = "download_ads"

    def requests_ads(self):
        return list(dictionary_url.keys())        

    def start_requests(self):
        start = time()
        print("==================Start download ads===================")
        urls_ads = self.requests_ads()
        for url in urls_ads:
            print("Ads: ", urls_ads.index(url) + 1)
            yield scrapy.Request(url=url, callback=self.download_detail_mode, meta = {
                  'dont_redirect': True,
                  'handle_httpstatus_list': [302]
              })
        delta = time()
        print(
            '==================%s SECONDS===========================' %
            (delta - start))

    def download_detail_mode(self, response):
        global id_position
        id_position = id_position + 1
        filename = '%s.html' % str(id_position)
        with open(all_folder + '/' + filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
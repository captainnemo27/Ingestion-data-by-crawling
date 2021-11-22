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
import nhadatcafeland_helper
folder, today, today_folder, all_folder, delta_folder, list_mode = nhadatcafeland_helper.create_folder()
max_page_file = open(today_folder + "/max_page_number.txt", "r")
max_page_number = max_page_file.readlines()

if os.path.isfile(delta_folder + '/list_id.txt'):
    dictionary_id = {}
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

    def requests_site(self):
        global max_page_number
        urls = []
        for i in range(0, len(max_page_number)):
            s=max_page_number[i].split()
            number_site=s[0]
            url_site=s[1]
            print("MAX PAGE NUMBER FOR %s is %s" % (url_site, number_site))
            for page_number in range(0,int(number_site)):
                urls.append(url_site+"page-"+str(page_number + 1))
        return urls

    def start_requests(self):
        print("==================Start download site==================")
        start = time()
        urls_site = self.requests_site()
        for url in urls_site:
            print("Page: ", urls_site.index(url) + 1)
            yield scrapy.Request(url=url, callback=self.download_list_mode , headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}, dont_filter=True)#, meta={"proxy": "http://172.16.1.11:3128/"})

        delta = time()
        print(
            '==================%s SECONDS===========================' %
            (delta - start))

    def download_list_mode(self, response):
        link = response.url.split("tai-")[0]
        land = link.split("cafeland.vn")[-1]
        location = response.url.split("tai-")[-1]
        page = land+""+location
        filename = 'page-list%s' % page[:-1].replace("/","-") + ".html"
        with open(list_mode + '/' + filename, 'wb') as f:
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
            yield scrapy.Request(url=url, callback=self.download_detail_mode, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"})#, meta={"proxy": "http://172.16.1.11:3128/"})
        delta = time()
        print(
            '==================%s SECONDS===========================' %
            (delta - start))

    def download_detail_mode(self, response):
        page = response.url.split("-")[-1]
        filename = '%s' % str(page)
        with open(all_folder + '/' + filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


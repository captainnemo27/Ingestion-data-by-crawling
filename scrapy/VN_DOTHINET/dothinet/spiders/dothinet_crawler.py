import scrapy
from dothinet.items import DothinetItem
import logging
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, FormRequest
from scrapy_splash import SplashRequest

import os
import re

logging.getLogger ('scrapy').propagate = False


class DothinetCrawlerSpider(scrapy.Spider):
    name = 'dothinet_crawler'
    allowed_domains = ['dothinet.vn']
    # start_urls = ['http://dothinet.vn/']

    def start_requests(self):
        data_dir = self.settings['FILES_STORE'] 
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            os.makedirs(data_dir+"/ALL")
        
        tab_file = data_dir + "/DELTA/extract.tab"
        with open(tab_file) as f:
            for url in f.readlines():
                item = DothinetItem()
                ads = url.strip().split("\t")
                # We need to check this has the http prefix or we get a Missing scheme error
                if not ads[1].startswith('http://') and not ads[1].startswith('https://'):
                    ads[1] = 'https://' + ads[1]
                                
                item['file_url'] = ads[1]
                filename = data_dir + "/ALL/annonce_" + ads[0] + ".txt"   
                item['filename'] = filename
                
                if os.path.exists(filename): 
                    self.log('INFO: file already exists {}'.format(filename))
                else:
                    #yield scrapy.Request(url = item['file_url'], meta = {'filename': filename}, callback = self.parse)  
                    yield SplashRequest(item['file_url'], self.parse, errback = lambda x: self.download_errback(x, item['file_url']), args={'wait': 1, 'proxy': 'http://172.16.1.11:3128', 'timeout': 1200, 'images': 0}, meta = {'filename': filename, 'handle_httpstatus_all': True})
           
    def parse(self, response):
        print('##########')
        print('Processing : ', response.url)
        self.logger.info('response.url=%s' % response.url)
        filename = response.meta['filename']
        with open(filename, 'wb') as f:
            f.write(response.body)

    def download_errback(self, e, url):
        print (type(e), repr(e))
        print (repr(e.value))
        print (url)



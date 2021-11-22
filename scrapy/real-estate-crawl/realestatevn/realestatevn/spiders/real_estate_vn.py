# -*- coding: utf-8 -*-
import os 
from urllib.parse import urlparse
import scrapy 
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule 
from scrapy.http.request import Request
import re
#used to scrap URLs
import yaml


class RealEstateVnSpider(CrawlSpider):
    name = 'real_estate_vn'
    custom_settings = {'HTTPERROR_ALLOW_ALL': True}
    outdir = ""
    org_url = ""
    xpath_ads_link = ""
    def __init__(self,outdir, config_file = None, *args, **kwargs):
        
        self.outdir = outdir
        handle_httpstatus_all = True    

        with open(config_file) as f:                                            
            self._config = yaml.safe_load(f)
    
        self.start_urls = self._config['start_urls']
        self.allowed_domains = self._config['rules']['allowed_domains']
        self.org_url = self._config['rules']['org_url']
        self.xpath_ads_link = self._config['rules']['xpath_ads_link']
        self.rules = (
            Rule(LinkExtractor(
                    allow=self._config['rules']['ads_link']), callback='parse'
            ),
            Rule(LinkExtractor(
                allow=self._config['rules']['page'] ),follow=True),
            )                    
        super(RealEstateVnSpider, self).__init__(*args, **kwargs)                             
        
        if not os.path.exists(outdir):
            os.makedirs(outdir)
            os.makedirs(outdir+"/ALL")
            
    
    def parse(self, response):
        try:              
            list_ads = response.xpath(self.xpath_ads_link).extract()
            for link in list_ads:
                if link != None and link.find(self.org_url) == -1:
                   link =  self.org_url + link
                   print ("Processing: ", link)
                yield Request(link.rstrip('\n\r'), self.download_all_files)

        except BaseException:
            print("NO LINKS !!!")

    def download_all_files(self, response):               
        id_page = urlparse(response.url).path.replace("/","")
        filename = self.outdir + "/ALL/annonce_" + str(id_page) + ".txt"
        #print (filename)
        if ( not os.path.exists(filename) ):
            with open(filename, 'wb') as f:
                f.write(response.body)                  
                
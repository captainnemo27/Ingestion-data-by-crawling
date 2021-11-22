import os
import os.path
import scrapy
from time import time
import sys
os.chdir("..")
os.chdir("..")
sys.path.insert(1, os.getcwd()+'/python/')
import chotot_helper
folder, today, today_folder, spider_folder, all_folder, delta_folder, list_mode = chotot_helper.create_folder()

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


class DownloadSiteChoTot(scrapy.Spider):
    """
    Reference link: https://docs.scrapy.org/en/latest/topics/spiders.html
    """
    name = "download_site"
            
    def requests_site(self):
        urls = []
        max_page_file = open(today_folder + "/max_page_number.txt", "r")
        max_page_number = int(max_page_file.readline())
    
        print("MAX PAGE NUMBER: ", max_page_number)
        for page_number in range(0,max_page_number):
            num = page_number*50
            urls.append("https://gateway.chotot.com/v1/public/ad-listing?cg=1000&limit=50&o="+str(num)+"&page="+str(page_number+1)) 
        return urls
    
    def start_requests(self):
        start = time()
        print("==================Start download site==================")
        urls_site = self.requests_site()
        for url in urls_site:
            print("Page number: ",urls_site.index(url)+1)
            yield scrapy.Request(url=url, callback=self.download_list_mode)

        delta = time()
        print('==================%s SECONDS===========================' % (delta - start))


    def download_list_mode(self, response):
        page = response.url.split("=")[-1]
        filename = 'page-mua-ban-bat-dong-san-%s.json' % page
        with open(list_mode+'/'+filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

class DownloadAdsChoTot(scrapy.Spider):
    """
    Reference link: https://docs.scrapy.org/en/latest/topics/spiders.html
    """
    name = "download_ads"
            
    def requests_ads(self):
        return list(dictionary_id.values())

    def start_requests(self):
        start = time()
        print("==================Start download ads===================")
        urls_ads = self.requests_ads()
        for url in urls_ads:
            print("Ads: ", urls_ads.index(url))
            yield scrapy.Request(url=url, callback=self.download_detail_mode)
        delta = time()
        print('==================%s SECONDS===========================' % (delta - start)) 

    def download_detail_mode(self, response):
        page = response.url.split("/")[-1]
        filename = '%s.json' % page
        with open(all_folder+'/'+filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

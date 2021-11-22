from scrapy import cmdline
import sys


# Running: python3 start_crawler.py "20201215"
# Define variable
# 20201215  
folder = str(sys.argv[1]) 


req = "scrapy crawl dothinet_crawler -s FILES_STORE=" + folder 
print("Running scrapy command-line: ", req)
cmdline.execute(req.split())
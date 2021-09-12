from scrapy import cmdline
import sys


# Running: python3 start_crawler.py "20201215" dothinet.yml
# Define variable
# 20201215  
folder = str(sys.argv[1]) 
config_file = str(sys.argv[2]) 


req = "scrapy crawl real_estate_vn -a outdir=" + folder  + "  -a config_file=" + config_file
print("Running scrapy command-line: ", req)
cmdline.execute(req.split())
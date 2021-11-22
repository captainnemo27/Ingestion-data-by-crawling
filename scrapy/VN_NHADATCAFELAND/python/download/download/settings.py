# Scrapy settings for download project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'download'

SPIDER_MODULES = ['download.spiders']
NEWSPIDER_MODULE = 'download.spiders'

DOWNLOADER_MIDDLEWARES = {
    # Custom proxy
    'download.middlewares.CustomProxyMiddleware': 350,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
} 

# DOWNLOADER_MIDDLEWARES  =  { 
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware' :  110 , 
#     'tor_ip_rotator.middlewares.TorProxyMiddleware' :  100,
# }
# PROXY_POOL_ENABLED = True
# PROXY_POOL_FILTER_CODE = 'sg'

# DOWNLOADER_MIDDLEWARES = {
#     # ...
#     'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
#     'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
#     # ...
# }
# PROXY_POOL_BAN_POLICY = 'download.policy.MyPolicy'

# TOR_IPROTATOR_ENABLED  =  True 
# TOR_IPROTATOR_CHANGE_AFTER  =  10# number of requests made to the same IP address
# TOR_IPROTATOR_ALLOW_REUSE_IP_AFTER  = 10
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'# Proxy list containing entries like
# http://host1:port
# http://username:password@host2:port
# http://host3:port
# ...
# print("===================================================")
import os
# CUSTOM_PROXY = "http://172.16.1.11:3128"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'download (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
##################
# CONCURRENT_ITEMS = 200
# CONCURRENT_REQUESTS_PER_DOMAIN = 50
CONCURRENT_REQUESTS = 50
##################
CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'download.middlewares.DownloadSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#   'download.middlewares.DownloadDownloaderMiddleware': 543,
#   'download.middlewares.DownloadDownloaderMiddleware' : 350,
#   'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
# }
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
#     'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
#     'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
# }
# FAKEUSERAGENT_PROVIDERS = [
#     'scrapy_fake_useragent.providers.FakeUserAgentProvider',
#     'scrapy_fake_useragent.providers.FakerProvider',
#     'scrapy_fake_useragent.providers.FixedUserAgentProvider',
#     'mypackage.providers.CustomProvider'
# ]
# FAKEUSERAGENT_FALLBACK = 'Mozilla/5.0 (Android; Mobile; rv:40.0)'

# USER_AGENT = '<your user agent string which you will fall back to if all other providers fail>'

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'download.pipelines.DownloadPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# # The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# # The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 20
# # The average number of requests Scrapy should be sending in parallel to
# # each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

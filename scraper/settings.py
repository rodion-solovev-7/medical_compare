import config

# Scrapy settings for scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = config.BOT_NAME

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = config.USER_AGENT
USER_AGENT_LIST = config.USER_AGENT_LIST

# Obey robots.txt rules
ROBOTSTXT_OBEY = config.ROBOTSTXT_OBEY

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = config.CONCURRENT_REQUESTS

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = config.DOWNLOAD_DELAY
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

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
#    'scraper.middlewares.ScraperSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # Replace default useragent by random
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scraper.middlewares.RandomUserAgentMiddleware': 400,
    # 'scraper.middlewares.ScraperDownloaderMiddleware': 543,
}

# This points to your local proxy server that talks to Tor
SCRAPER_TOR_HTTP_PROXY = config.SCRAPER_TOR_HTTP_PROXY
if SCRAPER_TOR_HTTP_PROXY is not None:
    # Tor Proxy Middleware
    DOWNLOADER_MIDDLEWARES.update({
        'scraper.middlewares.ProxyMiddleware': 350,
    })

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'scraper.pipelines.ScraperPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = config.AUTOTHROTTLE_ENABLED
# The initial download delay
AUTOTHROTTLE_START_DELAY = config.AUTOTHROTTLE_START_DELAY
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = config.AUTOTHROTTLE_MAX_DELAY
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = config.AUTOTHROTTLE_TARGET_CONCURRENCY
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = config.AUTOTHROTTLE_DEBUG

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = config.HTTPCACHE_ENABLED
HTTPCACHE_EXPIRATION_SECS = config.HTTPCACHE_EXPIRATION_SECS
HTTPCACHE_DIR = config.HTTPCACHE_DIR
HTTPCACHE_IGNORE_HTTP_CODES = config.HTTPCACHE_IGNORE_HTTP_CODES
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = config.REQUEST_FINGERPRINTER_IMPLEMENTATION
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

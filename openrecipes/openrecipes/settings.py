# Scrapy settings for thepioneerwoman project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'openrecipes'

SPIDER_MODULES = ['openrecipes.spiders']
NEWSPIDER_MODULE = 'openrecipes.spiders'

ITEM_PIPELINES = [
    'openrecipes.pipelines.MakestringsPipeline',
    'openrecipes.pipelines.DuplicaterecipePipeline',
]

CONCURRENT_REQUESTS_PER_DOMAIN = 2

DOWNLOAD_DELAY = 0.5
RANDOMIZE_DOWNLOAD_DELAY = True
DOWNLOADER_DEBUG = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31 openrecipes (+http://openrecip.es)'

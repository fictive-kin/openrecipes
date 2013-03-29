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

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'openrecipes (+http://openrecip.es)'

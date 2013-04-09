from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import XmlXPathSelector
from openrecipes.spiders.elanaspantry_spider import ElanaspantryMixin


class ElanaspantryfeedSpider(BaseSpider, ElanaspantryMixin):
    name = "elanaspantry.feed"
    allowed_domains = [
        "www.elanaspantry.com",
        "feeds.feedburner.com",
        "feedproxy.google.com",
    ]
    start_urls = [
        "http://feeds.feedburner.com/elanaspantry",
    ]

    def parse(self, response):
        xxs = XmlXPathSelector(response)
        links = xxs.select("//item/*[local-name()='origLink']/text()").extract()

        return [Request(x, callback=self.parse_item) for x in links]

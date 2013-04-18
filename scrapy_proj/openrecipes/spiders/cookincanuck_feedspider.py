from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import XmlXPathSelector
from openrecipes.spiders.cookincanuck_spider import CookincanuckMixin


class CookincanuckfeedSpider(BaseSpider, CookincanuckMixin):

    name = "cookincanuck.feed"
    allowed_domains = [
        "cookincanuck.com",
        "feeds.feedburner.com",
        "feedproxy.google.com"
    ]
    start_urls = [
        "http://feeds.feedburner.com/blogspot/hIdj",
    ]

    def parse(self, response):

        xxs = XmlXPathSelector(response)
        links = xxs.select("//item/*[local-name()='origLink']/text()").extract()

        return [Request(x, callback=self.parse_item) for x in links]

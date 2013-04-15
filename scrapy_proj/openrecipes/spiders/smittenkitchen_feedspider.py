from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import XmlXPathSelector
from openrecipes.spiders.smittenkitchen_spider import SmittenkitchenMixin


class SmittenkitchenfeedSpider(BaseSpider, SmittenkitchenMixin):
    name = "smittenkitchen.feed"
    allowed_domains = [
        "smittenkitchen.com",
        "feeds.feedburner.com",
        "feedproxy.google.com",
    ]
    start_urls = [
        "http://feeds.feedburner.com/smittenkitchen",
    ]

    def parse(self, response):
        xxs = XmlXPathSelector(response)
        links = xxs.select("TODO").extract()

        return [Request(x, callback=self.parse_item) for x in links]

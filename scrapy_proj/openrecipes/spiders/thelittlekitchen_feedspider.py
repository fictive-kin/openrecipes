from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import XmlXPathSelector
from openrecipes.spiders.thelittlekitchen_spider import ThelittlekitchenMixin


class ThelittlekitchenfeedSpider(BaseSpider, ThelittlekitchenMixin):
    name = "thelittlekitchen.feed"
    allowed_domains = [
        "www.thelittlekitchen.net",
    ]
    start_urls = [
        "http://www.thelittlekitchen.net/feed/",
    ]

    def parse(self, response):
        xxs = XmlXPathSelector(response)
        links = xxs.select("//item/*[local-name()='link']/text()").extract()

        return [Request(x, callback=self.parse_item) for x in links]

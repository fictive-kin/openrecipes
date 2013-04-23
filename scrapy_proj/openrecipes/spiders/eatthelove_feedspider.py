from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import XmlXPathSelector
from openrecipes.spiders.eatthelove_spider import EattheloveMixin


class EatthelovefeedSpider(BaseSpider, EattheloveMixin):
    name = "eatthelove.feed"
    allowed_domains = [
        "www.eatthelove.com",
        "feeds.feedburner.com",
        "feedproxy.google.com",
    ]
    start_urls = [
        "http://feeds.feedburner.com/eatthelove/feed",
    ]

    def parse(self, response):
        xxs = XmlXPathSelector(response)
        links = xxs.select("//link/text()").extract()

        return [Request(x, callback=self.parse_item) for x in links]

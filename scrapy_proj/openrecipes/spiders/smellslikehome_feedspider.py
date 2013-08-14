from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import XmlXPathSelector
from openrecipes.spiders.smellslikehome_spider import SmellslikehomeMixin


class SmellslikehomefeedSpider(BaseSpider, SmellslikehomeMixin):
    name = "smellslikehome.feed"
    allowed_domains = [
        "www.smells-like-home.com",
        "feeds.feedburner.com",
        "feedproxy.google.com",
    ]
    start_urls = [
        "http://www.smells-like-home.com/feed/",
    ]

    def parse(self, response):
        xxs = XmlXPathSelector(response)
        links = xxs.select("//item/*[local-name()='link']/text()").extract()

        return [Request(x, callback=self.parse_item) for x in links]

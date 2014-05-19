from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import XmlXPathSelector
from openrecipes.spiders.twopeasandtheirpod_spider import TwopeasandtheirpodMixin


class TwopeasandtheirpodfeedSpider(BaseSpider, TwopeasandtheirpodMixin):

    name = "twopeasandtheirpod.feed"

    allowed_domains = [
        "twopeasandtheirpod.com",
        "feeds.feedburner.com",
        "feedproxy.google.com"
    ]
    start_urls = [
        "http://feeds.feedburner.com/twopeasandtheirpod/rNNF",
    ]

    def parse(self, response):

        xxs = XmlXPathSelector(response)
        links = xxs.select("//item/*[local-name()='origLink']/text()").extract()

        return [Request(x, callback=self.parse_item) for x in links]

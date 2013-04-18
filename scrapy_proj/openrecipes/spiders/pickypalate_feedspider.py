from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import XmlXPathSelector
from openrecipes.spiders.pickypalate_spider import PickypalateMixin


class PickypalatefeedSpider(BaseSpider, PickypalateMixin):

    name = "pickypalate.feed"
    allowed_domains = [
        "picky-palate.com",
        "feeds.feedburner.com",
        "feedproxy.google.com"
    ]
    start_urls = [
        "http://feeds.feedburner.com/PickyPalate",
    ]

    def parse(self, response):

        xxs = XmlXPathSelector(response)
        links = xxs.select("//item/*[local-name()='origLink']/text()").extract()

        return [Request(x, callback=self.parse_item) for x in links]
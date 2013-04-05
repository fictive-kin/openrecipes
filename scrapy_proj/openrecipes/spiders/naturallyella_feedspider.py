from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import XmlXPathSelector
from openrecipes.spiders.naturallyella_spider import NaturallyEllaMixin


class NaturallyEllaFeedSpider(BaseSpider, NaturallyEllaMixin):

    name = "naturallyella.feed"
    allowed_domains = [
        "naturallyella.com",
        "feeds.feedburner.com",
        "feedproxy.google.com"
    ]
    start_urls = [
        "http://feeds.feedburner.com/naturallyella",
    ]

    def parse(self, response):

        xxs = XmlXPathSelector(response)
        links = xxs.select("//item/*[local-name()='origLink']/text()").extract()

        return [Request(x, callback=self.parse_item) for x in links]

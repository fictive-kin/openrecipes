from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import XmlXPathSelector
from openrecipes.spiders.fortheloveofcooking_spider import FortheloveofcookingMixin


class FortheloveofcookingfeedSpider(BaseSpider, FortheloveofcookingMixin):

    name = "fortheloveofcooking.feed"
    allowed_domains = [
        "fortheloveofcooking.net",
        "feeds.feedburner.com",
        "feedproxy.google.com"
    ]
    start_urls = [
        "http://feeds.feedburner.com/blogspot/OlvyH",
    ]

    def parse(self, response):

        xxs = XmlXPathSelector(response)
        links = xxs.select("//item/*[local-name()='origLink']/text()").extract()

        return [Request(x, callback=self.parse_item) for x in links]

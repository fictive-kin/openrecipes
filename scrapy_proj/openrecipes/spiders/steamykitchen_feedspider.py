from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import XmlXPathSelector
from openrecipes.spiders.steamykitchen_spider import SteamykitchenMixin


class SteamykitchenfeedSpider(BaseSpider, SteamykitchenMixin):

    name = "steamykitchen.feed"

    allowed_domains = [
        "steamykitchen.com",
        "feeds.feedburner.com",
        "feedproxy.google.com"
    ]
    start_urls = [
        "http://feeds.feedburner.com/SteamyKitchen",
    ]

    def parse(self, response):

        xxs = XmlXPathSelector(response)
        links = xxs.select("//item/*[local-name()='origLink']/text()").extract()

        return [Request(x, callback=self.parse_item) for x in links]

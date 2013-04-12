from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import XmlXPathSelector
from openrecipes.spiders.epicurious_spider import EpicuriousMixin


class EpicuriousfeedSpider(BaseSpider, EpicuriousMixin):
    """
    Uses the Epicurious recipes feed to get newly added items.
    """
    name = "epicurious.feed"
    allowed_domains = [
        "epicurious.com"
    ]
    start_urls = [
        "http://feeds.epicurious.com/newrecipes",
    ]

    def parse(self, response):

        xxs = XmlXPathSelector(response)
        links = xxs.select("//item/*[local-name()='origLink']/text()").extract()

        return [Request(x, callback=self.parse_item) for x in links]

from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import XmlXPathSelector
from openrecipes.spiders.simplyrecipes_spider import SimplyrecipesMixin


class SimplyrecipesfeedSpider(BaseSpider, SimplyrecipesMixin):

    name = "simplyrecipes.feed"
    allowed_domains = [
        "simplyrecipes.com",
        "feeds.feedburner.com",
        "feedproxy.google.com"
    ]
    start_urls = [
        "http://feeds.feedburner.com/SimplyRecipesRecipesOnly",
    ]

    def parse(self, response):

        xxs = XmlXPathSelector(response)
        links = xxs.select("//item/*[local-name()='origLink']/text()").extract()

        return [Request(x, callback=self.parse_item) for x in links]

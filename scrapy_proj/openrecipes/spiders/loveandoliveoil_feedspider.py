from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import XmlXPathSelector
from openrecipes.spiders.loveandoliveoil_spider import Loveandoliveoil_Mixin


class LoveandoliveoilfeedSpider(BaseSpider, Loveandoliveoil_Mixin):

    name = "loveandoliveoil.feed"

    allowed_domains = [
        "loveandoliveoil.com",
        "feeds.feedburner.com"
    ]
    start_urls = [
        "http://feeds.feedburner.com/loveandoliveoil",
    ]

    def parse(self, response):

        xxs = XmlXPathSelector(response)
        links = xxs.select("//link/text()").extract()

        return [Request(x, callback=self.parse_item) for x in links]

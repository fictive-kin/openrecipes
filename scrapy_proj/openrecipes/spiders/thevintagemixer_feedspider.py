from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import XmlXPathSelector
from openrecipes.spiders.thevintagemixer_spider import TheVintageMixerMixin


class TheVintageMixerFeedSpider(BaseSpider, TheVintageMixerMixin):

    name = "thevintagemixer.feed"
    allowed_domains = [
        "thevintagemixer.com"
    ]
    start_urls = [
        "http://www.thevintagemixer.com/category/vintage-mixer/feed/",
    ]

    def parse(self, response):

        xxs = XmlXPathSelector(response)
        links = xxs.select('//item/*[local-name()="link"]/text()').extract()

        return [Request(x, callback=self.parse_item) for x in links]

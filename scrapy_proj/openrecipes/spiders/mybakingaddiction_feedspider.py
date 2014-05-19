from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import XmlXPathSelector
from openrecipes.spiders.mybakingaddiction_spider import MybakingaddictionMixin


class MybakingaddictionfeedSpider(BaseSpider, MybakingaddictionMixin):

    name = "mybakingaddiction.feed"
    allowed_domains = [
        "mybakingaddiction.com",
        "feeds.feedburner.com",
        "feedproxy.google.com"
    ]
    start_urls = [
        "http://feeds.feedburner.com/mybakingaddiction",
    ]

    def parse(self, response):

        xxs = XmlXPathSelector(response)
        #check later
        links = xxs.select("//item/*[local-name()='origLink']/text()").extract()

        return [Request(x, callback=self.parse_item) for x in links]

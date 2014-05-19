from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import XmlXPathSelector
from openrecipes.spiders.dashingdish_spider import Dashingdish_spiderMixin


class DashingdishfeedSpider(BaseSpider, Dashingdish_spiderMixin):

    name = "dashingdish.feed"
    allowed_domains = [
        "dashingdish.com",
        "feeds.feedburner.com",
        "feedproxy.google.com"
    ]
    start_urls = [
        "http://feeds.feedburner.com/dashingdish-recipes",
    ]

    def parse(self, response):

        xxs = XmlXPathSelector(response)
        links = xxs.select("//item/*[local-name()='origLink']/text()").extract()

        return [Request(x, callback=self.parse_item) for x in links]

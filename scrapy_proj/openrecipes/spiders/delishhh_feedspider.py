from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import XmlXPathSelector
from openrecipes.spiders.delishhh_spider import DelishhhMixin


class DelishhhfeedSpider(BaseSpider, DelishhhMixin):
    """
    This parses the RSS feed for delishhh.com, grabs the original
    links to each entry, and scrapes just those pages. This should be used
    to keep up to date after we have backfilled the existing recipes by
    crawling the whole site
    """
    name = "delishhh.feed"
    allowed_domains = [
        "delishhh.com",
        "feeds.feedburner.com",
        "feedproxy.google.com"
    ]
    start_urls = [
        "http://feeds.feedburner.com/delishhh",
    ]

    def parse(self, response):
        """
        We define a custom parser here because we need to get the link from
        the feed item and then follow it to get the recipe data.

        Getting the data from <content:encoded> seems overly complex, as we
        would have to decode all the encoded characters and then build a DOM
        from that.
        """
        xxs = XmlXPathSelector(response)
        links = xxs.select("//item/*[local-name()='origLink']/text()").extract()

        # self.parse_item comes from OnehundredonecookbooksMixin
        return [Request(x, callback=self.parse_item) for x in links]

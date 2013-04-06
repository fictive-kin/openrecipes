from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem
from ..util import JQ


class BellalimentocrawlSpider(CrawlSpider):

    name = "www.bellalimento.com"
    allowed_domains = ["www.bellalimento.com"]
    start_urls = [
        "http://www.bellalimento.com/",
    ]

    # a tuple of Rules that are used to extract links from the HTML page
    rules = (
        Rule(SgmlLinkExtractor(allow=('/category/.+'))),
        Rule(SgmlLinkExtractor(allow=('/\d\d\d\d/\d\d/\d\d/')), callback='parse_item'),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        jq = JQ(hxs)
        item = RecipeItem()
        item['source'] = 'bellalimento'
        item['name'] = jq.select('#zlrecipe-title,.title').text()[0]
        name = item['name']

        item['image'] = jq.select('img[title~="%s"],img[alt~="%s"],img[title="%s"],img[alt="%s"]' % (name, name, name, name)).attr('src')
        if not item['image']:
            item['image'] = jq.select('img.size-full, img.size-large').attr('src')

        item['url'] = response.url

        item['ingredients'] = jq.select('[itemprop="ingredients"]').text()

        return [item]

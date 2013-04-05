from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem
from ..util import JQ


class ChezUsMixin(object):
    # this is the source string we'll store in the DB to aggregate stuff
    # from a single source
    source = 'chezus'

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        base_path = """//td[@id="content"]"""

        recipes_scopes = hxs.select(base_path)

        description_path = '//*[@data-role="content"]/p/text()'
        ingredients_path = '//*[@itemprop="ingredients"]/text()'

        recipes = []

        for r_scope in recipes_scopes:
            jq = JQ(r_scope)
            item = RecipeItem()

            item['source'] = self.source

            item['name'] = jq.select('[itemprop="name"]').text()
            if not item['name']:
                item['name'] = [''.join(jq.select('.article-title').text()).split('|')[-1].strip()]
            name = item['name'][0]

            image_path = '//img[contains(@alt, "' + name + '")]/@src'
            item['image'] = r_scope.select(image_path).extract()

            item['url'] = response.url
            item['description'] = r_scope.select(description_path).extract()

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = [i.strip() for i in ingredient_scopes.extract()]
            if not ingredients:
                ingredients = jq.select('ul li').text()
            item['ingredients'] = ingredients

            recipes.append(item)

        return recipes


class ChezuscrawlSpider(CrawlSpider, ChezUsMixin):
    name = "chezus"
    allowed_domains = ["chezus.com"]
    start_urls = [
        "http://chezus.com/",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/page/\d.+/'))),

        Rule(SgmlLinkExtractor(allow=('/\d\d\d\d/\d\d/\d\d/.*/')),
             callback='parse_item'),
    )

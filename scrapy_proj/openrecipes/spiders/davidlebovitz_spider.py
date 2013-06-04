from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class DavidlebovitzMixin(object):
    source = 'davidlebovitz'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = '//*[@class="post hrecipe"]'

        recipes_scopes = hxs.select(base_path)

        name_path = '//*[@class="title fn"]/text()'
        image_path = '//*[@class="photo"]/@src'
        ingredients_path = '//ul[@class="ingredient_list"]/li/text()'

        recipes = []

        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', response.url)

            il.add_value('ingredients', r_scope.select(ingredients_path).extract())

            recipes.append(il.load_item())

        return recipes


class DavidlebovitzcrawlSpider(CrawlSpider, DavidlebovitzMixin):

    name = "davidlebovitz.com"

    allowed_domains = ["www.davidlebovitz.com"]

    start_urls = [
        "http://www.davidlebovitz.com/category/recipes/"
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/category/recipes/'))),

        Rule(SgmlLinkExtractor(allow=('\/\d\d\d\d\/\d\d\/[a-zA-Z_]+/?')),
             callback='parse_item'),
    )

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class TablespoonMixin(object):
    source = 'tablespoon'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = '//*[@class="recipe-area hrecipe"]'

        recipes_scopes = hxs.select(base_path)

        name_path = '//*[@class="fn"]/text()'
        description_path = '//*[@class="summary"]/text()'
        image_path = '//*[@class="photo"]/@src'
        recipeYield_path = '//*[@class="servings"]/text()'

        recipes = []

        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', response.url)
            il.add_value('description', r_scope.select(description_path).extract())
            il.add_value('recipeYield', r_scope.select(recipeYield_path).extract())

            recipes.append(il.load_item())

        return recipes


class TablespooncrawlSpider(CrawlSpider, TablespoonMixin):

    name = "tablespoon.com"

    allowed_domains = ["tablespoon.com"]

    start_urls = [
        "http://www.tablespoon.com/search/#&page_type=",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/search/#&page_type=&sort=&page=\d+'))),

        Rule(SgmlLinkExtractor(allow=('/recipes/\[a-z]+/\d+/')),
             callback='parse_item'),
    )

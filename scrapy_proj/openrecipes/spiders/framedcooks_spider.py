from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader
import re


class FramedcooksMixin(object):
    source = 'framedcooks'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = '//*[@itemtype="http://schema.org/Recipe"]'

        recipes_scopes = hxs.select(base_path)

        name_path = '//*[@itemprop="name"]/text()'
        image_path = '//*[@itemprop="image"]/@src'
        recipeYield_path = '//*[@itemprop="recipeYield"]/text()'
        ingredients_path = '//*[@itemprop="ingredients"]/text()'
        datePublished = '//*[@class="date published time"]/text()'

        recipes = []

        label_regex = re.compile(r'^For ')

        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', response.url)
            il.add_value('recipeYield', r_scope.select(recipeYield_path).extract())

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                ingredient = i_scope.extract().strip()
                if not label_regex.match(ingredient) and not ingredient.endswith(':'):
                    ingredients.append(ingredient)
            il.add_value('ingredients', ingredients)

            il.add_value('datePublished', r_scope.select(datePublished).extract())

            recipes.append(il.load_item())

        return recipes


class FramedcookscrawlSpider(CrawlSpider, FramedcooksMixin):

    name = "framedcooks.com"

    allowed_domains = ["framedcooks.com"]

    start_urls = [
        "http://www.framedcooks.com/?s=.",
    ]

    rules = (
        #may want double check this reg exp.
        Rule(SgmlLinkExtractor(allow=('/page/\d+?s=.'))),

        Rule(SgmlLinkExtractor(allow=('/\d+/\d+/\[a-z]+.html')),
             callback='parse_item'),
    )

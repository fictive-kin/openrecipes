from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class WilliamsSonomaMixin(object):
    source = 'williamssonoma'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = """//*[contains(concat(' ', normalize-space(@class), ' '),
                        ' hrecipe ')]"""
        recipes_scopes = hxs.select(base_path)

        name_path = '//*[@class="fn"]/text()'
        description_path = '//*[@class="recipe-description summary"]/p/text()'
        image_path = '//img[@class="photo"]/@src'
        recipeYield_path = '//*[@class="directions"]/p/text()'
        ingredients_path = '//*[@class="ingredient"]/text()'

        recipes = []

        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', response.url)
            il.add_value('description',
                         r_scope.select(description_path).extract())

            # yield given somewhere in description 'Serves n.'
            il.add_value('recipeYield',
                         r_scope.select(recipeYield_path).re('Serves \d\.'))

            il.add_value('ingredients',
                         r_scope.select(ingredients_path).extract())

            recipes.append(il.load_item())

        return recipes


class WilliamsSonomacrawlSpider(CrawlSpider, WilliamsSonomaMixin):

    name = "williams-sonoma.com"

    allowed_domains = ["www.williams-sonoma.com"]

    start_urls = [
        "http://www.williams-sonoma.com/recipe/",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/recipe/[\w\-]+\.html')),
             callback='parse_item'),
        Rule(SgmlLinkExtractor(allow=('/recipe/.+'))),
    )

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader
import re

RECIPE_THRESHOLD = 2/3


def ingredient_heuristic(container):
    ingredient_regexp = re.compile(r'^(\d+[^\.]|salt|pepper|few|handful|pinch|some|dash)', re.IGNORECASE)
    text_nodes = container.select('text()')
    if len(text_nodes) == 0:
        return 0
    numbercount = 0
    for node in text_nodes:
        if ingredient_regexp.match(node.extract().strip()):
            numbercount += 1

    return float(numbercount) / len(text_nodes)


class MybakingaddictionMixin(object):
    source = 'mybakingaddiction'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = '//*[@class="hrecipe"]'

        recipes_scopes = hxs.select(base_path)

        name_path = '//h1[@class="fn"]/text()'
        description_path = '//div[@class="format_text entry-content jpibfi_container"]/p/text()'
        image_path = '//*[@class="photo"]/@src'
        #prepTime_path = 'TODO'
        #cookTime_path = 'TODO'
        #recipeYield_path = 'TODO'
        #  ingredients is only displaying first item, I assume the /br is messing with it.
        ingredients_path = '//*[@class="ingredient"]'
        datePublished = '//span[@class="published"]/text()'

        recipes = []

        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', response.url)
            il.add_value('description', r_scope.select(description_path).extract())

            #il.add_value('prepTime', r_scope.select(prepTime_path).extract())
            #il.add_value('cookTime', r_scope.select(cookTime_path).extract())
            #il.add_value('recipeYield', r_scope.select(recipeYield_path).extract())

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                if ingredient_heuristic(i_scope) > RECIPE_THRESHOLD:
                    for ingredient in i_scope.select('text()'):
                        ingredients.append(ingredient.extract().strip())

            il.add_value('ingredients', ingredients)

            il.add_value('datePublished', r_scope.select(datePublished).extract())

            recipes.append(il.load_item())

        return recipes


class MybakingaddictioncrawlSpider(CrawlSpider, MybakingaddictionMixin):

    name = "www.mybakingaddiction.com"

    allowed_domains = ["www.mybakingaddiction.com"]

    start_urls = [
        "http://www.mybakingaddiction.com/recipe-index/"


    ]

    rules = (
        (SgmlLinkExtractor(allow=('/[^/]+/?'))),

        Rule(SgmlLinkExtractor(allow=('/.+/')),
             callback='parse_item'),
    )

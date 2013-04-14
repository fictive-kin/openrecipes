from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader
import re

# made up number that governs how many ingredient-seeming things need to be in a
# word container before we decide that it's a list of ingredients
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


class SmittenkitchenMixin(object):
    source = 'smittenkitchen'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = '//div[@class="post"]'

        recipes_scopes = hxs.select(base_path)

        name_path = 'h2/a[@rel="bookmark"]/text()'
        image_path = '(//div[@class="entry"]/p/a[@title]/img/@src)[1]'
        description_path = 'div[@class="entry"]/text()'
        ingredients_path = 'div[@class="entry"]/p'
        datePublished = 'div[@class="date"]/text()'

        recipes = []

        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())

            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', response.url)
            il.add_value('description', ''.join(r_scope.select(description_path).extract()).strip())

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


class SmittenkitchencrawlSpider(CrawlSpider, SmittenkitchenMixin):

    name = "smittenkitchen.com"

    allowed_domains = ["smittenkitchen.com"]

    start_urls = [
        "http://smittenkitchen.com/recipes/",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/blog/\d+/\d+/.+/')),
             callback='parse_item'),
    )

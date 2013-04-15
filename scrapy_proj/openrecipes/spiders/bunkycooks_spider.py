from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader
import re


class BunkycooksMixin(object):
    source = 'bunkycooks'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = '//div[@id="content"]'

        recipes_scopes = hxs.select(base_path)

        name_path = './/span[@class="item"]/h2[@class="fn"]/text()'
        image_path = "descendant-or-self::img[@class and contains(concat(' ', normalize-space(@class), ' '), ' size-full ')][1]/@src"
        prepTime_path = './/span[@class="preptime"]/text()'
        cookTime_path = './/span[@class="cooktime"]/text()'
        recipeYield_path = './/span[@class="yield"]/text()'
        ingredients_path = './/div[@class="ingredient"]/p/text()'

        recipes = []

        label_regex = re.compile(r'^For ')

        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', response.url)

            il.add_value('prepTime', r_scope.select(prepTime_path).extract())
            il.add_value('cookTime', r_scope.select(cookTime_path).extract())
            il.add_value('recipeYield', r_scope.select(recipeYield_path).extract())

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                ingredient = i_scope.extract().strip()
                if not label_regex.match(ingredient) and not ingredient.endswith(':'):
                    ingredients.append(ingredient)
            il.add_value('ingredients', ingredients)

            recipes.append(il.load_item())

        return recipes


class BunkycookscrawlSpider(CrawlSpider, BunkycooksMixin):

    name = "bunkycooks.com"

    allowed_domains = ["www.bunkycooks.com"]

    start_urls = [
        'http://www.bunkycooks.com/category/recipes/appetizers/',
        'http://www.bunkycooks.com/category/recipes/baked-goods/',
        'http://www.bunkycooks.com/category/recipes/beverages/',
        'http://www.bunkycooks.com/category/recipes/condiments/',
        'http://www.bunkycooks.com/category/recipes/desserts/',
        'http://www.bunkycooks.com/category/recipes/main-dishes/',
        'http://www.bunkycooks.com/category/recipes/side-dishes/',
        'http://www.bunkycooks.com/category/recipes/soups-and-salads/',
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/category/recipes/.*/page/\d/'))),

        Rule(SgmlLinkExtractor(allow=('/\d\d\d\d/\d\d/.*')),
             callback='parse_item'),
    )

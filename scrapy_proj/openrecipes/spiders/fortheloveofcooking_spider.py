from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader
import re


class FortheloveofcookingMixin(object):
    source = 'fortheloveofcooking'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = '//*[@class="recipe hrecipe"]'

        recipes_scopes = hxs.select(base_path)

        name_path = './/*[@class="fn"]/text()'
        #desription is pretty odd on this site.
        #description_path = 'TODO'
        image_path = '//div/p[1]//img/@src'
        prepTime_path = '//*[@class="preptime"]/text()'
        cookTime_path = '//*[@class="cooktime"]/text()'
        recipeYield_path = '//*[@class="yield"]/text()'
        ingredients_path = './/div[@class="ingredient"]/p/text()'

        recipes = []

        label_regex = re.compile(r'^For ')

        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', response.url)
            #il.add_value('description', r_scope.select(description_path).extract())

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


class FortheloveofcookingcrawlSpider(CrawlSpider, FortheloveofcookingMixin):

    name = "fortheloveofcooking.net"

    allowed_domains = ["www.fortheloveofcooking.net"]

    start_urls = [
        "http://www.fortheloveofcooking.net/recipes",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/category/[0-9a-zA-Z\_-]+'))),

        Rule(SgmlLinkExtractor(allow=('\/\d\d\d\d\/\d\d\/[a-zA-Z_.]+')),
             callback='parse_item'),
    )

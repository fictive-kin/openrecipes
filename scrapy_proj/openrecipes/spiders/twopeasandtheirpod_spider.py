from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader
import re


class TwopeasandtheirpodMixin(object):
    source = 'twopeasandtheirpod'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = '//*[@class="recipe hrecipe"]'

        recipes_scopes = hxs.select(base_path)

        name_path = '//*[@class="fn"]/text()'
        description_path = '//*[@class="summary"]/p/text()'
        image_path = '//p[1]/span/img/@src'
        prepTime_path = '//*[@class="preptime"]/text()'
        cookTime_path = './/*[@class="cooktime"]/text()'
        recipeYield_path = '//*[@class="yield"]/text()'
        ingredients_path = './/*[@class="ingredient"]/p/text()'
        #same formatting as forthelovecooking, so kind of odd.
        #datePublished = 'TODO'

        recipes = []

        label_regex = re.compile(r'^For ')

        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', response.url)
            il.add_value('description', r_scope.select(description_path).extract())

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

            #il.add_value('datePublished', r_scope.select(datePublished).extract())

            recipes.append(il.load_item())

        return recipes


class TwopeasandtheirpodcrawlSpider(CrawlSpider, TwopeasandtheirpodMixin):

    name = "twopeasandtheirpod.com"

    allowed_domains = ["www.twopeasandtheirpod.com"]

    start_urls = [
        "http://www.twopeasandtheirpod.com/recipes/",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/category/recipes/[a-zA-Z-/]+'))),

        Rule(SgmlLinkExtractor(allow=('\/[a-zA-Z-/]+')),
             callback='parse_item'),
    )

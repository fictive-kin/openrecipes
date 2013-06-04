from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader
import re


class MybakingaddictionMixin(object):
    source = 'mybakingaddiction'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = '//*[@class="hrecipe"]'

        recipes_scopes = hxs.select(base_path)

        name_path = '//h1[@class="fn"]/text()'
        #long descriptions used in website, also the description doesn't appear..
        description_path = '//*[@class="format_text entry-content jpibfi_container"]/p/text()'
        #the end image url contains dimensions 150x150, not sure how to remove.
        image_path = '//*[@class="photo"]/@src'
        #prepTime_path = 'TODO'   None given
        #cookTime_path = 'TODO'   None given
        #recipeYield_path = 'TODO'None given
        ingredients_path = './/*[@class="ingredient"]/p/text()'
        datePublished = '//span[@class="published"]/text()'

        recipes = []

        label_regex = re.compile(r'^For ')

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
                ingredient = i_scope.extract().strip()
                if not label_regex.match(ingredient) and not ingredient.endswith(':'):
                    ingredients.append(ingredient)
            il.add_value('ingredients', ingredients)

            il.add_value('datePublished', r_scope.select(datePublished).extract())

            recipes.append(il.load_item())

        return recipes


class MybakingaddictioncrawlSpider(CrawlSpider, MybakingaddictionMixin):

    name = "mybakingaddiction.com"

    allowed_domains = ["www.mybakingaddiction.com"]

    start_urls = [
        "http://www.mybakingaddiction.com/recipe-index/"

    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/.+/')),
             callback='parse_item'),
    )

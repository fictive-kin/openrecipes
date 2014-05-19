from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class SimplyrecipesMixin(object):
    source = 'simplyrecipes'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = '//*[@itemtype="http://schema.org/Recipe"]'

        recipes_scopes = hxs.select(base_path)

        name_path = '//*[@class="recipe-callout"]/h2/text()'
        description_path = './/*[@id="recipe-intronote"]/p/text()'
        image_path = '//*[@itemprop="image"]/@src'
        prepTime_path = './/span[@itemprop="prepTime"]/span/@title'
        cookTime_path = './/span[@itemprop="cookTime"]/span/@title'
        recipeYield_path = '//*[@itemprop="recipeYield"]/text()'
        ingredients_path = '//*[@itemprop="ingredients"]/text()'
        datePublished = '//*[@class="entry-date"]/text()'
        recipes = []

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

            ingredients = []
            ingredient_scopes = r_scope.select(ingredients_path)
            for ingredient_scope in ingredient_scopes:
                ingredient = ingredient_scope.extract().strip()
                if (ingredient):
                    ingredients.append(ingredient)
            il.add_value('ingredients', ingredients)

            il.add_value('datePublished', r_scope.select(datePublished).extract())

            recipes.append(il.load_item())

        return recipes


class SimplyrecipescrawlSpider(CrawlSpider, SimplyrecipesMixin):

    name = "simplyrecipes.com"

    allowed_domains = ["simplyrecipes.com"]

    start_urls = [
        "http://www.simplyrecipes.com/index/",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/recipes/ingredient/[a-z-]+/'))),

        Rule(SgmlLinkExtractor(allow=('/recipes/[a-z_]+/')),
             callback='parse_item'),
    )

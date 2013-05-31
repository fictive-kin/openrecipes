from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


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
        ingredients_path = 'normalize-space(//*[@class="ingredient"])'
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
                ingredient = i_scope.extract('p/br').strip()
                ingredients.append(ingredient)
            il.add_value('ingredients', ingredients)

            il.add_value('datePublished', r_scope.select(datePublished).extract())

            recipes.append(il.load_item())

        return recipes


class MybakingaddictioncrawlSpider(CrawlSpider, MybakingaddictionMixin):

    name = "www.mybakingaddiction.com"

    allowed_domains = ["www.mybakingaddiction.com"]

    start_urls = [
        "http://www.mybakingaddiction.com/appetizers/",
        "http://www.mybakingaddiction.com/bar-cookies/",
        "http://www.mybakingaddiction.com/baking-in-jars/",
        "http://www.mybakingaddiction.com/beverages/",
        "http://www.mybakingaddiction.com/bread/",
        "http://www.mybakingaddiction.com/breakfast/",
        "http://www.mybakingaddiction.com/brownies/",
        "http://www.mybakingaddiction.com/bundt-cakes/",
        "http://www.mybakingaddiction.com/cakes/",
        "http://www.mybakingaddiction.com/cheesecakes/",
        "http://www.mybakingaddiction.com/chocolate/",
        "http://www.mybakingaddiction.com/chocolate-chip/",
        "http://www.mybakingaddiction.com/cookies/",
        "http://www.mybakingaddiction.com/cupcakes/",
        "http://www.mybakingaddiction.com/entrees/",
        "http://www.mybakingaddiction.com/fall/",
        "http://www.mybakingaddiction.com/frozen-desserts/",
        "http://www.mybakingaddiction.com/ice-cream/",
        "http://www.mybakingaddiction.com/lemon-recipes/",
        "http://www.mybakingaddiction.com/mini_desserts/",
        "http://www.mybakingaddiction.com/muffins/",
        "http://www.mybakingaddiction.com/no-bake-desserts/",
        "http://www.mybakingaddiction.com/peanut-butter/",
        "http://www.mybakingaddiction.com/pies/",
        "http://www.mybakingaddiction.com/pumpkin/",
        "http://www.mybakingaddiction.com/strawberry-desserts/",
        "http://www.mybakingaddiction.com/summer/",
        "http://www.mybakingaddiction.com/trifles/"


    ]

    rules = (
        #Rule(SgmlLinkExtractor(allow=('/.+/'))),

        Rule(SgmlLinkExtractor(allow=('/.+/')),
             callback='parse_item'),
    )

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class ThelittlekitchenMixin(object):
    source = 'thelittlekitchen'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = '//div[@class="innerrecipe"]'

        recipes_scopes = hxs.select(base_path)

        name_path = '*//h2[@class="fn"]/text()'
        image_path = '*//img[@class="photo"]/@src'
        prepTime_path = '*//span[@class="preptime"]/text()'
        cookTime_path = '*//span[@class="cooktime"]/text()'
        totalTime_path = '*//span[@class="duration"]/text()'
        recipeYield_path = '*//span[@class="yield"]/text()'
        datePublished = '//div[@class="post fullpost singlepost"]//div[@class="postmeta"]/text()[normalize-space()]'
        ingredients_path = '*//*[@class="ingredient"]/p'

        recipes = []

        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', response.url)

            il.add_value('prepTime', r_scope.select(prepTime_path).extract())
            il.add_value('cookTime', r_scope.select(cookTime_path).extract())
            il.add_value('totalTime', r_scope.select(totalTime_path).extract())
            il.add_value('recipeYield', r_scope.select(recipeYield_path).extract())

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                ingredient = i_scope.select('text()').extract()
                ingredient = "".join(ingredient)
                ingredients.append(ingredient)
            il.add_value('ingredients', ingredients)

            il.add_value('datePublished', r_scope.select(datePublished).extract())

            recipes.append(il.load_item())

        return recipes


class ThelittlekitchencrawlSpider(CrawlSpider, ThelittlekitchenMixin):

    name = "thelittlekitchen.net"

    allowed_domains = ["www.thelittlekitchen.net"]

    start_urls = [
        "http://www.thelittlekitchen.net/category/recipes/",
    ]

    rules = (
        # The start url directly links to all of the recipes on the site
        #Rule(SgmlLinkExtractor(allow=(''))),

        Rule(SgmlLinkExtractor(allow=('/\d{4}/\d{2}/\d{2}/.+')),
             callback='parse_item'),
    )



from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class LovefoodMixin(object):
    source = 'lovefood'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = '//article[@itemtype="http://data-vocabulary.org/Recipe"]'

        recipes_scopes = hxs.select(base_path)

        name_path = '//h1[@itemprop="name"]/text()'
        description_path = '//meta[@name="description"]/@content'
        image_path = '//img[@itemprop="photo"]/@src'
        prepTime_path = '//span[@itemprop="prepTime"]/text()'
        cookTime_path = '//span[@itemprop="cookTime"]/text()'
        recipeYield_path = '//span[@itemprop="yield"]/text()'
        ingredients_path = '//li[@itemprop="ingredient"]'
        ingredients_amounts_path = './span[@itemprop="amount"]/span/text()'
        ingredients_names_path = './span[@itemprop="name"]/text()'

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

            # then combine them into a string.
            ingredient_scopes = r_scope.select(ingredients_path)
            amount = ingredient_scopes.select(ingredients_amounts_path).extract()
            name = ingredient_scopes.select(ingredients_names_path).extract()
            ingredients = [" ".join(ing).encode('utf-8') for ing in zip(amount, name)]
            il.add_value('ingredients', ingredients)

            recipes.append(il.load_item())

        return recipes


class LovefoodcrawlSpider(CrawlSpider, LovefoodMixin):

    name = "lovefood.com"

    allowed_domains = ["www.lovefood.com"]

    start_urls = [
        "http://www.lovefood.com/guide/recipes?page=1",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/guide/recipes\?page=(\d+)'))),

        Rule(SgmlLinkExtractor(allow=('/guide/recipes/(.+)')),
             callback='parse_item'),
    )

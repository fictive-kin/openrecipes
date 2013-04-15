from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader

class BBCfoodMixin(object):
    # this is the source string we'll store in the DB to aggregate stuff
    # from a single source
    source = 'bbcfood'

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        base_path = """//div[@id="blq-main"]"""

        recipes_scopes = hxs.select(base_path)

        name_path = '//h1/text()'
        description_path = '//div[@id="description"]//span[@class="summary"]/text()'
        image_path = '//img[@id="food-image"]/@src'
        prepTime_path = '//span[@class="prepTime"]/span[@class="value-title"]/@title'
        cookTime_path = '//span[@class="cookTime"]/span[@class="value-title"]/@title'
        recipeYield_path = '//h3[@class="yield"]/text()'
        ingredients_path = '//p[@class="ingredient"]'

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

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                amount = i_scope.select('text()[1]').extract()
                name = i_scope.select('a/text()').extract()
                amount = "".join(amount).strip()
                name = "".join(name).strip()
                ingredients.append("%s %s" % (amount, name))
            il.add_value('ingredients', ingredients)

            recipes.append(il.load_item())

        return recipes


class BBCfoodcrawlSpider(CrawlSpider, BBCfoodMixin):
    name = "bbcfood"
    allowed_domains = ["bbc.co.uk"]
    start_urls = [
        "http://www.bbc.co.uk/food/chefs",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/food/chefs/.+'))),

        Rule(SgmlLinkExtractor(allow=('food/recipes/(?!search).+')),
             callback='parse_item'),
    )

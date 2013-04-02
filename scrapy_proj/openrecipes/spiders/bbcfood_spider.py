from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem

class BBCfoodMixin(object):

    """
    Using this as a mixin lets us reuse the parse_item method more easily
    """

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        base_path = """//div[@id="blq-main"]"""

        recipes_scopes = hxs.select(base_path)

        name_path = '//h1/text()'
        description_path = '//div[@id="description"]/span[@class="summary"]/text()'
        image_path = '//img[@id="food-image"]/@src'
        prepTime_path = '//span[@class="prepTime"]/span[@class="value-title"]/@title'
        cookTime_path = '//span[@class="cookTime"]/span[@class="value-title"]/@title'
        recipeYield_path = '//h3[@class="yield"]/text()'
        ingredients_path = '//p[@class="ingredient"]'
        url_path = '//body/@id'

        recipes = []

        for r_scope in recipes_scopes:
            item = RecipeItem()

            item['name'] = r_scope.select(name_path).extract()
            item['image'] = r_scope.select(image_path).extract()
            item['description'] = r_scope.select(description_path).extract()
            item['prepTime'] = r_scope.select(prepTime_path).extract()
            item['cookTime'] = r_scope.select(cookTime_path).extract()
            item['recipeYield'] = r_scope.select(recipeYield_path).extract()

            # could not locate full url within the page
            item['url'] = 'http://www.bbc.co.uk/food/recipes/' + r_scope.select(url_path).extract()[0]

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                amount = i_scope.select('text()[1]').extract()
                name = i_scope.select('a/text()').extract()
                amount = "".join(amount).strip()
                name = "".join(name).strip()
                ingredients.append("%s %s" % (amount, name))
            item['ingredients'] = ingredients

            recipes.append(item)

        return recipes


class BBCfoodcrawlSpider(CrawlSpider, BBCfoodMixin):
    name = "bbcfood"
    allowed_domains = ["bbc.co.uk"]
    start_urls = [
        "http://www.bbc.co.uk/food/chefs",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/food/chefs/.+'))),

        Rule(SgmlLinkExtractor(allow=('food/recipes/.+')),
             callback='parse_item'),
    )

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class AspicyperspectivecrawlSpider(CrawlSpider):

    name = "aspicyperspective.com"
    allowed_domains = ["www.aspicyperspective.com"]
    start_urls = [
        "http://www.aspicyperspective.com/",
    ]

    # a tuple of Rules that are used to extract links from the HTML page
    rules = (
        Rule(SgmlLinkExtractor(allow=('/page/\d+'))),
        Rule(SgmlLinkExtractor(allow=('/\d\d\d\d/\d\d/.+\.html')), callback='parse_item'),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        base_path = """//div[@class="recipe hrecipe"]"""

        recipes_scopes = hxs.select(base_path)

        name_path = '//h2[@class="fn"]/text()'
        image_path = '//img[@class="photo"]/@src'
        prepTime_path = '//span[@class="preptime"]/text()'
        cookTime_path = '//span[@class="cooktime"]/text()'
        recipeYield_path = '//span[@class="yield"]/text()'
        ingredients_path = '//div[@class="ingredient"]/node()//text()'

        recipes = []
        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())
            il.add_value('source', 'aspicyperspective')
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
                if ingredient != '':
                    ingredients.append(ingredient.encode('utf-8'))

            il.add_value('ingredients', ingredients)

            recipes.append(il.load_item())

        return recipes

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem


class AspicyperspectivecrawlSpider(CrawlSpider):

    name = "www.aspicyperspective.com"
    allowed_domains = ["www.aspicyperspective.com"]
    start_urls = [
        "http://www.aspicyperspective.com/",
    ]

    # a tuple of Rules that are used to extract links from the HTML page
    rules = (
        Rule(SgmlLinkExtractor(allow=('/page/\d+'))),
        Rule(SgmlLinkExtractor(allow=('/\d\d\d\d/\d\d/.+\.html')),callback='parse_item'),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        base_path = """//div[@class="recipe hrecipe"]"""

        recipes_scopes = hxs.select(base_path)

        name_path = '//h2[@class="fn"]'
        image_path = '//img[@class="photo"]/@src'
        prepTime_path = '//span[@class="preptime"]'
        cookTime_path = '//span[@class="cooktime"]'
        recipeYield_path = '//span[@class="yield"]'
        ingredients_path = '//div[@class="ingredient"]/ul'

        recipes = []
        for r_scope in recipes_scopes:
            item = RecipeItem()
            item['name'] = r_scope.select(name_path).extract()
            item['image'] = r_scope.select(image_path).extract()
            item['url'] = response.url

            item['prepTime'] = r_scope.select(prepTime_path).extract()
            item['cookTime'] = r_scope.select(cookTime_path).extract()
            item['recipeYield'] = r_scope.select(recipeYield_path).extract()

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                ingredient_item = i_scope.select('li/text()').extract()
                ingredients.append("%s"  % ingredient_item)
            item['ingredients'] = ingredients

            recipes.append(item)

        return recipes

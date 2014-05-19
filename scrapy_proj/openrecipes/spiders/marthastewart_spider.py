from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class MarthastewartMixin(object):
    source = 'marthastewart'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = '//*[@class="hrecipe"]'

        recipes_scopes = hxs.select(base_path)

        name_path = '//*[@class="title fn"]/text()'
        description_path = '//*[@class="expand-body"]/text()'
        #formating odd, so much concatenate base url with image
        image_path = 'concat("http://www.marthastewart.com", //*[@class="img-l photo"]/@src)'
        prepTime_path = '//li[1]/span/span/@title'
        cookTime_path = '//li[2]/span/span/@title'
        recipeYield_path = '//*[@class="yield"]/text()[2]'
        ingredients_path = '//*[@class="ingredient"]/text()'
        datePublished = '//*[@class="recipe-info"]/cite/text()'

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
            ingredient_scopes = r_scope.select(ingredients_path)
            for ingredient_scope in ingredient_scopes:
                ingredient = ingredient_scope.extract().strip()
                if (ingredient):
                    ingredients.append(ingredient)
            il.add_value('ingredients', ingredients)

            il.add_value('datePublished', r_scope.select(datePublished).extract())

            recipes.append(il.load_item())

        return recipes


class MarthastewartcrawlSpider(CrawlSpider, MarthastewartMixin):

    name = "www.marthastewart.com"

    allowed_domains = ["www.marthastewart.com"]

    start_urls = [
        "http://www.marthastewart.com/search/apachesolr_search/recipe"

    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/search/apachesolr_search/recipe?page=\d+'))),

        Rule(SgmlLinkExtractor(allow=('/\d+/[a-z-]+')),
             callback='parse_item'),
    )

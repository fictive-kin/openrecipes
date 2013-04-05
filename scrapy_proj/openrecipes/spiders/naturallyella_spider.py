from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem


class NaturallyEllaMixin(object):

    source = 'naturallyella'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = """//div[@itemtype="http://schema.org/Recipe"]"""
        recipes_scope = hxs.select(base_path)

        description_path = '//meta[@property="og:description"]/@content'
        image_path = '//meta[@property="og:image"][1]/@content'
        name_path = '//meta[@property="og:title"]/@content'
        url_path = '//meta[@property="og:url"]/@content'

        date_published_path = '//div[@class="metabar-pad"]//time/@datetime'
        author_path = '//span[@itemprop="author"]/text()'

        ingredients_path = '//li[@itemprop="ingredients"]/text()'

        cook_time_path = './/time[@itemprop="cookTime"]//*[starts-with(@title, "PT")]/@title | .//time[@itemprop="cookTime"]/@datetime'
        prep_time_path = './/time[@itemprop="prepTime"]//*[starts-with(@title, "PT")]/@title | .//time[@itemprop="prepTime"]/@datetime'
        category_path = '//span[@itemprop="recipeCategory"]/text()'
        yield_path = '//span[@itemprop="recipeYield"]/text()'
        total_time_path = './/time[@itemprop="totalTime"]//*[starts-with(@title, "PT")]/@title | .//time[@itemprop="totalTime"]/@datetime'

        recipes = []
        for recipe_scope in recipes_scope:

            item = RecipeItem()
            item['source'] = self.source

            item['description'] = recipe_scope.select(description_path).extract()
            item['image'] = recipe_scope.select(image_path).extract()
            item['name'] = recipe_scope.select(name_path).extract()
            item['url'] = recipe_scope.select(url_path).extract()

            item['datePublished'] = recipe_scope.select(date_published_path).extract()
            item['creator'] = recipe_scope.select(author_path).extract()

            ingredients = []
            ingredient_scopes = recipe_scope.select(ingredients_path)
            for ingredient_scope in ingredient_scopes:
                ingredient = ingredient_scope.extract().strip()
                if (ingredient):
                    ingredients.append(ingredient)
            item['ingredients'] = ingredients

            item['cookTime'] = recipe_scope.select(cook_time_path).extract()
            item['prepTime'] = recipe_scope.select(prep_time_path).extract()
            item['recipeCategory'] = recipe_scope.select(category_path).extract()
            item['recipeYield'] = recipe_scope.select(yield_path).extract()
            item['totalTime'] = recipe_scope.select(total_time_path).extract()

            recipes.append(item)

        return recipes


class NaturallyEllaCrawlSpider(CrawlSpider, NaturallyEllaMixin):

    name = "naturallyella.com"

    allowed_domains = ["naturallyella.com"]

    start_urls = [
        "http://naturallyella.com/recipes/appetizers/",
        "http://naturallyella.com/recipes/breads/",
        "http://naturallyella.com/recipes/breakfast/",
        "http://naturallyella.com/recipes/cookies-and-bars/",
        "http://naturallyella.com/recipes/desserts/",
        "http://naturallyella.com/recipes/odds-and-ends/",
        "http://naturallyella.com/recipes/salads/",
        "http://naturallyella.com/recipes/soup/",
        "http://naturallyella.com/recipes/vegetarian-main-courses/",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/\d{4}/\d{2}/\d{2}/[a-z-]+/')),
             callback='parse_item'),
    )

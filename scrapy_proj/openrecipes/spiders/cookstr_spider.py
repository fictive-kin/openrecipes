from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class CookstrMixin(object):
    source = 'cookstr'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = '//*[@itemtype="http://schema.org/Recipe"]'

        recipes_scopes = hxs.select(base_path)

        name_path = '//*[@class="recipe-title"]/text()'
        description_path = '//span[@class="recipe_structure_headnotes"]/p/text()'
        #formating odd for image, so must concatenate url to beginning of image path
        image_path = 'concat("http://www.cookstr.com", //*[@itemprop="image"]/@src)'
        prepTime_path = 'id("recipe_body")/div[4]/span/text()'
        #for some formatting, the info won't display.
        cookTime_path = 'id("recipe_body")/div[5]/span/text()'
        recipeYield_path = '//*[@itemprop="recipeYield"]/text()'
        ingredients_path = '//*[@itemprop="ingredients"]//text()'

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

            recipes.append(il.load_item())

        return recipes


class CookstrcrawlSpider(CrawlSpider, CookstrMixin):

    name = "www.cookstr.com"

    allowed_domains = ["www.cookstr.com"]

    start_urls = [
        #resulting url when hitting enter into search with nothing searching
        "http://www.cookstr.com/searches?,"
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/searches?page=\d+'))),

        Rule(SgmlLinkExtractor(allow=('/recipes/\[a-z-]+')),
             callback='parse_item'),
    )

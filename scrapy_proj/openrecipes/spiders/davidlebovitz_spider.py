from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class DavidlebovitzMixin(object):
    source = 'davidlebovitz'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = '//*[@class="post hrecipe"]'

        recipes_scopes = hxs.select(base_path)

        name_path = '//*[@class="title fn"]/text()'
        #  little iffy on how to do this one
        #description_path = 'TODO'
        image_path = '//*[@class="photo"]/@src'
        #  both cook and prep time not available
        #prepTime_path = 'TODO'
        #cookTime_path = 'TODO'
        #  check on diff sites
        recipeYield_path = '//blockquote/p[2]/text()'
        #ingredients_path = '//*[@class="ingredient_list"]'
        ingredients_path = '//ul[@class="ingredient_list"]/li/text()'
        datePublished = 'normalize-space(//*[@class="postmeta"]/text())'

        recipes = []

        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', response.url)
            #il.add_value('description', r_scope.select(description_path).extract())

            #il.add_value('prepTime', r_scope.select(prepTime_path).extract())
            #il.add_value('cookTime', r_scope.select(cookTime_path).extract())
            il.add_value('recipeYield', r_scope.select(recipeYield_path).extract())

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                pass
            il.add_value('ingredients', ingredients)

            il.add_value('datePublished', r_scope.select(datePublished).extract())

            recipes.append(il.load_item())

        return recipes


class DavidlebovitzcrawlSpider(CrawlSpider, DavidlebovitzMixin):

    name = "www.davidlebovitz.com"

    allowed_domains = ["www.davidlebovitz.com"]

    start_urls = [
        "http://www.davidlebovitz.com/category/recipes/"
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/[^/]+/?'))),

        Rule(SgmlLinkExtractor(allow=('\/\d\d\d\d\/\d\d\/[a-zA-Z_]+/?')),
             callback='parse_item'),
    )

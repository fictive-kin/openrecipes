from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class Loveandoliveoil_Mixin(object):
    source = 'loveandoliveoil'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = '//blockquote[@class="recipe hrecipe"]'

        recipes_scopes = hxs.select(base_path)

        name_path = '//*[@class="fn"]/text()'
        description_path = '//*[@class="summary"]/p/text()'
        image_path = '//img[@class="photo"]/@src'
        prepTime_path = '//*[@class="preptime"]/text()'
        cookTime_path = '//*[@class="cooktime"]/text()'
        recipeYield_path = '//*[@class="yield"]/text()'
        ingredients_path = '//*[@class="ingredient"]/p/text()'

        recipes = []

        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', response.url)
            il.add_value('description',
                         r_scope.select(description_path).extract())

            il.add_value('prepTime', r_scope.select(prepTime_path).extract())
            il.add_value('cookTime', r_scope.select(cookTime_path).extract())
            il.add_value('recipeYield',
                         r_scope.select(recipeYield_path).extract())

            il.add_value('ingredients',
                         r_scope.select(ingredients_path).extract())

            recipes.append(il.load_item())

        return recipes


class Loveandoliveoil_crawlSpider(CrawlSpider, Loveandoliveoil_Mixin):

    name = "loveandoliveoil.com"

    allowed_domains = ["www.loveandoliveoil.com"]

    start_urls = ["http://www.loveandoliveoil.com/recipe-index", ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/tag/.+'))),

        Rule(SgmlLinkExtractor(allow=('/\d{4}/\d{2}/.+\.html')),
             callback='parse_item'),
    )

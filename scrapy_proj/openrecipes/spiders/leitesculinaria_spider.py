from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class LeitesculinariaMixin(object):

    source = 'leitesculinaria'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = '//*[@id="content"]'

        recipes_scopes = hxs.select(base_path)

        name_path = '//*[@class="entry-title"]/text()'
        image_path = '//*[@itemprop="image"]/@src'
        prepTime_path = '//*[@itemprop="prepTime"]/@content'
        recipeYield_path = '//*[@itemprop="recipeYield"]/text()'
        ingredients_path = '//*[@itemprop="ingredients"]'
        datePublished = '//*[@class="date published time"]/text()'

        recipes = []

        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', response.url)

            il.add_value('prepTime', r_scope.select(prepTime_path).extract())
            il.add_value('recipeYield', r_scope.select(recipeYield_path).extract())

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                amount = i_scope.select('*[@class="ingredient-n"]/text()').extract()
                unit = i_scope.select('*[@class="ingredient-unit"]/text()').extract()
                name = i_scope.select('*[@class="ingredient-name"]/text()').extract()
                amount = "".join(amount).strip()
                unit = "".join(unit).strip()
                name = "".join(name).strip()
                ingredients.append("%s %s %s" % (amount, unit, name))
            il.add_value('ingredients', ingredients)

            il.add_value('datePublished', r_scope.select(datePublished).extract())

            recipes.append(il.load_item())

        return recipes


class LeitesculinariacrawlSpider(CrawlSpider, LeitesculinariaMixin):

    name = "leitesculinaria.com"

    allowed_domains = ["leitesculinaria.com"]

    start_urls = [
        "http://leitesculinaria.com/category/recipes",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/category/recipes/page/\d+'))),

        Rule(SgmlLinkExtractor(allow=('/\d+/\[a-z]+.html')),
             callback='parse_item'),
    )

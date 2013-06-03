from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class Spider_nameMixin(object):
    source = 'spider_name'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = 'TODO'

        recipes_scopes = hxs.select(base_path)

        name_path = 'TODO'
        description_path = 'TODO'
        image_path = 'TODO'
        prepTime_path = 'TODO'
        cookTime_path = 'TODO'
        recipeYield_path = 'TODO'
        ingredients_path = 'TODO'
        datePublished = 'TODO'

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
                pass
            il.add_value('ingredients', ingredients)

            il.add_value('datePublished', r_scope.select(datePublished).extract())

            recipes.append(il.load_item())

        return recipes


class Spider_namecrawlSpider(CrawlSpider, Spider_nameMixin):

    name = "START_URL"

    allowed_domains = ["START_URL"]

    start_urls = [
        "START_URL",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('TODO'))),

        Rule(SgmlLinkExtractor(allow=('TODO')),
             callback='parse_item'),
    )

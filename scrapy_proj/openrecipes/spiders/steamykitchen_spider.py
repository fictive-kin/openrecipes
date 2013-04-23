from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class SteamykitchenMixin(object):

    """
    Using this as a mixin lets us reuse the parse_item method more easily
    """

    source = 'steamykitchen'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)
        base_path = """//blockquote[@class="recipe"]"""
        recipes_scopes = hxs.select(base_path)

        name_path = '//meta[@property="og:title"]/@content'
        url_path = '//meta[@property="og:url"]/@content'
        description_path = '//meta[@property="og:description"]/@content'
        image_path = '//meta[@property="og:image"][1]/@content'
        prepTime_path = '*//*[@itemprop="prepTime"]/@content'
        cookTime_path = '*//*[@itemprop="cookTime"]/@content'
        recipeYield_path = '*//*[@itemprop="recipeYield"]/text()'
        ingredients_path = '*//*[@itemprop="ingredients"]'
        datePublished = '//p[@class="date"]/text()'

        recipes = []

        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', r_scope.select(url_path).extract())
            il.add_value('description', r_scope.select(description_path).extract())
            il.add_value('prepTime', r_scope.select(prepTime_path).extract())
            il.add_value('cookTime', r_scope.select(cookTime_path).extract())
            il.add_value('recipeYield', r_scope.select(recipeYield_path).extract())

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                ind = i_scope.extract()
                ind = ind.strip()
                ingredients.append("%s " % (ind))
            il.add_value('ingredients', ingredients)

            il.add_value('datePublished', r_scope.select(datePublished).extract())

            recipes.append(il.load_item())

        return recipes


class SteamykitchenSpider(CrawlSpider, SteamykitchenMixin):

    name = "steamykitchen.com"
    allowed_domains = ["steamykitchen.com"]
    start_urls = [
        "http://www.steamykitchen.com/recipes",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/category/recipes/[0-9a-zA-Z\_-]+'))),

        Rule(SgmlLinkExtractor(allow=('[0-9a-zA-Z\._-]+')),
             callback='parse_item'),
    )

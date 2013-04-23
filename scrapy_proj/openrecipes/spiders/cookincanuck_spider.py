from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class CookincanuckMixin(object):

    """
    Using this as a mixin lets us reuse the parse_item method more easily
    """

    source = 'cookincanuck'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)
        base_path = """//div[@id="zlrecipe-innerdiv"]"""
        recipes_scopes = hxs.select(base_path)

        name_path = '*//*[@itemprop="name"]/text()'
        url_path = '//link[@rel="canonical"]/@href'
        image_path = '//meta[@property="og:image"][1]/@content'

        prepTime_path = '*//*[@itemprop="prepTime"]/@content'
        cookTime_path = '*//*[@itemprop="cookTime"]/@content'
        recipeYield_path = '*//*[@itemprop="recipeYield"]/text()'

        ingredients_path = '*//*[@itemprop="ingredients"]'
        datePublished = '//*[@class="time_stamp_month"]'

        recipes = []

        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', r_scope.select(url_path).extract())

            il.add_value('prepTime', r_scope.select(prepTime_path).extract())
            il.add_value('cookTime', r_scope.select(cookTime_path).extract())
            il.add_value('recipeYield', r_scope.select(recipeYield_path).extract())

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                ind = i_scope.select('.//text()').extract()
                ingredients.append(''.join(ind).strip())
            il.add_value('ingredients', ingredients)

            il.add_value('datePublished', r_scope.select(datePublished).extract())

            recipes.append(il.load_item())

        return recipes


class CookincanuckcrawlSpider(CrawlSpider, CookincanuckMixin):

    name = "cookincanuck.com"

    allowed_domains = ["cookincanuck.com"]

    start_urls = [
        "http://www.cookincanuck.com/recipes/",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/category/[^/]+/?'))),

        Rule(SgmlLinkExtractor(allow=('\/\d\d\d\d\/\d\d\/[a-zA-Z_]+/?')),
             callback='parse_item'),
    )

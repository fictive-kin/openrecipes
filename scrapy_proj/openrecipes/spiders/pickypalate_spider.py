from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class PickypalateMixin(object):

    """
    Using this as a mixin lets us reuse the parse_item method more easily
    """

    source = 'pickypalate'

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        # site has many recipes missing the semantmic markup, but not worth
        # pursuing those IMHO. use hrecipe
        base_path = """//*[@class="hrecipe"]"""

        recipes_scopes = hxs.select(base_path)

        name_path = './/*[@class="fn"]/text()'
        url_path = '//meta[@property="og:url"]/@content'
        image_path = '//meta[@property="og:image"][1]/@content'
        recipeYield_path = './/*[@class="yield"]/text()'
        ingredients_path = '*//*[@class="ingredient"]'

        # get the date from rest of page, not under hrecipe
        datePublished_path = '//*[@class="date"][1]'

        recipes = []

        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', r_scope.select(url_path).extract())

            il.add_value('recipeYield', r_scope.select(recipeYield_path).extract())

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                amount = i_scope.select('*[@class="amount"]/text()').extract()
                name = i_scope.select('*[@class="name"]/text()').extract()
                amount = "".join(amount).strip()
                name = "".join(name).strip()
                ingredients.append("%s %s" % (amount, name))
            il.add_value('ingredients', ingredients)

            il.add_value('datePublished', r_scope.select(datePublished_path).extract())

            recipes.append(il.load_item())

        return recipes


class PickypalateSpider(CrawlSpider, PickypalateMixin):
    name = "picky-palate.com"
    allowed_domains = ["picky-palate.com"]

    start_urls = [
        "http://picky-palate.com/recipe-index/",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/category/\d+/'))),

        Rule(SgmlLinkExtractor(allow=('\/\d\d\d\d\/\d\d\/\d\d\/[a-zA-Z_]+/?')),
             callback='parse_item'),
    )

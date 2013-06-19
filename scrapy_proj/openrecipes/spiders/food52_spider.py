from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class Food52Mixin(object):
    source = 'food52'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = '//*[@itemtype="http://schema.org/Recipe"]'

        recipes_scopes = hxs.select(base_path)

        name_path = '//*[@itemprop="name"]/text()'
        #may be too useless
        description_path = '//*[@class="recipe-note"]/text()'
        image_path = '//figure[@class="photo-frame first"]/img/@src'
        recipeYield_path = '//*[@itemprop="recipeYield"]/strong/em/text()'
        ingredients_path = '*//*[@itemprop="ingredients"]'

        recipes = []

        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', response.url)
            il.add_value('description', r_scope.select(description_path).extract())

            il.add_value('recipeYield', r_scope.select(recipeYield_path).extract())

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                amount = i_scope.select('*[@class="quantity"]/text()').extract()
                name = i_scope.select('*[@class="item-name"]/text()').extract()
                amount = "".join(amount).strip()
                name = "".join(name).strip()
                ingredients.append("%s %s" % (amount, name))
            il.add_value('ingredients', ingredients)

            recipes.append(il.load_item())

        return recipes


class Food52crawlSpider(CrawlSpider, Food52Mixin):

    name = "food52.com"

    allowed_domains = ["food52.com"]

    start_urls = [
        "http://food52.com/recipes/search?cat=popular",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/recipes/search?cat=popular&page=\d+'))),
        #may want to double check this last reg exp.
        Rule(SgmlLinkExtractor(allow=('/recipes/\d+-[a-z]+')),
             callback='parse_item'),
    )

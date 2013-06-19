from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class SippitysupMixin(object):
    source = 'sippitysup'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = '//*[@itemtype="http://data-vocabulary.org/Recipe"]'

        recipes_scopes = hxs.select(base_path)

        name_path = '//*[@class="recipe-title"]/a/text()'
        description_path = '//*[@class="recipe-description"]/text()'
        image_path = '//*[@itemprop="photo"]/@src'
        recipeYield_path = '//*[@itemprop="yield"]/text()'
        ingredients_path = '//*[@itemprop="ingredient"]'
        datePublished = '//*[@itemprop="published"]/text()'

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
                amount = i_scope.select('//*[@itemprop="amount"]/text()').extract()
                name = i_scope.select('//*[@itemprop="name"]/text()').extract()
                amount = "".join(amount).strip()
                name = "".join(name).strip()
                ingredients.append("%s %s" % (amount, name))
            il.add_value('ingredients', ingredients)

            il.add_value('datePublished', r_scope.select(datePublished).extract())

            recipes.append(il.load_item())

        return recipes


class SippitysupcrawlSpider(CrawlSpider, SippitysupMixin):

    name = "sippitysup.com"

    allowed_domains = ["sippitysup.com"]

    start_urls = [
        "sippitysup.com",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/recipe/page/\d+/'))),

        Rule(SgmlLinkExtractor(allow=('/recipe\/[a-z]+/')),
             callback='parse_item'),
    )
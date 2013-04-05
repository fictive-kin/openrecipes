from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem


class ChezUsMixin(object):
    # this is the source string we'll store in the DB to aggregate stuff
    # from a single source
    source = 'chezus'

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        base_path = """//td[@id="content"]"""

        recipes_scopes = hxs.select(base_path)

        name_path = '//*[@itemprop="name"]/text()'
        description_path = '//*[@data-role="content"]/p/text()'
        ingredients_path = '//*[@itemprop="ingredients"]/text()'

        recipes = []

        for r_scope in recipes_scopes:
            item = RecipeItem()

            item['source'] = self.source

            item['name'] = r_scope.select(name_path).extract()
            name = item['name'][0]

            image_path = '//img[contains(@alt, "' + name + '")]/@src'
            item['image'] = r_scope.select(image_path).extract()

            item['url'] = response.url
            item['description'] = r_scope.select(description_path).extract()

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = [i.strip() for i in ingredient_scopes.extract()]
            item['ingredients'] = ingredients

            recipes.append(item)

        return recipes


class ChezuscrawlSpider(CrawlSpider, ChezUsMixin):
    name = "chezus"
    allowed_domains = ["chezus.com"]
    start_urls = [
        "http://chezus.com/",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/page/\d.+/'))),

        Rule(SgmlLinkExtractor(allow=('/\d\d\d\d/\d\d/\d\d/.*/')),
             callback='parse_item'),
    )

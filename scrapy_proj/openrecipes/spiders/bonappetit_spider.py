from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem


class BonappetitMixin(object):

    # this is the source string we'll store in the DB to aggregate stuff
    # from a single source
    source = 'bonappetit'

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        base_path = """//*[contains(@class,'hrecipe')]"""

        recipes_scopes = hxs.select(base_path)

        name_path = '//meta[@property="og:title"]/@content'
        description_path = '//meta[@name="description"]/@content'
        url_path = '//meta[@property="og:url"]/@content'
        image_path = '//meta[@property="og:image"]/@content'
        recipeYield_path = '//div[@class="time-and-yield"]/*/span[@class="yield"]/text()'
        ingredients_path = '//ul[@class="ingredients"]/li/span[@class="ingredient"]'
        datePublished_path = '//div[@class="intro"]/div[@class="display-date"]/text()[last()]' # skip HTML comment

        recipes = []
        for r_scope in recipes_scopes:
            item = RecipeItem()

            item['source'] = self.source
            item['name'] = r_scope.select(name_path).extract()
            item['image'] = r_scope.select(image_path).extract()
            item['url'] = r_scope.select(url_path).extract()
            item['description'] = r_scope.select(description_path).extract()
            item['recipeYield'] = r_scope.select(recipeYield_path).extract()

            ingredients_scope = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredients_scope:
                quantity = i_scope.select('span[@class="quantity"]/text()').extract()
                name = i_scope.select('span[@class="name"]/text()').extract()
                quantity = "".join(quantity).strip()
                name = "".join(name).strip()
                ingredients.append("%s %s" % (quantity, name))
            item['ingredients'] = ingredients

            item['datePublished'] = r_scope.select(datePublished_path).extract()

            recipes.append(item)

        return recipes


class BonappetitcrawlSpider(CrawlSpider, BonappetitMixin):
    name = "bonappetit.com"
    allowed_domains = ["bonappetit.com"]
    start_urls = [
        # all of the recipes are linked from this page
        "http://www.bonappetit.com/services/sitemap/recipes",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('services/sitemap/recipes?page=\d+'))),

        Rule(SgmlLinkExtractor(allow=('recipes/\d{4}/\d{2}/.+')),
             callback='parse_item'),
    )

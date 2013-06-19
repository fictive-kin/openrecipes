from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class NorecipesMixin(object):
    source = 'norecipes'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = '//*[@id="recipress_recipe" ]'

        recipes_scopes = hxs.select(base_path)

        name_path = '//*[@class="fn" ]/text()'
        description_path = '//*[@class="summary" ]/text()'
        image_path = '//*[@class="format_text entry-content"]/p/img/@src'
        recipeYield_path = '//*[@class="yield"]/text()'
        ingredients_path = '//ul/li[@class="ingredient"]'
        datePublished = '//*[@class="published"]/text()'

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
                amount = i_scope.select('//*[@class="amount"]/text()').extract()
                name = i_scope.select('//*[@class="name"]/a/text()').extract()
                amount = "".join(amount).strip()
                name = "".join(name).strip()
                ingredients.append("%s %s" % (amount, name))
            il.add_value('ingredients', ingredients)

            il.add_value('datePublished', r_scope.select(datePublished).extract())

            recipes.append(il.load_item())

        return recipes


class NorecipescrawlSpider(CrawlSpider, NorecipesMixin):

    name = "norecipes.com"

    allowed_domains = ["norecipes.com"]

    start_urls = [
        "http://norecipes.com/recipe/#sthash.6lk3YFJ8.ZTaVerMz.dpbs",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/blog/recipe/type\/[a-zA-z]+/'))),

        Rule(SgmlLinkExtractor(allow=('/blog\/[a-z]+/')),
             callback='parse_item'),
    )
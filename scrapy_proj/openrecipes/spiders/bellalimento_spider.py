from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem


class BellalimentocrawlSpider(CrawlSpider):

    name = "www.bellalimento.com"
    allowed_domains = ["www.bellalimento.com"]
    start_urls = [
        "http://www.bellalimento.com/",
    ]

    # a tuple of Rules that are used to extract links from the HTML page
    rules = (
        Rule(SgmlLinkExtractor(allow=('/category/.+'))),
        Rule(SgmlLinkExtractor(allow=('/\d\d\d\d/\d\d/\d\d/')),callback='parse_item'),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        base_path = """//div[@id="zlrecipe-container"]"""

        recipes_scopes = hxs.select(base_path)

        name_path = '//div[@id="zlrecipe-title"]/text()'
        ingredients_path = '//ul[@id="zlrecipe-ingredients-list"]/li[@class="ingredient"]'

        recipes = []
        for r_scope in recipes_scopes:
            item = RecipeItem()
            item['name'] = r_scope.select(name_path).extract()
            name = item['name']
            image_path = '//img[contains(@title, "' + name[0] + '")]/@src'
            item['image'] = r_scope.select(image_path).extract()[0]
            item['url'] = response.url

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                ingredient_item = i_scope.select('text()').extract()
                ingredients.append("%s"  % ingredient_item)
            item['ingredients'] = ingredients

            recipes.append(item)

        return recipes

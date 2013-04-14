from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem


class PickypalateMixin(object):

    """
    Using this as a mixin lets us reuse the parse_item method more easily
    """

    source = 'pickypalate'

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        base_path = """//*[@id="content"]/div/div[4]"""

        recipes_scopes = hxs.select(base_path)

        name_path = '//*[@id="content"]/div/div[4]/div[1]/h2/span/text()'
        url_path = '//meta[@property="og:url"]/@content'
        image_path = '//meta[@property="og:image"][1]/@content'
        recipeYield_path = '//*[@id="content"]/div/div[4]/div[2]/div/p[3]/span/text()'
        ingredients_path = '*//*[@class="ingredient"]'

        monthPublished = '//*[@id="content"]/div/div[1]/div/text()[1]'
        dayPublished = '//*[@id="content"]/div/div[1]/div/div/text()'
        yearPublished = '//*[@id="content"]/div/div[1]/div/text()[2]'

        recipes = []

        for r_scope in recipes_scopes:
            item = RecipeItem()

            item['source'] = self.source

            item['name'] = r_scope.select(name_path).extract()
            item['image'] = r_scope.select(image_path).extract()
            item['url'] = r_scope.select(url_path).extract()

            item['recipeYield'] = r_scope.select(recipeYield_path).extract()

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                amount = i_scope.select('*[@class="amount"]/text()').extract()
                name = i_scope.select('*[@class="name"]/text()').extract()
                amount = "".join(amount).strip()
                name = "".join(name).strip()
                ingredients.append("%s %s" % (amount, name))
            item['ingredients'] = ingredients

            month = r_scope.select(monthPublished).extract()
            month_stripped = month[0].strip()
            day = r_scope.select(dayPublished).extract()
            day_stripped = day[0].strip()
            year = r_scope.select(yearPublished).extract()
            year_stripped = year[0].strip()

            item['datePublished'] = month_stripped + ' ' + day_stripped + ', ' + year_stripped

            recipes.append(item)

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

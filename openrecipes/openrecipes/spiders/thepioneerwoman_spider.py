# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem


class ThepioneerwomancrawlSpider(CrawlSpider):
    name = "thepioneerwoman.com"
    allowed_domains = ["thepioneerwoman.com"]
    start_urls = [
        "http://thepioneerwoman.com/cooking/category/all-pw-recipes/?posts_per_page=60",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/cooking/category/all-pw-recipes/page/\d+/'))),
        Rule(SgmlLinkExtractor(allow=('cooking\/\d\d\d\d\/\d\d\/[a-zA-Z_]+')),
             callback='parse_item'),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        base_path = """//div[@itemtype="http://data-vocabulary.org/Recipe"]"""

        recipes_scopes = hxs.select(base_path)

        name_path = '//meta[@property="og:title"]/@content'
        description_path = '//meta[@property="og:description"]/@content'
        url_path = '//meta[@property="og:url"]/@content'
        image_path = '//meta[@property="og:image"][1]/@content'
        prepTime_path = '*//*[@itemprop="prepTime"]/@datetime'
        cookTime_path = '*//*[@itemprop="cookTime"]/@datetime'
        recipeYield_path = '*//*[@itemprop="yield"]/text()'
        ingredients_path = '*//*[@itemprop="ingredient"]'
        datePublished = '*/*[@itemprop="published"]/@datetime'

        recipes = []
        for r_scope in recipes_scopes:
            item = RecipeItem()
            item['name'] = r_scope.select(name_path).extract()
            item['image'] = r_scope.select(image_path).extract()
            item['url'] = r_scope.select(url_path).extract()
            item['description'] = r_scope.select(description_path).extract()

            item['prepTime'] = r_scope.select(prepTime_path).extract()
            item['cookTime'] = r_scope.select(cookTime_path).extract()
            item['recipeYield'] = r_scope.select(recipeYield_path).extract()

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                amount = i_scope.select('*[@itemprop="amount"]/text()').extract()
                name = i_scope.select('*[@itemprop="name"]/text()').extract()
                amount = "".join(amount).strip()
                name = "".join(name).strip()
                ingredients.append("%s %s" % (amount, name))
            item['ingredients'] = ingredients

            item['datePublished'] = r_scope.select(datePublished).extract()

            recipes.append(item)

        return recipes

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem


# TODO: fix http://www.elanaspantry.com/squash-aduki-chestnut-soup/

class ElanaspantryMixin(object):
    source = 'elanaspantry'

    def parse_item(self, response):
        if '/ingredients/' in response.url or '/category/' in response.url:
            return []

        hxs = HtmlXPathSelector(response)

        base_path = '//div[@class="blog"]'

        recipes_scopes = hxs.select(base_path)

        name_path = 'h1/a[@rel="bookmark"]/text()'
        description_path = '//meta[@property="og:description"]/@content'
        image_path = '//meta[@property="og:image"][1]/@content'
        recipeYield_path = './/*[@class="yield"]//text()[normalize-space()]'
        ingredients_path = './/*[@class="ingredient"]'
        datePublished = '//div[@class="blurb"]/strong/text()[1]'

        recipes = []

        for r_scope in recipes_scopes:
            item = RecipeItem()

            item['source'] = self.source

            item['name'] = r_scope.select(name_path).extract()
            item['image'] = r_scope.select(image_path).extract()
            item['url'] = response.url
            item['description'] = r_scope.select(description_path).extract()

            item['recipeYield'] = ' '.join(r_scope.select(recipeYield_path).extract())

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for ingredient_node in ingredient_scopes:
                ingredient = [i.strip() for i in ingredient_node.select('.//text()[normalize-space()]').extract()]
                ingredients.append(' '.join(ingredient))

            item['ingredients'] = ingredients

            datePublished = r_scope.select(datePublished).extract()[0]
            item['datePublished'] = datePublished.replace('Posted on', '').replace('in', '').strip()

            recipes.append(item)

        return recipes


class ElanaspantrycrawlSpider(CrawlSpider, ElanaspantryMixin):

    name = "elanaspantry.com"

    allowed_domains = ["www.elanaspantry.com"]

    start_urls = [
        "http://www.elanaspantry.com/gluten-free-recipes/",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/gluten-free-recipes/.+/'))),

        Rule(SgmlLinkExtractor(allow=('/[^/]+/')),
             callback='parse_item'),
    )

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem


class TheVintageMixerMixin(object):
   
    source = 'thevintagemixer'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = '//div[@itemtype="http://schema.org/Recipe"]'
        recipes_scope = hxs.select(base_path)

        ingredients_path = '//li[@itemprop="ingredients"]/text()';

        image_path = '(//div[@class="entry"]//img/@src)[1]'
        name_path = '//div[@itemprop="name"]/text()'
        url_path = '//h2[@class="title"]/a/@href'

        yield_path = '//span[@itemprop="servingSize"]/text()'
        total_time_path = '//span[@itemprop="totalTime"]/@content'

        recipes = []
        for recipe_scope in recipes_scope:

            item = RecipeItem()
            item['source'] = self.source

            item['image'] = recipe_scope.select(image_path).extract()
            item['name'] = recipe_scope.select(name_path).extract()
            item['url'] = recipe_scope.select(url_path).extract()

            ingredients = []
            ingredient_scopes = recipe_scope.select(ingredients_path)
            for ingredient_scope in ingredient_scopes:
                ingredient = ingredient_scope.extract().strip()
                if (ingredient):
                    ingredients.append(ingredient) 
            item['ingredients'] = ingredients

            item['recipeYield'] = recipe_scope.select(yield_path).extract()
            item['totalTime'] = recipe_scope.select(total_time_path).extract()

            recipes.append(item)

        return recipes

class TheVintageMixerCrawlSpider(CrawlSpider, TheVintageMixerMixin):

    name = "thevintagemixer.com"

    allowed_domains = ["thevintagemixer.com"]

    start_urls = [
        "http://www.thevintagemixer.com/category/vintage-mixer/recipes/",
    ]

    rules = (
        
        Rule(SgmlLinkExtractor(allow=('/category/vintage-mixer/recipes/page/\d+/'))),

        Rule(SgmlLinkExtractor(allow=('/\d{4}/\d{2}//[a-z-]+/')), callback='parse_item'),
    )
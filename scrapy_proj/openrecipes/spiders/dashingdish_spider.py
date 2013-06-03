from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class Dashingdish_spiderMixin(object):
    source = 'dashingdish_spider'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = '//*[@id="recipe"]'

        recipes_scopes = hxs.select(base_path)

        name_path = '//*[@class="row page_title clearfix"]/h2/text()'
        description_path = '//*[@class="entry"]/p//text()'
        image_path = '//*[@class="featured_image"]/img[@class="image"]/@src'
        recipeYield_path = '//*[@class="breakdown"]/tbody/tr[1]/td[1]/text()'
        ingredients_path = '*//*[@class="ingredients"]'
        #the site only offers total time, so prep and cook is combined
        #prepTime_path = ''
        # timezone warning, that is over my head at this point
        #cookTime_path = '//*[@class="cook_time"]'
        # datePublished = 'TODO' not available

        recipes = []

        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())

            #il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', response.url)
            il.add_value('description', r_scope.select(description_path).extract())

            # il.add_value('prepTime', r_scope.select(prepTime_path).extract())
            #il.add_value('cookTime', r_scope.select(cookTime_path).extract())
            il.add_value('recipeYield', r_scope.select(recipeYield_path).extract())
            #il.add_value('ingredients', r_scope.select(ingredients_path).extract())
            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                amount = i_scope.select('//td/strong').extract()
                name = i_scope.select('//*[@class="ingredients"]/tbody/tr/td/text()').extract()
                amount = "".join(amount).strip()
                name = "".join(name).strip()
                ingredients.append("%s %s" % (amount, name))
            il.add_value('ingredients', ingredients)
            # il.add_value('datePublished', r_scope.select(datePublished).extract())

            recipes.append(il.load_item())

        return recipes


class Dashingdish_spidercrawlSpider(CrawlSpider, Dashingdish_spiderMixin):

    name = "dashingdish.com"

    allowed_domains = ["dashingdish.com"]

    start_urls = [
        "http://dashingdish.com/recipes/",
    ]

    rules = (
        #Rule(SgmlLinkExtractor(allow=('TODO'))),

        Rule(SgmlLinkExtractor(allow=('recipe\/.+\/')),
             callback='parse_item'),
    )

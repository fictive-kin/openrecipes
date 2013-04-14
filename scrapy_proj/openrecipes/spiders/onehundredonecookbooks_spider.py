from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class OnehundredonecookbooksMixin(object):

    # this is the source string we'll store in the DB to aggregate stuff
    # from a single source
    source = '101cookbooks'

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        base_path = """//div[@id="recipe"]"""

        recipes_scopes = hxs.select(base_path)

        name_path = 'h1/text()'
        description_path = '//meta[@property="og:description"]/@content'
        url_path = '//meta[@property="og:url"]/@content'
        image_path = '//meta[@property="og:image"][1]/@content'
        prepTime_path = './/span[@class="preptime"]/span[@class="value-title"]/@title'
        cookTime_path = './/span[@class="cooktime"]/span[@class="value-title"]/@title'

        # super inconsistent in how the yield is formatted
        recipeYield_path = "|".join([
                                    '//div[@id="recipe"]/p[starts-with(i,"Makes")]/i',
                                    '//div[@id="recipe"]/p[starts-with(i,"Serves")]/i',
                                    '//div[@id="recipe"]/p[starts-with(em,"Makes")]/em',
                                    '//div[@id="recipe"]/p[starts-with(em,"Serves")]/em',
                                    '//div[@id="recipe"][starts-with(p,"Makes")]/p',
                                    '//div[@id="recipe"][starts-with(p,"Serves")]/p',
                                    ])
        ingredients_path = 'blockquote/*'
        datePublished = '//span[@class="published"]/span[@class="value-title"]/@title'

        recipes = []
        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())
            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', r_scope.select(url_path).extract())
            il.add_value('description', r_scope.select(description_path).extract())

            il.add_value('prepTime', r_scope.select(prepTime_path).extract())
            il.add_value('cookTime', r_scope.select(cookTime_path).extract())
            il.add_value('recipeYield', r_scope.select(recipeYield_path).extract())

            il.add_value('ingredients', r_scope.select(ingredients_path).extract())

            il.add_value('datePublished', r_scope.select(datePublished).extract())

            recipes.append(il.load_item())

        return recipes


class OnehundredonecookbookscrawlSpider(CrawlSpider, OnehundredonecookbooksMixin):
    name = "101cookbooks.com"
    allowed_domains = ["101cookbooks.com"]
    start_urls = [
        # all of the recipes are linked from this page
        "http://www.101cookbooks.com/archives.html",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('archives/.+\.html')),
             callback='parse_item'),
    )

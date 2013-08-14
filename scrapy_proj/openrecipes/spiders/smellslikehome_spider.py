from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class SmellslikehomeMixin(object):
    source = 'smellslikehome'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        # Older recipe posts have a different, much looser format
        base_path = '//div[@itemtype="http://schema.org/Recipe"] | //div[@class="post-content"]'

        recipes_scopes = hxs.select(base_path)

        name_path = '//div[@itemprop="name"]/text() | //p/span/strong/text()'
        description_path = '//meta[@name="description"]/@content'
        image_path = '//img[1]/@src'
        prepTime_path = '//span[@itemprop="prepTime"][contains(@datetime, "PT")]/text()'
        cookTime_path = '//span[@itemprop="cookTime"][contains(@datetime, "PT")]/text()'
        totalTime_path = '//span[@itemprop="totalTime"][contains(@content, "PT")]/text()'
        recipeYield_path = '//span[@itemprop="recipeYield"]/text()'
        ingredients_path = '//li[@itemprop="ingredients"]/text() | //ul/li/text()'
        datePublished = '//div[contains(concat(" ", @class, " "), " post-date ")]/text()'

        recipes = []

        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', response.url)
            il.add_value('description', r_scope.select(description_path).extract())

            il.add_value('prepTime', r_scope.select(prepTime_path).extract())
            il.add_value('cookTime', r_scope.select(cookTime_path).extract())
            il.add_value('totalTime', r_scope.select(totalTime_path).extract())
            il.add_value('recipeYield', r_scope.select(recipeYield_path).extract())

            il.add_value('ingredients', r_scope.select(ingredients_path).extract())

            il.add_value('datePublished', r_scope.select(datePublished).extract())

            recipes.append(il.load_item())

        return recipes


class SmellslikehomecrawlSpider(CrawlSpider, SmellslikehomeMixin):

    name = "smellslikehome.com"

    allowed_domains = ["www.smells-like-home.com"]

    start_urls = [
        "http://www.smells-like-home.com/full-archives/",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/20[01][0-9]/'))),
        #Rule(SgmlLinkExtractor(allow=('/2007/'))),
        #Rule(SgmlLinkExtractor(allow=('/2008/'))),
        #Rule(SgmlLinkExtractor(allow=('/2009/'))),
        #Rule(SgmlLinkExtractor(allow=('/2010/'))),
        #Rule(SgmlLinkExtractor(allow=('/2011/'))),
        #Rule(SgmlLinkExtractor(allow=('/2012/'))),
        #Rule(SgmlLinkExtractor(allow=('/2013/'))),

        Rule(SgmlLinkExtractor(allow=('/\d{4}/\d{2}/.+')),
             callback='parse_item'),
    )

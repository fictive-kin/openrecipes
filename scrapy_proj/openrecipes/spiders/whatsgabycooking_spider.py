from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader
from openrecipes.schema_org_parser import parse_recipes
from openrecipes.util import is_ingredient_container


class WhatsgabycookingMixin(object):
    source = 'whatsgabycooking'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)
        image_path = hxs.select("descendant-or-self::img[@class and contains(@class, 'wp-image')][1]/@data-lazy-src").extract()

        raw_recipes = parse_recipes(hxs, {'source': self.source, 'url': response.url})
        if raw_recipes:
            # schema.org.  Yay!
            for recipe in raw_recipes:
                recipe['image'] = image_path

            return [RecipeItem.from_dict(recipe) for recipe in raw_recipes]
        else:
            # not schema.org.  Boo!
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)
            il.add_value('url', response.url)
            il.add_value('image', image_path)

            name_path = '//*[@class="post-title"]/h1/text()'
            il.add_value('name', hxs.select(name_path).extract())
            # maybe it's in the P's
            for p in hxs.select('//div[@id="recipe" or @class="span9"]/p'):
                if is_ingredient_container(p):
                    il.add_value('ingredients', p.select('text()').extract())
            # or maybe it's in the LI's
            for li in hxs.select('//*[@class="span9"]//ul/li'):
                if is_ingredient_container(li):
                    il.add_value('ingredients', li.select('text()').extract())
            # or maybe it's in these other LI's
            for li in hxs.select('//li[@class="ingredient"]/text()'):
                il.add_value('ingredients', li.extract())
            return il.load_item()


class WhatsgabycookingcrawlSpider(CrawlSpider, WhatsgabycookingMixin):

    name = "whatsgabycooking.com"

    allowed_domains = ["whatsgabycooking.com"]

    start_urls = [
        "http://whatsgabycooking.com/index/",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/category/categories/.*/'))),

        Rule(SgmlLinkExtractor(allow=('/[^/]+/'), deny=('/category/categories/.*/')),
             callback='parse_item'),
    )

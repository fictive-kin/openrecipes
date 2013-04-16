from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem
from openrecipes.schema_org_parser import parse_recipes



class WhatsgabycookingMixin(object):
    source = 'whatsgabycooking'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)
        raw_recipes = parse_recipes(hxs, {'source': self.source, 'url': response.url})

        image_path = hxs.select("descendant-or-self::img[@class and contains(@class, 'wp-image')][1]/@src").extract()


        for recipe in raw_recipes :
            recipe['image'] = image_path
            
        return [RecipeItem.from_dict(recipe) for recipe in raw_recipes]

      
            


class WhatsgabycookingcrawlSpider(CrawlSpider, WhatsgabycookingMixin):

    name = "whatsgabycooking.com"

    allowed_domains = ["whatsgabycooking.com"]

    start_urls = [
        "http://whatsgabycooking.com/index/",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('TODO'))),

        Rule(SgmlLinkExtractor(allow=('TODO')),
             callback='parse_item'),
    )



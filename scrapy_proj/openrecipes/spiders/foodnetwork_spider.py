from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader
from openrecipes.schema_org_parser import parse_recipes
from openrecipes.util import flatten


class FoodnetworkMixin(object):
    source = 'foodnetwork'

    def parse_item(self, response):
        # skip review pages, which are hard to distinguish from recipe pages
        # in the link extractor regex
        if '/reviews/' in response.url:
            return []

        hxs = HtmlXPathSelector(response)
        raw_recipes = parse_recipes(hxs, {'source': self.source, 'url': response.url})
        for recipe in raw_recipes:
            if 'photo' in recipe:
                recipe['photo'] = flatten(recipe['photo'])
                recipe['photo'] = recipe['photo'].replace('_med.', '_lg.')
            if 'image' in recipe:
                recipe['image'] = flatten(recipe['image'])
                recipe['image'] = recipe['image'].replace('_med.', '_lg.')

        return [RecipeItem.from_dict(recipe) for recipe in raw_recipes]


class FoodnetworkcrawlSpider(CrawlSpider, FoodnetworkMixin):

    name = "foodnetwork.com"

    allowed_domains = ["www.foodnetwork.com"]

    start_urls = [
        "http://www.foodnetwork.com/search/delegate.do?fnSearchString=&fnSearchType=Recipe",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/search/delegate.do?Ntk=site_search&Nr=Record%20Type:Result&N=501&No=\d+'))),

        Rule(SgmlLinkExtractor(allow=('/recipes/.+')),
             callback='parse_item'),
    )

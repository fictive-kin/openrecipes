from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader
from openrecipes.hrecipe_parser import parse_recipe
from openrecipes.util import select_class


class PaninihappyMixin(object):
    source = 'paninihappy'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)
        data = {'url': response.url, 'source': self.source}
        recipe = RecipeItem.from_dict(parse_recipe(hxs, data))
        loader = RecipeItemLoader(item=recipe)
        loader.add_value('image', select_class(hxs, 'post_image').select('@src').extract())
        loader.add_value('description', hxs.select('//meta[@name="description"]/@content').extract())
        loader.add_value('name', select_class(hxs, 'entry-title').select('text()').extract())
        return [loader.load_item()]


class PaninihappycrawlSpider(CrawlSpider, PaninihappyMixin):

    name = "paninihappy.com"

    allowed_domains = ["paninihappy.com"]

    start_urls = [
        'http://paninihappy.com/category/recipes/beef-panini-recipes/',
        'http://paninihappy.com/category/recipes/breakfast-panini-recipes/',
        'http://paninihappy.com/category/recipes/chicken-panini-recipes/',
        'http://paninihappy.com/category/recipes/dessert-panini-recipes/',
        'http://paninihappy.com/category/recipes/leftovers-recipes/',
        'http://paninihappy.com/category/recipes/pork-panini-recipes/',
        'http://paninihappy.com/category/recipes/seafood-panini-recipes/',
        'http://paninihappy.com/category/recipes/turkey-panini-recipes/',
        'http://paninihappy.com/category/recipes/vegetarian-panini-recipes/',
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/recipes/.*/page/\d+/'))),

        Rule(SgmlLinkExtractor(allow=('/.*/'), deny=('/category/recipes/.*')),
             callback='parse_item'),
    )

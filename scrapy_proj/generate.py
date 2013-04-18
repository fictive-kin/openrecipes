import argparse
from urlparse import urlparse
import os
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))

SpiderTemplate = """from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class %(crawler_name)sMixin(object):
    source = '%(source)s'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = 'TODO'

        recipes_scopes = hxs.select(base_path)

        name_path = 'TODO'
        description_path = 'TODO'
        image_path = 'TODO'
        prepTime_path = 'TODO'
        cookTime_path = 'TODO'
        recipeYield_path = 'TODO'
        ingredients_path = 'TODO'
        datePublished = 'TODO'

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
            il.add_value('recipeYield', r_scope.select(recipeYield_path).extract())

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                pass
            il.add_value('ingredients', ingredients)

            il.add_value('datePublished', r_scope.select(datePublished).extract())

            recipes.append(il.load_item())

        return recipes


class %(crawler_name)scrawlSpider(CrawlSpider, %(crawler_name)sMixin):

    name = "%(domain)s"

    allowed_domains = ["%(domain)s"]

    start_urls = [
        "%(start_url)s",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('TODO'))),

        Rule(SgmlLinkExtractor(allow=('TODO')),
             callback='parse_item'),
    )
"""

FeedSpiderTemplate = """from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import XmlXPathSelector
from openrecipes.spiders.%(source)s_spider import %(crawler_name)sMixin


class %(crawler_name)sfeedSpider(BaseSpider, %(crawler_name)sMixin):
    name = "%(name)s.feed"
    allowed_domains = [
        "%(feed_domains)s",
        "feeds.feedburner.com",
        "feedproxy.google.com",
    ]
    start_urls = [
        "%(feed_url)s",
    ]

    def parse(self, response):
        xxs = XmlXPathSelector(response)
        links = xxs.select("TODO").extract()

        return [Request(x, callback=self.parse_item) for x in links]
"""


def parse_url(url):
    if url.startswith('http://') or url.startswith('https://'):
        return urlparse(url)
    else:
        return urlparse('http://' + url)


def generate_crawlers(args):
    parsed_url = parse_url(args.start_url)

    domain = parsed_url.netloc
    name = args.name.lower()

    values = {
        'crawler_name': name.capitalize(),
        'source': name,
        'name': domain,
        'domain': domain,
        'start_url': args.start_url,
    }

    spider_filename = os.path.join(script_dir, 'openrecipes', 'spiders', '%s_spider.py' % name)
    with open(spider_filename, 'w') as f:
        f.write(SpiderTemplate % values)

    if args.with_feed:
        feed_url = args.with_feed[0]
        feed_domain = parse_url(feed_url).netloc
        values['feed_url'] = feed_url
        values['name'] = name
        if feed_domain == domain:
            values['feed_domains'] = domain
        else:
            values['feed_domains'] = '%s",\n        "%s' % (domain, feed_domain)
        feed_filename = os.path.join(script_dir, 'openrecipes', 'spiders', '%s_feedspider.py' % name)
        with open(feed_filename, 'w') as f:
            f.write(FeedSpiderTemplate % values)


epilog = """
Example usage: python generate.py epicurious http://www.epicurious.com/
"""
parser = argparse.ArgumentParser(description='Generate a scrapy spider', epilog=epilog)
parser.add_argument('name', help='Spider name.  This will be used to generate the filename')
parser.add_argument('start_url', help='Start URL for crawling')
parser.add_argument('--with-feed', required=False, nargs=1, metavar='feed-url', help='RSS Feed URL')

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
else:
    args = parser.parse_args()
    generate_crawlers(args)

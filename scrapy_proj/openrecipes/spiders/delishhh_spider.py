from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader
import re


class DelishhhMixin(object):

    """
    Using this as a mixin lets us reuse the parse_item method more easily
    """

    # this is the source string we'll store in the DB to aggregate stuff
    # from a single source
    source = 'delishhh'

    def parse_item(self, response):
        """
        this site is a mess, with LOTS of inconsistencies in formatting. We will
        try one other approach (in parse_item_alt1), but spending a bunch of
        time to get their old recipes seems like a waste.
        """

        # we use this to run XPath commands against the HTML in the response
        hxs = HtmlXPathSelector(response)

        # this is the base XPath string for the element that contains the recipe
        # info
        base_path = """//blockquote[@class="recipe hrecipe"]"""

        # the select() method will return a list of HtmlXPathSelector objects.
        # On this site we will almost certainly either get back just one, if
        # any exist on the page
        recipes_scopes = hxs.select(base_path)

        # if we don't find anything, try the alt parser
        if len(recipes_scopes) < 1:
            self.log('calling alternate delishhh.com scraper')
            return self.parse_item_alt1(response)

        name_path = '//meta[@property="og:title"]/@content'
        description_path = '//meta[@property="og:description"]/@content'
        url_path = '//meta[@property="og:url"]/@content'
        image_path = '//meta[@property="og:image"][1]/@content'
        prepTime_path = './/*[@class="preptime"]/text()'
        cookTime_path = './/*[@class="cooktime"]/text()'
        recipeYield_path = './/*[@class="yield"]/text()'
        ingredients_path = './/div[@class="ingredient"]/*'
        datePublished_path = '//meta[@property="article:published_time"]/@content'
        dateModified_path = '//meta[@property="article:modified_time"]/@content'
        # init an empty list
        recipes = []

        # loop through our recipe scopes and extract the recipe data from each
        for r_scope in recipes_scopes:
            # make an empty RecipeItem
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

            il.add_value('datePublished', r_scope.select(datePublished_path).extract())
            il.add_value('dateModified', r_scope.select(dateModified_path).extract())

            # stick this RecipeItem in the array of recipes we will return
            recipes.append(il.load_item())

        # more processing is done by the openrecipes.pipelines. Look at that
        # file to see transforms that are applied to each RecipeItem
        return recipes

    def parse_item_alt1(self, response):
        hxs = HtmlXPathSelector(response)
        base_path = """//blockquote"""
        recipes_scopes = hxs.select(base_path)

        # it's easier to define these XPath strings outside of the loop below
        name_path = '//meta[@property="og:title"]/@content'
        description_path = '//meta[@property="og:description"]/@content'
        url_path = '//meta[@property="og:url"]/@content'
        # just grab the first image we can find
        image_path = '//div[@class="post"]/p[1]/img/@src'
        ypc_path = './/p/text()[starts-with(.,"Yields")]'
        # ingredients always seems to follow the ypc block
        ingredients_path = './/p[starts-with(text(),"Yields")]/following-sibling::p[1]'
        datePublished_path = '//meta[@property="article:published_time"]/@content'
        dateModified_path = '//meta[@property="article:modified_time"]/@content'

        # init an empty list
        recipes = []

        # loop through our recipe scopes and extract the recipe data from each
        for r_scope in recipes_scopes:
            # make an empty RecipeItem
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', r_scope.select(url_path).extract())
            il.add_value('description', r_scope.select(description_path).extract())

            # might be able to make this bit more robust, which would probably
            # let us hit more recipes on this site. Not terribly motivated, tho
            ypc_str = "".join(r_scope.select(ypc_path).extract())
            yield_match = re.match(r'Yields?:?\s([^|]+)', ypc_str, re.I)
            prep_match = re.match(r'.+Prep(?: Time)?:?\s([^|]+)', ypc_str, re.I)
            cook_match = re.match(r'.+Cook Time:?\s([^|]+)', ypc_str, re.I)

            if yield_match:
                il.add_value('recipeYield', yield_match.group(1))
            if prep_match:
                il.add_value('prepTime', prep_match.group(1))
            if cook_match:
                il.add_value('cookTime', cook_match.group(1))

            il.add_value('ingredients', r_scope.select(ingredients_path).extract())

            il.add_value('datePublished', r_scope.select(datePublished_path).extract())
            il.add_value('dateModified', r_scope.select(dateModified_path).extract())

            # stick this RecipeItem in the array of recipes we will return
            recipes.append(il.load_item())

        # more processing is done by the openrecipes.pipelines. Look at that
        # file to see transforms that are applied to each RecipeItem
        return recipes


class DelishhhcrawlSpider(CrawlSpider, DelishhhMixin):

    # this is the name you'll use to run this spider from the CLI
    name = "delishhh.com"

    # URLs not under this set of domains will be ignored
    allowed_domains = ["delishhh.com"]

    # the set of URLs the crawler with start with. We're starting on the first
    # page of the site's recipe archive
    start_urls = [
        "http://delishhh.com/recipes/"
    ]

    # a tuple of Rules that are used to extract links from the HTML page
    rules = (
        # these two will just get crawled for links -- not scraped
        Rule(SgmlLinkExtractor(allow=('\d\d\d\d\/\d\d\/?$'))),
        Rule(SgmlLinkExtractor(allow=('\d\d\d\d\/\d\d\/page\/\d\/?$'))),

        # this rule is for recipe posts themselves. The callback argument will
        # process the HTML on the page, extract the recipe information, and
        # return a RecipeItem object
        Rule(SgmlLinkExtractor(allow=('\d\d\d\d\/\d\d\/\d\d\/(.+)\/?')),
             callback='parse_item'),
    )

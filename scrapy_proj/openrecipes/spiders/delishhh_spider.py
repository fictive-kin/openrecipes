from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem


class DelishhhMixin(object):

    """
    Using this as a mixin lets us reuse the parse_item method more easily
    """

    def parse_item(self, response):

        # we use this to run XPath commands against the HTML in the response
        hxs = HtmlXPathSelector(response)

        # this is the base XPath string for the element that contains the recipe
        # info
        base_path = """//blockquote[@class="recipe hrecipe"]"""

        # the select() method will return a list of HtmlXPathSelector objects.
        # On this site we will almost certainly either get back just one, if
        # any exist on the page
        recipes_scopes = hxs.select(base_path)

        # it's easier to define these XPath strings outside of the loop below
        name_path = 'h2/text()'
        description_path = '//meta[@property="og:description"]/@content'
        url_path = '//meta[@property="og:url"]/@content'
        image_path = '//meta[@property="og:image"][1]/@content'
        prepTime_path = '*//*[@class="preptime"]/text()'
        cookTime_path = '*//*[@class="cooktime"]/text()'
        recipeYield_path = '*//*[@class="yield"]/text()'
        ingredients_path = '*//*[@class="ingredient"]'
        datePublished = '//meta[@property="article:published_time"]/@content'

        # init an empty list
        recipes = []

        # loop through our recipe scopes and extract the recipe data from each
        for r_scope in recipes_scopes:
            # make an empty RecipeItem
            item = RecipeItem()
            item['name'] = r_scope.select(name_path).extract()
            item['image'] = r_scope.select(image_path).extract()
            item['url'] = r_scope.select(url_path).extract()
            item['description'] = r_scope.select(description_path).extract()

            item['prepTime'] = r_scope.select(prepTime_path).extract()
            item['cookTime'] = r_scope.select(cookTime_path).extract()
            item['recipeYield'] = r_scope.select(recipeYield_path).extract()

            item['ingredients'] = r_scope.select(ingredients_path).extract()

            item['datePublished'] = r_scope.select(datePublished).extract()

            # stick this RecipeItem in the array of recipes we will return
            recipes.append(item)

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
        "http://delishhh/2013",
        "http://delishhh/2012",
        "http://delishhh/2012/page/2",
        "http://delishhh/2011",
        "http://delishhh/2011/page/2",
        "http://delishhh/2011/page/3",
        "http://delishhh/2010",
        "http://delishhh/2010/page/2",
        "http://delishhh/2010/page/3",
        "http://delishhh/2010/page/4",
        "http://delishhh/2008",
    ]

    # a tuple of Rules that are used to extract links from the HTML page
    rules = (
        # this rule is for recipe posts themselves. The callback argument will
        # process the HTML on the page, extract the recipe information, and
        # return a RecipeItem object
        Rule(SgmlLinkExtractor(allow=('\d\d\d\d\/\d\d\/\d\d\/[a-zA-Z_]+')),
             callback='parse_item'),
    )

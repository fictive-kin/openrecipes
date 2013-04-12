from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem


class CookieandkateMixin(object):

    # this is the source string we'll store in the DB to aggregate stuff
    # from a single source
    source = 'cookieandkate'

    def parse_item(self, response):

        # we use this to run XPath commands against the HTML in the response
        hxs = HtmlXPathSelector(response)

        # this is the base XPath string for the element that contains the
        # recipe info
        base_path = """//div[@itemtype="http://schema.org/Recipe"]"""

        # the select() method will return a list of HtmlXPathSelector objects.
        # On this site we will almost certainly either get back just one, if
        # any exist on the page
        recipes_scopes = hxs.select(base_path)

        # it's easier to define these XPath strings outside of the loop below
        name_path = '//div[@itemprop="name"]/text()'
        alt_name_path = '//div[@itemprop="name"]/span/text()'
        description_path = '//div[@itemprop="description"]/text()'
        image_path = '//img[1]/@src'
        prepTime_path = '//time[@itemprop="prepTime"]/text()'
        cookTime_path = '//time[@itemprop="cookTime"]/text()'
        recipeYield_path = '//span[@itemprop="recipeYield"]/text()'
        ingredients_path = '//li[@itemprop="ingredients"]/text()'
        datePublished = '//abbr[@class="published"]/text()'

        # init an empty list
        recipes = []

        # loop through our recipe scopes and extract the recipe data from each
        for r_scope in recipes_scopes:
            # make an empty RecipeItem
            item = RecipeItem()

            item['source'] = self.source

            item['name'] = r_scope.select(name_path).extract()
            if not item['name']:
                item['name'] = r_scope.select(alt_name_path).extract()

            # There's a bunch of images for each recipe, so we just
            # grab the first.
            item['image'] = r_scope.select(image_path).extract()[1]
            item['url'] = response.url
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


class CookieandkateSpider(CrawlSpider, CookieandkateMixin):

    # this is the name you'll use to run this spider from the CLI
    name = "cookieandkate.com"

    # URLs not under this set of domains will be ignored
    allowed_domains = ["cookieandkate.com"]

    # the set of URLs the crawler with start with. We're starting on the first
    # page of the site's recipe archive
    start_urls = [
        "http://cookieandkate.com/recipes/",
    ]

    # a tuple of Rules that are used to extract links from the HTML page
    rules = (
        # this rule is for recipe posts themselves. The callback argument will
        # process the HTML on the page, extract the recipe information, and
        # return a RecipeItem object
        Rule(SgmlLinkExtractor(allow=('\d\d\d\d\/[a-zA-Z_]+')),
             callback='parse_item'),
    )

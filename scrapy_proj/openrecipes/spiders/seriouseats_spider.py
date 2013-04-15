from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class SeriouseatsMixin(object):

    """
    Using this as a mixin lets us reuse the parse_item method more easily
    """

    # this is the source string we'll store in the DB to aggregate stuff
    # from a single source
    source = 'seriouseats'

    def parse_item(self, response):

        # we use this to run XPath commands against the HTML in the response
        hxs = HtmlXPathSelector(response)

        # this is the base XPath string for the element that contains the recipe
        # info
        base_path = """//article[@class="hrecipe"]"""

        # the select() method will return a list of HtmlXPathSelector objects.
        # On this site we will almost certainly either get back just one, if
        # any exist on the page
        recipes_scopes = hxs.select(base_path)

        # it's easier to define these XPath strings outside of the loop below
        name_path = '//h1/text()'
        recipeYield_path = '//span[@class="info yield"]/text()'
        image_path = '//section[@class="content-unit"]/img/@src'
        prepTime_path = '//span[@class="info preptime"]/text()'
        cookTime_path = '//span[@class="info duration"]/text()'
        ingredients_path = '//div[@class="ingredients-section"]/ul/li/span/text()'
        datePublished = '//footer/time/text()'

        # init an empty list
        recipes = []

        # loop through our recipe scopes and extract the recipe data from each
        for r_scope in recipes_scopes:
            # make an empty RecipeItem
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', response.url)

            il.add_value('prepTime', r_scope.select(prepTime_path).extract())
            il.add_value('cookTime', r_scope.select(cookTime_path).extract())
            il.add_value('recipeYield', r_scope.select(recipeYield_path).extract())

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                ingredients.append(i_scope.extract())
            il.add_value('ingredients', ingredients)

            il.add_value('datePublished', r_scope.select(datePublished).extract())

            # stick this RecipeItem in the array of recipes we will return
            recipes.append(il.load_item())

        # more processing is done by the openrecipes.pipelines. Look at that
        # file to see transforms that are applied to each RecipeItem
        return recipes


class SeriouseatscrawlSpider(CrawlSpider, SeriouseatsMixin):

    # this is the name you'll use to run this spider from the CLI
    name = "seriouseats.com"

    # URLs not under this set of domains will be ignored
    allowed_domains = ["seriouseats.com"]

    # the set of URLs the crawler will start from
    start_urls = [
        "http://www.seriouseats.com/recipes/2013/03/24-week/",
    ]

    # a tuple of Rules that are used to extract links from the HTML page
    rules = (
        # this rule has no callback, so these links will be followed and mined
        # for more URLs. This lets us page through the recipe archives
        Rule(SgmlLinkExtractor(allow=('recipes\/\d\d\d\d\/\d\d\/\d\d\-week'))),

        # this rule is for recipe posts themselves. The callback argument will
        # process the HTML on the page, extract the recipe information, and
        # return a RecipeItem object
        # Added $ to prevent duplicates via referral arguments
        Rule(SgmlLinkExtractor(allow=('recipes\/\d\d\d\d\/\d\d\/.+.html$')),
             callback='parse_item'),
    )

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class ThepioneerwomanMixin(object):

    """
    Using this as a mixin lets us reuse the parse_item method more easily
    """

    # this is the source string we'll store in the DB to aggregate stuff
    # from a single source
    source = 'thepioneerwoman'

    def parse_item(self, response):

        # we use this to run XPath commands against the HTML in the response
        hxs = HtmlXPathSelector(response)

        # this is the base XPath string for the element that contains the recipe
        # info
        base_path = """//div[@itemtype="http://data-vocabulary.org/Recipe"]"""

        # the select() method will return a list of HtmlXPathSelector objects.
        # On this site we will almost certainly either get back just one, if
        # any exist on the page
        recipes_scopes = hxs.select(base_path)

        # it's easier to define these XPath strings outside of the loop below
        name_path = '//meta[@property="og:title"]/@content'
        description_path = '//meta[@property="og:description"]/@content'
        url_path = '//meta[@property="og:url"]/@content'
        image_path = '//meta[@property="og:image"][1]/@content'
        prepTime_path = '*//*[@itemprop="prepTime"]/@datetime'
        cookTime_path = '*//*[@itemprop="cookTime"]/@datetime'
        recipeYield_path = '*//*[@itemprop="yield"]/text()'
        ingredients_path = '*//*[@itemprop="ingredient"]'
        datePublished = '*/*[@itemprop="published"]/@datetime'

        # init an empty list
        recipes = []

        # loop through our recipe scopes and extract the recipe data from each
        for r_scope in recipes_scopes:
            # make an empty RecipeItemLoader
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', r_scope.select(url_path).extract())
            il.add_value('description', r_scope.select(description_path).extract())

            il.add_value('prepTime', r_scope.select(prepTime_path).extract())
            il.add_value('cookTime', r_scope.select(cookTime_path).extract())
            il.add_value('recipeYield', r_scope.select(recipeYield_path).extract())

            # ingredients require more work on this site to extract. We first
            # get the base elements, and then loop through to pull out each
            # "amount" and "name." Then we build a single string to represent
            # each one and append it to the array of ingredients
            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                amount = i_scope.select('*[@itemprop="amount"]/text()').extract()
                name = i_scope.select('*[@itemprop="name"]/text()').extract()
                amount = "".join(amount).strip()
                name = "".join(name).strip()
                ingredients.append("%s %s" % (amount, name))
            il.add_value('ingredients', ingredients)

            il.add_value('datePublished', r_scope.select(datePublished).extract())

            # il.load_item() returns a RecipeItem passed through the
            # RecipeItemLoader's property formatters. Apppend the RecipeItem
            # to the recipes list
            recipes.append(il.load_item())

        # more processing is done by the openrecipes.pipelines. Look at that
        # file to see transforms that are applied to each RecipeItem
        return recipes


class ThepioneerwomancrawlSpider(CrawlSpider, ThepioneerwomanMixin):

    # this is the name you'll use to run this spider from the CLI
    name = "thepioneerwoman.com"

    # URLs not under this set of domains will be ignored
    allowed_domains = ["thepioneerwoman.com"]

    # the set of URLs the crawler with start with. We're starting on the first
    # page of the site's recipe archive
    start_urls = [
        "http://thepioneerwoman.com/cooking/category/all-pw-recipes/?posts_per_page=60",
    ]

    # a tuple of Rules that are used to extract links from the HTML page
    rules = (
        # this rule has no callback, so these links will be followed and mined
        # for more URLs. This lets us page through the recipe archives
        Rule(SgmlLinkExtractor(allow=('/cooking/category/all-pw-recipes/page/\d+/'))),

        # this rule is for recipe posts themselves. The callback argument will
        # process the HTML on the page, extract the recipe information, and
        # return a RecipeItem object
        Rule(SgmlLinkExtractor(allow=('cooking\/\d\d\d\d\/\d\d\/[a-zA-Z_]+/?')),
             callback='parse_item'),
    )

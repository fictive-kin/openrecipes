from urlparse import urljoin
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem


class JamieoliverMixin(object):

    """
    Using this as a mixin lets us reuse the parse_item method more easily
    """

    # this is the source string we'll store in the DB to aggregate stuff
    # from a single source
    source = 'jamieoliver'

    def parse_item(self, response):

        # we use this to run XPath commands against the HTML in the response
        hxs = HtmlXPathSelector(response)

        # this is the base XPath string for the element that contains the recipe
        # info
        base_path = """//span[@class="hrecipe"]"""

        # the select() method will return a list of HtmlXPathSelector objects.
        # On this site we will almost certainly either get back just one, if
        # any exist on the page
        recipes_scopes = hxs.select(base_path)

        # it's easier to define these XPath strings outside of the loop below
        name_path = '//div[@class="content"]/header/h1[@class="fn"]/text()'
        description_path = '//article[@class="recipe_description"]//text()'
        image_path = '//div[@class="recipe_image_main"]/p/img/@src'
        recipeYield_path = '//div[@class="recipe_meta"]/p/span[contains(@class,"yield")]/text()'
        ingredients_path = '//article[@class="ingredients"]//ul//li/p[@class="ingredient"]/span[@class="value"]/text()'

        # init an empty list
        recipes = []

        # loop through our recipe scopes and extract the recipe data from each
        for r_scope in recipes_scopes:
            # make an empty RecipeItem
            item = RecipeItem()

            item['source'] = self.source

            item['name'] = r_scope.select(name_path).extract()
            item['image'] = urljoin(response.url, r_scope.select(image_path).extract().pop(0))
            item['url'] = response.url
            item['description'] = r_scope.select(description_path).extract()

            # prepTime not available
            item['prepTime'] = None
            # cookTime not available
            item['cookTime'] = None
            item['recipeYield'] = r_scope.select(recipeYield_path).extract()
            item['ingredients'] = r_scope.select(ingredients_path).extract()

            # datePublished not available
            item['datePublished'] = None

            # stick this RecipeItem in the array of recipes we will return
            recipes.append(item)

        # more processing is done by the openrecipes.pipelines. Look at that
        # file to see transforms that are applied to each RecipeItem
        return recipes


class JamieolivercrawlSpider(CrawlSpider, JamieoliverMixin):

    # this is the name you'll use to run this spider from the CLI
    name = "jamieoliver"

    # URLs not under this set of domains will be ignored
    allowed_domains = ["jamieoliver.com"]

    # the set of URLs the crawler with start with. We're starting on the first
    # page of the site's recipe archive
    start_urls = [
        "https://www.jamieoliver.com/recipes",
    ]

    # a tuple of Rules that are used to extract links from the HTML page
    rules = (
        # url format for a single recipe
        #     /recipes/{section}/{recipe-name}
        # url formats for recipes list
        #     /recipes/{section}
        #     /recipes/category/{category}
        #     /recipes/category/{category}/{sub-category}

        # this rule has no callback, so these links will be followed and mined
        # for more URLs. This lets us page through the recipe archives
        Rule(SgmlLinkExtractor(allow=(
            '/recipes/[a-zA-Z\-]+/',
            '/recipes/category/.*'
        ))),

        # this rule is for recipe posts themselves. The callback argument will
        # process the HTML on the page, extract the recipe information, and
        # return a RecipeItem object
        Rule(SgmlLinkExtractor(allow=('recipes\/[^(category)][a-zA-Z\-]+/[a-zA-Z\-]+')),
             callback='parse_item'),
    )

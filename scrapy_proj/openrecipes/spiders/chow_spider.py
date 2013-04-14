from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader
from openrecipes.util import parse_iso_date


class ChowMixin(object):

    """
    Using this as a mixin lets us reuse the parse_item method more easily
    """

    # this is the source string we'll store in the DB to aggregate stuff
    # from a single source
    source = 'chow'

    def parse_item(self, response):

        # we use this to run XPath commands against the HTML in the response
        hxs = HtmlXPathSelector(response)

        # this is the base XPath string for the element that contains the recipe
        # info
        base_path = """//body"""

        # the select() method will return a list of HtmlXPathSelector objects.
        # On this site we will almost certainly either get back just one, if
        # any exist on the page
        recipes_scopes = hxs.select(base_path)

        # it's easier to define these XPath strings outside of the loop below
        name_path = '//h1[@itemprop="name"]/text()'
        recipeYield_path = '//span[@itemprop="yield"]/text()'
        description_path = '//meta[@name="description"]/@content'
        image_path = '//img[@class="recipe_image"]/@src'
        cookTime_path = '//time[@itemprop="totalTime"]'
        prepTime_path = '//time[@itemprop="activeTime"]'

        # There are some inconsistencies in the format of ingredients,
        # so we'll scrape both: if the first yields nothing, we go
        # with the second.
        ingredients_path = '//span[@itemprop="ingredient"]'
        ingredients_alt_path = '//div[@id="ingredients"]/ul/li/text()'

        # init an empty list
        recipes = []

        # loop through our recipe scopes and extract the recipe data from each
        for r_scope in recipes_scopes:
            # make an empty RecipeItem
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('description', r_scope.select(description_path).extract())
            il.add_value('url', response.url)
            il.add_value('prepTime', parse_iso_date(r_scope.select(prepTime_path)))
            il.add_value('cookTime', parse_iso_date(r_scope.select(cookTime_path)))
            il.add_value('recipeYield', r_scope.select(recipeYield_path).extract())

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                ingredient = i_scope.select('node()/text() | text()').extract()
                ingredients.append(' '.join(i.strip() for i in ingredient).encode('utf-8'))

            # Again, checking to see if our first XPath was a failure.
            if not ingredients:
                ingredient_scopes = r_scope.select(ingredients_alt_path)
                for i_scope in ingredient_scopes:
                    ingredients.append(i_scope.extract().strip().encode('utf-8'))

            il.add_value('ingredients', ingredients)

            # stick this RecipeItem in the array of recipes we will return
            recipes.append(il.load_item())

        # more processing is done by the openrecipes.pipelines. Look at that
        # file to see transforms that are applied to each RecipeItem
        return recipes


class ChowSpider(CrawlSpider, ChowMixin):

    # this is the name you'll use to run this spider from the CLI
    name = "chow.com"

    # URLs not under this set of domains will be ignored
    allowed_domains = [
        "chow.com"
    ]

    # the set of URLs the crawler will start from
    start_urls = [
        "http://www.chow.com/recipes?page=2"
    ]

    # a tuple of Rules that are used to extract links from the HTML page
    rules = (
        # this rule has no callback, so these links will be followed and mined
        # for more URLs. This lets us page through the recipe archives
        Rule(SgmlLinkExtractor(allow=('recipes\?page=.+'))),

        # this rule is for recipe posts themselves. The callback argument will
        # process the HTML on the page, extract the recipe information, and
        # return a RecipeItem object
        # Added $ to prevent duplicates via referral arguments
        Rule(SgmlLinkExtractor(allow=('recipes\/\d\d\d\d\d-.+$')),
             callback='parse_item'),
    )

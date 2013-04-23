from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader


class TastyKitchenMixin(object):

    """
    Using this as a mixin lets us reuse the parse_item method more easily
    """

    # this is the source string we'll store in the DB to aggregate stuff
    # from a single source
    source = 'tastykitchen'

    def parse_item(self, response):

        # we use this to run XPath commands against the HTML in the response
        hxs = HtmlXPathSelector(response)

        # this is the base XPath string for the element that contains the recipe
        # info
        base_path = """//div[@class="recipe-details"]"""

        # the select() method will return a list of HtmlXPathSelector objects.
        # On this site we will almost certainly either get back just one, if
        # any exist on the page
        recipes_scopes = hxs.select(base_path)

        # it's easier to define these XPath strings outside of the loop below
        name_path = '//h1[@itemprop="name"]/text()'
        recipeYield_path = '//label[@for="set_servings"]/input/@value'
        description_path = '//span[@itemprop="summary"]/p/text()'
        image_path = '//img[@class="the_recipe_image"]/@src'
        cookTime_path = '//form/p/time[@itemprop="cookTime"]/@datetime'
        prepTime_path = '//form/p/time[@itemprop="prepTime"]/@datetime'
        ingredients_path = '//span[@itemprop="ingredient"]'
        ingredients_amounts_path = './span[@itemprop="amount"]/text()'
        ingredients_names_path = './span[@itemprop="name"]/text()'
        datePublished_path = '//span[@itemprop="published"]/@datetime'

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
            il.add_value('prepTime', r_scope.select(prepTime_path).extract())
            il.add_value('cookTime', r_scope.select(cookTime_path).extract())
            il.add_value('recipeYield', r_scope.select(recipeYield_path).extract())
            il.add_value('datePublished', r_scope.select(datePublished_path).extract())

            # Simpler to grab the amount and name spans separately,
            # then combine them into a string.
            ingredient_scopes = r_scope.select(ingredients_path)
            amount = ingredient_scopes.select(ingredients_amounts_path).extract()
            name = ingredient_scopes.select(ingredients_names_path).extract()
            ingredients = [" ".join(ing).encode('utf-8') for ing in zip(amount, name)]

            il.add_value('ingredients', ingredients)

            # stick this RecipeItem in the array of recipes we will return
            recipes.append(il.load_item())

        # more processing is done by the openrecipes.pipelines. Look at that
        # file to see transforms that are applied to each RecipeItem
        return recipes


class TastyKitchenSpider(CrawlSpider, TastyKitchenMixin):

    # this is the name you'll use to run this spider from the CLI
    name = "tastykitchen.com"

    # URLs not under this set of domains will be ignored
    allowed_domains = [
        "tastykitchen.com"
    ]

    # the set of URLs the crawler will start from
    start_urls = [
        "http://tastykitchen.com/recipes/page/1/"
    ]

    # a tuple of Rules that are used to extract links from the HTML page
    rules = (

        # this rule has no callback, so these links will be followed and mined
        # for more URLs. This lets us page through the recipe archives
        Rule(SgmlLinkExtractor(allow=('/recipes/page/\d{1,}/?'))),

        # There wasn't an easy regex to specify recipe URLs, so opted
        # for an XPath restriction instead.
        Rule(SgmlLinkExtractor(
             allow=('/recipes/[^/]+/[^/]+/?$'),
             deny=('/recipes/(page|category)/[^/]+/?$')
             ),
        callback='parse_item'),
    )

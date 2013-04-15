from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader
import re


class EpicuriousMixin(object):

    """
    Made as a mixin for easier reuse of the parse_item method
    """

    source = 'epicurious'

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)

        base_path = """//div[@id="primary_content"]"""

        recipes_scopes = hxs.select(base_path)

        name_path = '//h1[@class="fn"]/text()'
        description_path = '//meta[@property="og:description"]/@content'
        url_path = '//meta[@property="og:url"]/@content'
        image_path = '//meta[@property="og:image"][1]/@content'
        time_path = './/p[@class="summary_data"][contains(text(), "Prep Time")]/text()'
        recipeYield_path = '//span[@class="yield"]/text()'
        ingredients_path = '*//*[@class="ingredient"]'
        datePublished_path = '//p[@id="mag_info"]/text()'

        recipes = []

        for r_scope in recipes_scopes:

            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', r_scope.select(name_path).extract())
            il.add_value('image', r_scope.select(image_path).extract())
            il.add_value('url', r_scope.select(url_path).extract())
            il.add_value('description', r_scope.select(description_path).extract())

            # time isn't stored in semantic markup on this site, which
            # makes it a pretty big disaster. ickiness ahead
            time_str = "".join(r_scope.select(time_path).extract())
            if (time_str.strip()):
                prep_pattern = '\s?Prep Time:\s?(\d{1,}\s(?:second|minute|hour|day)s?)'
                prep_time_re = re.match(prep_pattern, time_str, re.I)
                if (prep_time_re):
                    il.add_value('prepTime', prep_time_re.group(1))

                cook_pattern = '.+\s?Cook Time:\s?(\d{1,}\s(?:second|minute|hour|day)s?)'
                cook_time_re = re.match(cook_pattern, time_str, re.I)
                if (cook_time_re):
                    il.add_value('cookTime', cook_time_re.group(1))

            il.add_value('recipeYield', r_scope.select(recipeYield_path).extract())

            # the ingredients are pretty well formatted here, but we do need
            # to trim some trailing whitespace
            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                ingredient = i_scope.select('text()').extract()
                ingredient = "".join(ingredient)
                ingredients.append(ingredient)
            il.add_value('ingredients', ingredients)

            # Date Published is formatted as [Category] | MMM YYYY
            # Split this into a tuple on the | and keep the last part
            datePublished = r_scope.select(datePublished_path).extract()
            datePublished = "".join(datePublished).partition("|")[2]
            il.add_value('datePublished', datePublished)

            recipes.append(il.load_item())

        return recipes


class EpicuriouscrawlSpider(CrawlSpider, EpicuriousMixin):
    name = "epicurious.com"

    allowed_domains = ["epicurious.com"]

    start_urls = [
        "http://www.epicurious.com/tools/searchresults/all"
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=(
            '/tools/searchresults/all\?pageNumber=\d+&pageSize=\d+&resultOffset=\d+'))),
        Rule(SgmlLinkExtractor(allow=(
            '/recipes/food/views/[A-Za-z0-9_-]+')),
            callback='parse_item'),
    )

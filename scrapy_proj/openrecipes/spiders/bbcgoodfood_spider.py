from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader
from openrecipes.util import strip_html


class BBCgoodfoodMixin(object):
    # this is the source string we'll store in the DB to aggregate stuff
    # from a single source
    source = 'bbcgoodfood'

    def remove_whitespace(self, input):
        return " ".join("".join(input).split()).strip()

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        base_path = """//div[@class='hrecipe']"""

        recipes_scopes = hxs.select(base_path)

        name_path = '//h1[@class="fn"][1]/text() | //h1/text()'
        description_path = './/p[@class="subhead summary"]/text()'
        image_path = './/img[@class="photo"]/@src'
        # a lot of the content is repeated inside the '#printSidebar' div
        # so specify that to avoid doubling up content
        prepTime_path = '//div[@id="printSidebar"]/div[@id="prep"]/p[1]/text()'
        cookTime_path = '//div[@id="printSidebar"]/div[@id="prep"]/p[2]/text()'
        recipeYield_path = '//div[@id="printSidebar"]/div[@id="serving"]/p/text()'
        recipeYieldAmount_path = '//span[@class="yield"]/text()'
        ingredients_path = '//div[@id="printSidebar"]/div[@id="ingredients"]//li'

        recipes = []

        for r_scope in recipes_scopes:
            il = RecipeItemLoader(item=RecipeItem())

            il.add_value('source', self.source)

            il.add_value('name', "".join(r_scope.select(name_path).extract()))
            il.add_value('url', response.url)

            # construct base url for image by removing recipe title from url
            base_img_url = '/'.join(response.url.split('/')[:-1])
            img_name = "".join(r_scope.select(image_path).extract()).strip()
            if img_name:
                il.add_value('image', '/'.join([base_img_url, img_name]))

            il.add_value('description', r_scope.select(description_path).extract())

            # remove extra tabs and newlines from Prep Time and Cook Time
            prepSentence = " ".join(r_scope.select(prepTime_path).extract()).strip()
            if prepSentence:
                prepSentence = self.remove_whitespace(prepSentence)
                # also remove preceding 'Prep '
                il.add_value('prepTime', prepSentence.split(' ', 1)[1])

            cookSentence = " ".join(r_scope.select(cookTime_path).extract()).strip()
            if cookSentence:
                cookSentence = self.remove_whitespace(cookSentence)
                il.add_value('cookTime', cookSentence.split(' ', 1)[1])

            # the number of servings is a bit tricky
            # if there's a span with class 'yield' it contains the number of servings
            # otherwise number of servings is given in the <p> element
            if r_scope.select(recipeYieldAmount_path).extract():
                yieldAmount = r_scope.select(recipeYieldAmount_path).extract()[0].strip()
            else:
                yieldAmount = ""

            yieldList = r_scope.select(recipeYield_path).extract()
            if yieldList:
                yieldString = yieldList[0].strip()
                il.add_value('recipeYield', ('%s %s' % (yieldString, yieldAmount)).strip())

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                ingredient = strip_html(i_scope.extract())

                # clean extra tabs and newlines
                ingredient = self.remove_whitespace(ingredient)
                ingredients.append(ingredient)
            il.add_value('ingredients', ingredients)

            recipes.append(il.load_item())

        return recipes


class BBCgoodfoodcrawlSpider(CrawlSpider, BBCgoodfoodMixin):
    name = "bbcgoodfood.com"
    allowed_domains = ["bbcgoodfood.com"]
    start_urls = [
        "http://www.bbcgoodfood.com/searchAZ.do",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/searchAZ.do\?pager\.offset=\d+'))),
        Rule(SgmlLinkExtractor(allow=('/searchAZ.do\?letter=[a-zA-Z]+'))),
        Rule(SgmlLinkExtractor(allow=('/recipes/\d+/.+/?'),
                 deny='/recipes/\d+/.+/?\?.+'),
             callback='parse_item'),
    )

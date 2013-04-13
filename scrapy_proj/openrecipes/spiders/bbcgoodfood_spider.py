from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem

class BBCgoodfoodMixin(object):
    # this is the source string we'll store in the DB to aggregate stuff
    # from a single source
    source = 'bbcgoodfood'

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        base_path = """//body[@id="recipes"]"""

        recipes_scopes = hxs.select(base_path)

        name_path = '//h1/text()'
        description_path = '//div[@class="hrecipe"]/p[@class="subhead summary"]/text()'
        image_path = '//img[@class="photo"]/@src'
        # a lot of the content is repeated inside the '#printSidebar' div
        # so specify that to avoid doubling up content
        prepTime_path = '//div[@id="printSidebar"]/div[@id="prep"]/p[1]/text()'
        cookTime_path = '//div[@id="printSidebar"]/div[@id="prep"]/p[2]/text()'
        recipeYield_path = '//div[@id="printSidebar"]/div[@id="serving"]/p/text()'
        recipeYieldAmount_path = '//span[@class="yield"]/text()'
        ingredients_path = '//div[@id="printSidebar"]/div[@id="ingredients"]//li'

        recipes = []

        for r_scope in recipes_scopes:
            item = RecipeItem()

            item['source'] = self.source

            item['name'] = r_scope.select(name_path).extract()[0].strip()
            item['url'] = response.url
            
            # construct base url for image by removing recipe title from url
            base_img_url = '/'.join(response.url.split('/')[:-1])
            img_name = r_scope.select(image_path).extract()[0]
            item['image'] = '/'.join([base_img_url, img_name])

            item['description'] = r_scope.select(description_path).extract()

            # remove extra tabs and newlines from Prep Time and Cook Time
            prepSentence = " ".join(r_scope.select(prepTime_path).extract()[0].split())
            # also remove preceding 'Prep '
            item['prepTime'] = prepSentence.split(' ',1)[1]
            cookSentence = " ".join(r_scope.select(cookTime_path).extract()[0].split())
            item['cookTime'] = cookSentence.split(' ',1)[1]

            # the number of servings is a bit tricky
            # if there's a span with class 'yield' it contains the number of servings
            # otherwise number of servings is given in the <p> element
            if r_scope.select(recipeYieldAmount_path).extract():
                yieldAmount = r_scope.select(recipeYieldAmount_path).extract()[0].strip()
            else:
                yieldAmount = ""

            yieldString = r_scope.select(recipeYield_path).extract()[0].strip()
            item['recipeYield'] = ('%s %s' % (yieldString, yieldAmount)).strip()

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                amount = i_scope.select('text()').extract()
                # occasionally the name of the ingredient is inside an <a> tag
                name = i_scope.select('a/text()').extract()
                # interleave text and <a> elements to get plain text
                # there's probably a better way to do this
                combo = [y for x in map(None, amount, name) for y in x if y is not None]
                # clean extra tabs and newlines
                ingredient = " ".join("".join(combo).split()).strip()
                ingredients.append(ingredient)
            item['ingredients'] = ingredients

            recipes.append(item)

        return recipes


class BBCgoodfoodcrawlSpider(CrawlSpider, BBCgoodfoodMixin):
    name = "bbcgoodfood"
    allowed_domains = ["bbcgoodfood.com"]
    start_urls = [
        "http://www.bbcgoodfood.com",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/recipes/.+'))),
    )

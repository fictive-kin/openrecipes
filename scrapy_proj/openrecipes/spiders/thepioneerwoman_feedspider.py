from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector, XmlXPathSelector
from openrecipes.items import RecipeItem


class ThepioneerwomanfeedSpider(BaseSpider):
    """
    This parses the RSS feed for thepioneerwoman.com, grabs the original
    links to each entry, and scrapes just those pages. This should be used
    to keep up to date after we have backfilled the existing recipes by
    crawling the whole site
    """
    name = "thepioneerwoman.feed"
    allowed_domains = [
        "thepioneerwoman.com",
        "feeds.feedburner.com",
        "feedproxy.google.com"
    ]
    start_urls = [
        "http://feeds.feedburner.com/pwcooks",
    ]

    def parse(self, response):
        """
        We define a custom parser here because we need to get the link from
        the feed item and then follow it to get the recipe data.

        Getting the data from <content:encoded> seems overly complex, as we
        would have to decode all the encoded characters and then build a DOM
        from that.
        """
        xxs = XmlXPathSelector(response)
        links = xxs.select("//item/*[local-name()='origLink']/text()").extract()
        return [Request(x, callback=self.parse_item) for x in links]

    def parse_item(self, response):
        """
        this is identical to spiders.ThepioneerwomancrawlSpider.parse_item(),
        which is probably not good. we should sort out a way to not repeat
        ourselves
        """
        hxs = HtmlXPathSelector(response)

        base_path = """//div[@itemtype="http://data-vocabulary.org/Recipe"]"""

        recipes_scopes = hxs.select(base_path)

        name_path = '//meta[@property="og:title"]/@content'
        description_path = '//meta[@property="og:description"]/@content'
        url_path = '//meta[@property="og:url"]/@content'
        image_path = '//meta[@property="og:image"][1]/@content'
        prepTime_path = '*//*[@itemprop="prepTime"]/@datetime'
        cookTime_path = '*//*[@itemprop="cookTime"]/@datetime'
        recipeYield_path = '*//*[@itemprop="yield"]/text()'
        ingredients_path = '*//*[@itemprop="ingredient"]'
        datePublished = '*/*[@itemprop="published"]/@datetime'

        recipes = []
        for r_scope in recipes_scopes:
            item = RecipeItem()
            item['name'] = r_scope.select(name_path).extract()
            item['image'] = r_scope.select(image_path).extract()
            item['url'] = r_scope.select(url_path).extract()
            item['description'] = r_scope.select(description_path).extract()

            item['prepTime'] = r_scope.select(prepTime_path).extract()
            item['cookTime'] = r_scope.select(cookTime_path).extract()
            item['recipeYield'] = r_scope.select(recipeYield_path).extract()

            ingredient_scopes = r_scope.select(ingredients_path)
            ingredients = []
            for i_scope in ingredient_scopes:
                amount = i_scope.select('*[@itemprop="amount"]/text()').extract()
                name = i_scope.select('*[@itemprop="name"]/text()').extract()
                amount = "".join(amount).strip()
                name = "".join(name).strip()
                ingredients.append("%s %s" % (amount, name))
            item['ingredients'] = ingredients

            item['datePublished'] = r_scope.select(datePublished).extract()

            recipes.append(item)

        return recipes

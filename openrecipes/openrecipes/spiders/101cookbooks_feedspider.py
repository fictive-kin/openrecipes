from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector, XmlXPathSelector
from openrecipes.items import RecipeItem


class OnehundredonecookbooksfeedSpider(BaseSpider):
    """
    This parses the RSS feed for 101cookbooks.com, grabs the original
    links to each entry, and scrapes just those pages. This should be used
    to keep up to date after we have backfilled the existing recipes by
    crawling the whole site
    """
    name = "101cookbooks.feed"
    allowed_domains = [
        "101cookbooks.com",
        "feeds.101cookbooks.com",
        "feedproxy.google.com"
    ]
    start_urls = [
        "http://feeds.101cookbooks.com/101cookbooks",
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
        this is identical to
        spiders.OnehundredonecookbookscrawlSpider.parse_item(), which is
        probably not good. we should sort out a way to not repeat ourselves
        """
        hxs = HtmlXPathSelector(response)

        base_path = """//div[@id="recipe"]"""

        recipes_scopes = hxs.select(base_path)

        name_path = 'h1/text()'
        description_path = '//meta[@property="og:description"]/@content'
        url_path = '//meta[@property="og:url"]/@content'
        image_path = '//meta[@property="og:image"][1]/@content'
        prepTime_path = './/span[@class="preptime"]/span[@class="value-title"]/@title'
        cookTime_path = './/span[@class="cooktime"]/span[@class="value-title"]/@title'

        # super inconsistent in how the yield is formatted
        recipeYield_path = "|".join([
                                    '//div[@id="recipe"]/p[starts-with(i,"Makes")]/i',
                                    '//div[@id="recipe"]/p[starts-with(i,"Serves")]/i',
                                    '//div[@id="recipe"]/p[starts-with(em,"Makes")]/em',
                                    '//div[@id="recipe"]/p[starts-with(em,"Serves")]/em',
                                    '//div[@id="recipe"][starts-with(p,"Makes")]/p',
                                    '//div[@id="recipe"][starts-with(p,"Serves")]/p',
                                    ])
        ingredients_path = 'blockquote/*'
        datePublished = '//span[@class="published"]/span[@class="value-title"]/@title'

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

            item['ingredients'] = r_scope.select(ingredients_path).extract()

            item['datePublished'] = r_scope.select(datePublished).extract()

            recipes.append(item)

        return recipes

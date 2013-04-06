from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem


class EpicuriousMixin(object):

	"""
	Made as a mixin for easier reuse of the parse_item method
	"""

	source = 'epicurious'

	def parse_item(self, response):

		hxs = HtmlXPathSelector(response)

		base_path = """//div[@id="primary_content"]"""

		recipes_scopes = hxs.select(base_path)

		name_path = '//meta[@property="og:title"]/@content'
		description_path = '//meta[@property="og:description"]/@content'
		url_path = '//meta[@property="og:url"]/@content'
		image_path = '//meta[@property="og:image"][1]/@content'
		prepTime_path = '//span[@class="prepTime"]/span[@class="value-title"]/@title'
		cookTime_path = '//span[@class="duration"]/span[@class="value-title"]/@title'
		recipeYield_path = '//span[@class="yield"]/text()'
		ingredients_path = '*//*[@class="ingredient"]'
		datePublished_path = '//p[@id="mag_info"]/text()'

		recipes = []

		for r_scope in recipes_scopes:

			item = RecipeItem()

			item['source'] = self.source

			# TODO: Need to truncate the "\n at Epicurious.com" tag line appended to each recipe name
			item['name'] = r_scope.select(name_path).extract()
			item['image'] = r_scope.select(image_path).extract()
			item['url'] = r_scope.select(url_path).extract()
			item['description'] = r_scope.select(description_path).extract()

			item['prepTime'] = r_scope.select(prepTime_path).extract()
			item['totalTime'] = r_scope.select(cookTime_path).extract()
			item['recipeYield'] = r_scope.select(recipeYield_path).extract()

			# the ingredients are pretty well formatted here, but we do need
			# to trim some trailing whitespace
			ingredient_scopes = r_scope.select(ingredients_path)
			ingredients = []
			for i_scope in ingredient_scopes:
				ingredient = i_scope.select('text()').extract()
				ingredient = "".join(ingredient)
				ingredients.append(ingredient)
			item['ingredients'] = ingredients

			# Date Published is formatted as [Category] | MMM YYYY
			# Split this into a tuple on the | and keep the last part
			datePublished = r_scope.select(datePublished_path).extract()
			datePublished = "".join(datePublished).partition("|")[2]
			item['datePublished'] = datePublished

			recipes.append(item)

		return recipes

class EpicuriouscrawlSpider(CrawlSpider, EpicuriousMixin):
	name = "epicurious.com"

	allowed_domains = ["epicurious.com"]

	start_urls = [
		"http://www.epicurious.com/tools/searchresults/all"
	]

	rules = (
		Rule(SgmlLinkExtractor(allow=(
			'/tools/searchresults/all?pageNumber=\d+&pageSize=\d+&resultOffset=\d+'))),
		Rule(SgmlLinkExtractor(allow=(
			'/recipes/food/views/[A-Za-z0-9_-]+')),
			callback='parse_item'),
	)










from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Compose, TakeFirst, Join
from scrapy.item import Item, Field
from openrecipes.util import strip_html, get_isodate, get_isoduration


class RecipeItemLoader(ItemLoader):

    source_out = TakeFirst()

    description_out = Compose(TakeFirst(), strip_html)
    image_out = Compose(TakeFirst(), strip_html)
    name_out = Compose(TakeFirst(), strip_html)
    url_out = Compose(TakeFirst(), strip_html)

    creator_out = Compose(TakeFirst())
    dateCreated_out = Compose(TakeFirst(), strip_html, get_isodate)
    dateModified_out = Compose(TakeFirst(), strip_html, get_isodate)
    datePublished_out = Compose(TakeFirst(), strip_html, get_isodate)
    keywords_out = Compose(TakeFirst())

    cookingMethod_out = Compose(TakeFirst())
    cookTime_out = Compose(TakeFirst(), strip_html, get_isoduration)
    ingredients_out = Compose(Join("\n"), strip_html)
    prepTime_out = Compose(TakeFirst(), strip_html, get_isoduration)
    recipeCategory_out = Compose(TakeFirst())
    recipeCuisine_out = Compose(TakeFirst())
    recipeYield_out = Compose(TakeFirst(), strip_html)
    totalTime_out = Compose(TakeFirst(), strip_html, get_isoduration)

    calories_out = Compose(TakeFirst())
    carbohydrateContent_out = Compose(TakeFirst())
    cholesterolContent_out = Compose(TakeFirst())
    fatContent_out = Compose(TakeFirst())
    fiberContent_out = Compose(TakeFirst())
    proteinContent_out = Compose(TakeFirst())
    saturatedFatContent_out = Compose(TakeFirst())
    servingSize_out = Compose(TakeFirst())
    sodiumContent_out = Compose(TakeFirst())
    sugarContent_out = Compose(TakeFirst())
    transFatContent_out = Compose(TakeFirst())
    unsaturatedFatContent_out = Compose(TakeFirst())


class RecipeItem(Item):
    """
    based on the structure of a recipe from schema.org
    http://schema.org/Recipe

    We don't have to fill ALL of these, but we should try to get as many as
    possible. We absolutely MUST get these:
    - name
    - url
    - ingredients
    """

    @classmethod
    def from_dict(kls, d):
        item = kls()
        for name, value in d.iteritems():
            try:
                item[name] = value
            except KeyError:
                pass
        return item

    # our internal stuff
    source = Field()

    # Thing
    description = Field()
    image = Field()  # URL
    name = Field()
    url = Field()  # URL

    # CreativeWork
    creator = Field()  # Organization or Person -- not sure yet how to handle
    dateCreated = Field()  # ISO 8601 Date -- the orig item, not our copy
    dateModified = Field()  # ISO 8601 Date -- the orig item, not our copy
    datePublished = Field()  # ISO 8601 Date -- the orig item, not our copy
    keywords = Field()

    # Recipe
    cookingMethod = Field()
    cookTime = Field()  # ISO 8601 Duration
    ingredients = Field()  # Text; separate with newlines ("\n")
    prepTime = Field()    # ISO 8601 Duration
    recipeCategory = Field()
    recipeCuisine = Field()
    recipeInstructions = Field()  # we don't currently populate this
    recipeYield = Field()
    totalTime = Field()  # ISO 8601 Duration

    # Nutrition
    calories = Field()  # Energy. E.g., "100 calories" http://schema.org/Energy
    carbohydrateContent = Field()  # Mass. E.g., "7 kg" http://schema.org/Mass
    cholesterolContent = Field()  # Mass
    fatContent = Field()  # Mass
    fiberContent = Field()  # Mass
    proteinContent = Field()  # Mass
    saturatedFatContent = Field()  # Mass
    servingSize = Field()  # Mass
    sodiumContent = Field()  # Mass
    sugarContent = Field()  # Mass
    transFatContent = Field()  # Mass
    unsaturatedFatContent = Field()  # Mass

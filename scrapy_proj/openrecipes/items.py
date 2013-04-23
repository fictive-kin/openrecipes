from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Compose, MapCompose, TakeFirst, Join
from scrapy.item import Item, Field
from openrecipes.util import strip_html, trim_whitespace, get_isodate, get_isoduration


def filter_ingredients(x):
    return None if 'ingredient' in x.lower() else x


class RecipeItemLoader(ItemLoader):

    source_out = TakeFirst()

    description_out = Compose(TakeFirst(), strip_html, trim_whitespace)
    image_out = Compose(TakeFirst(), strip_html, trim_whitespace)
    name_out = Compose(TakeFirst(), strip_html, trim_whitespace)
    url_out = Compose(TakeFirst(), strip_html, trim_whitespace)

    creator_out = Compose(TakeFirst(), trim_whitespace)
    dateCreated_out = Compose(TakeFirst(), strip_html, get_isodate)
    dateModified_out = Compose(TakeFirst(), strip_html, get_isodate)
    datePublished_out = Compose(TakeFirst(), strip_html, get_isodate)
    keywords_out = Compose(TakeFirst(), trim_whitespace)

    cookingMethod_out = Compose(TakeFirst(), trim_whitespace)
    cookTime_out = Compose(TakeFirst(), strip_html, get_isoduration)
    ingredients_out = Compose(MapCompose(strip_html, trim_whitespace, filter_ingredients), Join("\n"))
    prepTime_out = Compose(TakeFirst(), strip_html, get_isoduration)
    recipeCategory_out = Compose(TakeFirst(), trim_whitespace)
    recipeCuisine_out = Compose(TakeFirst(), trim_whitespace)
    recipeYield_out = Compose(TakeFirst(), strip_html, trim_whitespace)
    totalTime_out = Compose(TakeFirst(), strip_html, get_isoduration)

    calories_out = Compose(TakeFirst(), trim_whitespace)
    carbohydrateContent_out = Compose(TakeFirst(), trim_whitespace)
    cholesterolContent_out = Compose(TakeFirst(), trim_whitespace)
    fatContent_out = Compose(TakeFirst(), trim_whitespace)
    fiberContent_out = Compose(TakeFirst(), trim_whitespace)
    proteinContent_out = Compose(TakeFirst(), trim_whitespace)
    saturatedFatContent_out = Compose(TakeFirst(), trim_whitespace)
    servingSize_out = Compose(TakeFirst(), trim_whitespace)
    sodiumContent_out = Compose(TakeFirst(), trim_whitespace)
    sugarContent_out = Compose(TakeFirst(), trim_whitespace)
    transFatContent_out = Compose(TakeFirst(), trim_whitespace)
    unsaturatedFatContent_out = Compose(TakeFirst(), trim_whitespace)


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
        il = RecipeItemLoader(item=kls())
        for name, value in d.iteritems():
            try:
                il.add_value(name, value)
            except KeyError:
                pass
        return il.load_item()

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

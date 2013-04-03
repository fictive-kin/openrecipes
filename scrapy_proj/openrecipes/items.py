from scrapy.item import Item, Field


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

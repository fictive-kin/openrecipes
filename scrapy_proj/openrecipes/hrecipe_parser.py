from openrecipes.util import select_class


def parse_recipe(scope, data={}):
    root = select_class(scope, 'hrecipe')
    data['name'] = select_class(root, 'fn').select('.//text()').extract()
    data['yield'] = select_class(root, 'yield').select('.//text()').extract()
    data['published'] = select_class(root, 'published').select('.//text()').extract()
    data['description'] = select_class(root, 'summary').select('.//text()').extract()
    data['duration'] = select_class(root, 'duration').select('.//text()').extract()
    data['prepTime'] = select_class(root, 'preptime').select('.//text()').extract()
    data['cookTime'] = select_class(root, 'cooktime').select('.//text()').extract()
    data['ingredients'] = []
    for ingredient in select_class(root, 'ingredient'):
        data['ingredients'].append(''.join(ingredient.select('.//text()').extract()))
    return data

def _parse(root, schema, data={}):
    rootStr = root.extract()
    attrMap = {
        'photo': '@src',
        'image': '@src',
        'url': '@href',
        'prepTime': '@content',
        'cookTime': '@content',
        'totalTime': '@content',
        'datePublished': '@content',
    }
    data['itemtype'] = schema
    props = root.select('.//*[@itemprop]')
    for prop in props:
        node = prop
        skip = False
        name = prop.select('@itemprop').extract()[0]
        prevValue = data.get(name, None)

        while True:
            if node.extract() == rootStr:
                break
            if node.select('@itemscope'):
                skip = True
                break

            node = node.select('parent::*')[0]

        if skip:
            continue

        if prop.select('@itemscope'):
            value = _parse(prop, prop.select('@itemtype').extract()[0])
        else:
            value = [''.join(prop.select(attrMap.get(name, ".//text()[normalize-space()]")).extract()).strip()]

        if prevValue is None:
            data[name] = value
        else:
            prevValue.extend(value)

    return data


def parse_recipes(scope, data={}):
    schema = 'http://schema.org/Recipe'
    recipes = [_parse(recipe, schema, data) for recipe in scope.select('//*[@itemtype="%s"]' % schema)]
    for recipe in recipes:
        if 'recipeInstructions' in recipe:
            del recipe['recipeInstructions']

    return recipes

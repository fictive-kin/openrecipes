def _parse(root, schema):
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
    data = {'itemtype': schema}
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
            value = [''.join(prop.select(attrMap.get(name, './/text()')).extract())]

        if prevValue is None:
            data[name] = value
        else:
            prevValue.extend(value)

    return data


def parse_recipes(scope):
    name = 'http://schema.org/Recipe'
    return [_parse(recipe, name) for recipe in scope.select('//*[@itemtype="%s"]' % name)]

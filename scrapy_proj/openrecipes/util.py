def parse_iso_date(scope):
    try:
        return scope.select('@content | @datetime').extract()[0]
    except:
        return ''


def flatten(list_or_string):
    if not list_or_string:
        return ''
    if isinstance(list_or_string, list):
        return list_or_string[0]
    else:
        return list_or_string

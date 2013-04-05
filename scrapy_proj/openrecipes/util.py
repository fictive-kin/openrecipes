from lxml.cssselect import CSSSelector


def parse_iso_date(scope):
    try:
        return scope.select('@content | @datetime').extract()[0]
    except:
        return ''


class JQ(object):
    def __init__(self, root):
        self.root = root

    def select(self, selector):
        return JQ(self.root.select(CSSSelector(selector).path))

    def text(self):
        return self.root.select('.//text()').extract()

    def attr(self, name):
        try:
            return self.root[0].select('@' + name).extract()[0]
        except IndexError:
            return None

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/0.16/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import hashlib
import bleach


class MakestringsPipeline(object):
    """
    This processes all the properties of the RecipeItems, all of which are
    lists, and turns them into strings
    """

    def process_item(self, item, spider):
        if not item.get('source', False):
            raise DropItem("Missing 'source' in %s" % item)

        if not item.get('name', False):
            raise DropItem("Missing 'name' in %s" % item)

        if not item.get('url', False):
            raise DropItem("Missing 'url' in %s" % item)

        if not item.get('ingredients', False):
            raise DropItem("Missing 'ingredients' in %s" % item)

        for k, v in item.iteritems():
            if k == 'ingredients':
                # with ingredients, we want to separate each entry with a
                # newline character
                item[k] = "\n".join(v)
            elif isinstance(item[k], list):
                # otherwise just smash them together with nothing between.
                # We expect these to always just be lists with 1 or 0
                # elements, so it effectively converts the list into a
                # string
                item[k] = "".join(v)

            # Use Bleach to strip all HTML tags. The tags could be a source
            # of code injection, and it's generally not safe to keep them.
            # We may consider storing a whitelisted subset in special
            # properties for the sake of presentation.
            item[k] = bleach.clean(item[k], tags=[], attributes={},
                                   styles=[], strip=True)

            # trim whitespace
            item[k] = item[k].strip()

        return item


class DuplicaterecipePipeline(object):
    """
    This tries to avoid grabbing duplicates within the same session.

    Note that it does not persist between crawls, so it won't reject duplicates
    captured in earlier crawl sessions.
    """

    def __init__(self):
        # initialize ids_seen to empty
        self.ids_seen = set()

    def process_item(self, item, spider):
        # create a string that's just a concatenation of name & url
        base = "%s%s" % (item['name'].encode('utf-8'),
                         item['url'].encode('utf-8'))

        # generate an ID based on that string
        hash_id = hashlib.md5(base).hexdigest()

        # check if this ID already has been processed
        if hash_id in self.ids_seen:
            #if so, raise this exception that drops (ignores) this item
            raise DropItem("Duplicate name/url: %s" % base)

        else:
            # otherwise add the has to the list of seen IDs
            self.ids_seen.add(hash_id)
            return item

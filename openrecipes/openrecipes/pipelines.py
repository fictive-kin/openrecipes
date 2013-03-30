# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import hashlib
import bleach


class MakestringsPipeline(object):
    def process_item(self, item, spider):
        if item.get('ingredients', False):
            for k, v in item.iteritems():
                if k == 'ingredients':
                    item[k] = "\n".join(v)
                elif k == 'recipeInstructions':
                    item[k] = "\n".join(v)
                else:
                    item[k] = "".join(v)
                # strips all HTML tags
                item[k] = bleach.clean(item[k], tags=[], attributes={},
                                       styles=[], strip=True)
            return item
        else:
            raise DropItem("Missing ingredients in %s" % item)


class DuplicaterecipePipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        base = "%s%s" % (item['name'].encode('utf-8'),
                         item['url'].encode('utf-8'))
        hash_id = hashlib.md5(base).hexdigest()

        if hash_id in self.ids_seen:
            raise DropItem("Duplicate name/url: %s" % base)

        else:
            self.ids_seen.add(hash_id)
            return item

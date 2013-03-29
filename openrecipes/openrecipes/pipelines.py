# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import hashlib
from scrapy import log


class MakestringsPipeline(object):
    def process_item(self, item, spider):
        if item['ingredients']:
            for k, v in item.iteritems():
                if k == 'ingredients':
                    item[k] = "\n".join(v)
                elif k == 'recipeInstructions':
                    item[k] = "\n".join(v)
                else:
                    item[k] = "".join(v)
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

        log.msg("Dupecheck %s:%s" % (base, hash_id), level=log.INFO)

        if hash_id in self.ids_seen:
            raise DropItem("Duplicate name/url: %s" % item)

        else:
            self.ids_seen.add(hash_id)
            return item

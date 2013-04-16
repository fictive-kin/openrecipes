# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/0.16/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy import log
from scrapy.conf import settings
import pymongo
import hashlib
import datetime


class RejectinvalidPipeline(object):
    def process_item(self, item, spider):
        if not item.get('source', False):
            raise DropItem("Missing 'source' in %s" % item)

        if not item.get('name', False):
            raise DropItem("Missing 'name' in %s" % item)

        if not item.get('url', False):
            raise DropItem("Missing 'url' in %s" % item)

        if not item.get('ingredients', False):
            raise DropItem("Missing 'ingredients' in %s" % item)

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
        base = "%s%s" % (''.join(item['name']).encode('utf-8'),
                         ''.join(item['url']).encode('utf-8'))

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


class MongoDBPipeline(object):
    """
    modified from http://snipplr.com/view/65894/
    some ideas from https://github.com/sebdah/scrapy-mongodb/blob/master/scrapy_mongodb.py
    """

    def __init__(self):
        self.uri = settings['MONGODB_URI']
        self.db = settings['MONGODB_DB']
        self.col = settings['MONGODB_COLLECTION']
        connection = pymongo.mongo_client.MongoClient(self.uri)
        db = connection[self.db]
        self.collection = db[self.col]

        self.collection.ensure_index(settings['MONGODB_UNIQUE_KEY'],
                                     unique=True)
        log.msg('Ensuring index for key %s' % settings['MONGODB_UNIQUE_KEY'])

    def process_item(self, item, spider):

        # mongo takes a dict
        item_dict = dict(item)

        err_msg = ''

        # add timestamp automatically if requested
        if settings['MONGODB_ADD_TIMESTAMP']:
            item_dict['ts'] = datetime.datetime.utcnow()

        try:
            self.collection.insert(item_dict)

        except Exception, e:
            err_msg = 'Insert to MongoDB %s/%s FAILED: %s' % (self.db,
                                                              self.col,
                                                              e.message)
        if err_msg:
            log.msg(err_msg,
                level=log.WARNING, spider=spider)
            return item

        log.msg('Item written to MongoDB database %s/%s' % (self.db, self.col),
                level=log.DEBUG, spider=spider)
        return item


class MakestringsPipeline(object):
    """
    DEPRECATED

    This processes all the properties of the RecipeItems, all of which are
    lists, and turns them into strings
    """

    def process_item(self, item, spider):
        deprecated_msg = "MakestringsPipeline is deprecated. You may need to update your settings.py to the current pipeline config. See settings.py.default for example"
        log.msg(deprecated_msg, level=log.WARNING, spider=spider)
        return item


class CleanDatesTimesPipeline(object):
    """DEPRECATED"""
    def process_item(self, item, spider):
        deprecated_msg = "CleanDatesTimesPipeline is deprecated. You may need to update your settings.py to the current pipeline config. See settings.py.default for example"
        log.msg(deprecated_msg, level=log.WARNING, spider=spider)
        return item

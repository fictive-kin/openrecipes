# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/0.16/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy import log
from scrapy.conf import settings
import pymongo
import hashlib
import bleach
import datetime
from openrecipes.util import get_isodate, get_isoduration


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


class CleanDatesTimesPipeline(object):
    def process_item(self, item, spider):
        #isodates
        if item['datePublished']:
            item['datePublished'] = get_isodate(item['datePublished'], spider)
        if item['dateModified']:
            item['dateModified'] = get_isodate(item['dateModified'], spider)
        if item['dateCreated']:
            item['dateCreated'] = get_isodate(item['dateCreated'], spider)

        #isodurations
        if item['prepTime']:
            item['prepTime'] = get_isoduration(item['prepTime'], spider)
        if item['cookTime']:
            item['cookTime'] = get_isoduration(item['cookTime'], spider)
        if item['totalTime']:
            item['totalTime'] = get_isoduration(item['totalTime'], spider)


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

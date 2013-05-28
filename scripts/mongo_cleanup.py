#!/usr/bin/env python
import pymongo
import os
import sys
import logging
import argparse
script_path = os.path.abspath(os.path.dirname(__file__))
new_path = os.path.abspath((os.path.join(script_path, '..', 'scrapy_proj')))

# add this path so we can import openrecipes.*
sys.path.append(new_path)

# change to this path so we're in the right spot
os.chdir(new_path)

from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem
from openrecipes.items import RecipeItem, RecipeItemLoader
from openrecipes.pipelines import RejectinvalidPipeline


def clean_item(old_dict):
    # copy this so we have an unmodified version
    source_dict = dict(old_dict)
    # remove ts and _id fields from what we pass to loader
    del source_dict['ts']
    del source_dict['_id']

    if VERBOSE:
        print "Examining '%s' from '%s' (%s)..." % (old_dict['name'],
                                                    old_dict['source'],
                                                    old_dict['_id'])

    loader = RecipeItemLoader(RecipeItem())
    for k, v in source_dict.iteritems():
        loader = set_value(loader, k, v)

    new_item = loader.load_item()
    return new_item, source_dict


def set_value(loader, k, v):
    try:
        loader.replace_value(k, v)
    except Exception, e:
        logging.exception(e)
        print "Setting %s to %s" % (k, None)
        loader.replace_value(k, None)

    return loader


def update_record(conn_coll, new_dict, old_dict):
    # restore _id and ts
    new_dict['_id'] = old_dict['_id']
    new_dict['ts'] = old_dict['ts']
    if VERBOSE:
        print "Updating '%s' from '%s' (%s) in db" % (old_dict['name'],
                                                      old_dict['source'],
                                                      old_dict['_id'])
    conn_coll.update({'_id': new_dict['_id']}, new_dict)


def output_changes(new_item, old_dict):
    print "'%s' from '%s' ++++++ " % (old_dict['name'], old_dict['source'])
    for k, v in new_item.iteritems():
        new_val = v
        old_val = old_dict.get(k, None)
        if new_val != old_val:
            print "Changing %s to '%s'" % (k, new_val)


def get_args():
    parser = argparse.ArgumentParser(description='Clean RecipeItems in MongoDB')
    parser.add_argument('-v', dest='VERBOSE', action='store_true',
                       help='be more verbose')
    parser.add_argument('-u', dest='UPDATE', action='store_true',
                       help='write changes to MongoDB. By default, no changes are made')
    args = parser.parse_args()
    return args


VERBOSE = False
UPDATE = False


if __name__ == '__main__':

    args = get_args()
    VERBOSE = args.VERBOSE
    UPDATE = args.UPDATE

    # load the settings
    settings = get_project_settings()

    # get connection to mongodb collection
    mongo_uri = settings['MONGODB_URI']
    mongo_db = settings['MONGODB_DB']
    mongo_coll = settings['MONGODB_COLLECTION']
    conn = pymongo.mongo_client.MongoClient(mongo_uri)
    conn_db = conn[mongo_db]
    conn_coll = conn_db[mongo_coll]

    # make invalid item pipeline object
    rip = RejectinvalidPipeline()

    for r_dict in conn_coll.find():

        try:
            new_item, source_dict = clean_item(r_dict)
            if new_item != source_dict:
                output_changes(new_item, r_dict)
            try:
                # validate the new item
                new_item = rip.process_item(new_item, object())
                # if valid, update (it raises DropItem exception if not)
                if UPDATE:
                    update_record(conn_coll, dict(new_item), r_dict)

            except DropItem, e:
                print "Item invalid; consider deleting record %s. (Reason: %s)" % (r_dict["_id"], e.message)

        except Exception, e:
            logging.exception(e)
            print "Item invalid; consider deleting record %s. (Reason: %s)" % (r_dict["_id"], e.message)

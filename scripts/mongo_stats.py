import pymongo
import os
import sys
import timelib
script_path = os.path.abspath(os.path.dirname(__file__))
new_path = os.path.abspath((os.path.join(script_path, '..', 'scrapy_proj')))

# add this path so we can import openrecipes.*
sys.path.append(new_path)

# change to this path so we're in the right spot
os.chdir(new_path)

from scrapy.utils.project import get_project_settings


def total_by_source(days_back=None):

    q = [
        {"$group": {'_id': "$source", 'totalItems': {"$sum": 1}}},
        {"$sort": {'_id': 1}}
    ]
    if days_back:
        days_back = timelib.strtodatetime("%d days ago" % days_back)
        q.insert(0, {"$match": {'ts': {"$gte": days_back}}})

    totals = conn_coll.aggregate(q)
    if not totals:
        return False

    return totals['result']


def output_totals(days_in_past, totals):
    if (days_in_past):
        print "Last %d day(s) ===========" % days_in_past
    else:
        print "All time ==========="
    for total in totals:
        print "%s: %d" % (total['_id'], total['totalItems'])
    print "\n"


if __name__ == '__main__':

    # load the settings
    settings = get_project_settings()

    # get connection to mongodb collection
    mongo_uri = settings['MONGODB_URI']
    mongo_db = settings['MONGODB_DB']
    mongo_coll = settings['MONGODB_COLLECTION']
    conn = pymongo.mongo_client.MongoClient(mongo_uri)
    conn_db = conn[mongo_db]
    conn_coll = conn_db[mongo_coll]
    days = [1, 7, 30, 0]
    for day in days:
        totals = total_by_source(day)
        output_totals(day, totals)

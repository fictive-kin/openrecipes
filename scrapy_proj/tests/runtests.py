from scrapy.crawler import CrawlerProcess
from scrapy.http import TextResponse
from scrapy.utils.project import get_project_settings
import re
import os

BASE_TEST_PATH = os.path.dirname(os.path.realpath(__file__))


def get_spiders():
    """returns a dict of spiders
    """
    settings = get_project_settings()
    crawler = CrawlerProcess(settings)
    crawler.settings = settings
    crawler.configure()

    spiders = {}
    for spname in crawler.spiders.list():
        spider = crawler.spiders.create(spname)
        module_name = spider.__module__
        if not '_feedspider' in module_name:
            match_obj = re.match(r'openrecipes\.spiders\.([a-zA-Z0-9]+)_spider',
                            module_name)
            if match_obj:
                short_name = match_obj.group(1)
                spiders[short_name] = spider

    return spiders


def get_test_html_paths():
    """returns a dict of arrays of file paths for test html data"""
    paths = {}
    for root, dirs, files in os.walk(BASE_TEST_PATH, topdown=False):
        for name in dirs:
            paths[name] = []
            for troot, tdirs, tfiles in os.walk(os.path.join(root, name),
                                                topdown=False):
                for tfile in tfiles:
                    tpath = os.path.join(troot, tfile)
                    paths[name].append(tpath)
            return paths


def test_scrape(spider, test_files_list):
    """takes a spider and a list of file paths, and runs spider.parse_item
       against the HTML body loaded from each file
    """
    items = []
    for test_file in test_files_list:
        print "scraping %s" % test_file
        body = open(test_file, 'r').read()
        response = TextResponse('http://example.org', body=body)
        item_dict = spider.parse_item(response)
        items.append(item_dict)

    return items


if __name__ == "__main__":
    spiders = get_spiders()
    test_file_paths = get_test_html_paths()

    for name, spider in spiders.iteritems():
        if name in test_file_paths:
            print "testing %s" % name
            print test_scrape(spider, test_file_paths[name])

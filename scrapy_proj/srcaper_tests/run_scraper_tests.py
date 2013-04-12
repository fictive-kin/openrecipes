"""
Put html files to test scrapers against in directory corresponding with spider

For example, testing files for thepioneerwoman_spider go in:

scrapy_proj/tests/thepioneerwoman/
"""

from scrapy.crawler import CrawlerProcess
from scrapy.http import TextResponse
from scrapy.utils.project import get_project_settings
import re
import os
import unittest


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


def create_item_test(item):
    def do_test_scraped_item(self):
        msg = "Name is not in item %s" % (item)
        self.assertIn('name', item, msg)
        msg = "Ingredients is not in item %s" % (item)
        self.assertIn('ingredients', item, msg)
        msg = "URL is not in item %s" % (item)
        self.assertIn('url', item, msg)
    return do_test_scraped_item


# we just need *a* TestCase class; we'll add test methods manually
class CheckScrape(unittest.TestCase):
    pass


if __name__ == "__main__":
    spiders = get_spiders()
    test_file_paths = get_test_html_paths()

    for spider_name, spider in spiders.iteritems():
        if spider_name in test_file_paths:

            # scraping test HTML
            items = test_scrape(spider, test_file_paths[spider_name])

            # create a test method for each item
            for k, item in enumerate(items):
                test_method = create_item_test(item[0])
                test_method.__name__ = 'test_expected_%s_%d' % (spider_name, k)
                setattr(CheckScrape, test_method.__name__, test_method)

    # kick off tests
    unittest.main()

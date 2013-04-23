import argparse
import os
import errno
import lxml
import lxml.html

script_dir = os.path.dirname(os.path.realpath(__file__))


#http://stackoverflow.com/a/5032238
#Recursively try to create a path.  Raise an exception if it fails due to any
#reason other than the directory already existing
def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
        if not os.path.isdir(path):
            raise


def grab_html(args):
    htmldir = os.path.join(script_dir, 'tests', 'html_data', args.name)
    make_sure_path_exists(htmldir)
    t = lxml.html.parse(args.url)
    title = t.find(".//title").text

    with open(os.path.join(htmldir, title + '.html'), 'w') as f:
        f.write(lxml.etree.tostring(t, pretty_print=True))
    # print response.content

    # parsed_url = parse_url(args.start_url)

    # domain = parsed_url.netloc
    # name = args.name.lower()

    # values = {
    #     'crawler_name': name.capitalize(),
    #     'source': name,
    #     'name': domain,
    #     'domain': domain,
    #     'start_url': args.start_url,
    # }

    # spider_filename = os.path.join(script_dir, 'openrecipes', 'spiders', '%s_spider.py' % name)
    # with open(spider_filename, 'w') as f:
    #     f.write(SpiderTemplate % values)

    # if args.with_feed:
    #     feed_url = args.with_feed[0]
    #     feed_domain = parse_url(feed_url).netloc
    #     values['feed_url'] = feed_url
    #     values['name'] = name
    #     if feed_domain == domain:
    #         values['feed_domains'] = domain
    #     else:
    #         values['feed_domains'] = '%s",\n        "%s' % (domain, feed_domain)
    #     feed_filename = os.path.join(script_dir, 'openrecipes', 'spiders', '%s_feedspider.py' % name)
    #     with open(feed_filename, 'w') as f:
    #         f.write(FeedSpiderTemplate % values)


epilog = """
Example usage: python grab_html.py cookincanuck http://www.cookincanuck.com/2013/04/10-minute-thai-shrimp-cucumber-avocado-salad-recipe/
"""
parser = argparse.ArgumentParser(description='Grab page html for testing', epilog=epilog)
parser.add_argument('name', help='Spider name')
parser.add_argument('url', help='URL of recipe page')

args = parser.parse_args()
grab_html(args)

import argparse
import os
import errno
import lxml
import lxml.html
import re

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
    title = title.strip()
    title = "item_%s" % (re.sub(r"([^a-zA-Z0-9\._-]+)", "_", title))
    filename = os.path.join(htmldir, title + '.html')
    with open(filename, 'w') as f:
        f.write(lxml.etree.tostring(t, pretty_print=True))
        print "Wrote %s" % filename

epilog = """
Example usage: python grab_html.py cookincanuck http://www.cookincanuck.com/2013/04/10-minute-thai-shrimp-cucumber-avocado-salad-recipe/
"""
parser = argparse.ArgumentParser(description='Grab page html for testing', epilog=epilog)
parser.add_argument('name', help='Spider name')
parser.add_argument('url', help='URL of recipe page')

args = parser.parse_args()
grab_html(args)

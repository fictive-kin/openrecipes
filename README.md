# Open Recipes

## About

Open Recipes is an open database of recipes.

Our goals are simple:

1. Help publishers make their recipes as discoverable and consumable (get it?) as possible.
2. Prevent good recipes from disappearing when a publisher goes away.

That's pretty much it. We're not trying to save the world. We're just trying to save some recipes.

## The Database

Regular snapshots of the database will be provided as a JSON file. The format will mirror the [schema.org Recipe format](http://schema.org/Recipe). Here's an example:

[recipes.json](http://openrecip.es/recipes.json)

As long as the source of a recipe still exists, preparation instructions will not be provided in the database. For preparation instructions, please link to the source.

## The Story

We're not a bunch of chefs. We're not even good cooks.

When we read about the [acquisition shutdown of Punchfork](http://punchfork.com/pinterest), we just shook our heads. It was the same ol' story:

> We're excited to share the news that we're gonna be rich! To celebrate, we're shutting down the site and taking all your data down with it. So long, suckers!

This part of the story isn't unique, but it continues. When one of our Studiomates spoke up about her disappointment, we listened. Then, [we acted](https://hugspoon.com/punchfork). What happens next surprised us. The CEO of Punchfork [took issue](https://twitter.com/JeffMiller/status/314899821351821312) with our good deed and demanded that we not save any data, even the data (likes) of users who asked us to save their data.

Here's the thing. None of the recipes belonged to Punchfork. They were scraped from various [publishers](https://github.com/fictivekin/openrecipes/wiki/Publishers) to begin with. But, we don't wanna ruffle any feathers, so we're starting over.

Use the force; seek the source?

## The Work

Wanna help? Fantastic. We knew we liked you.

We're gonna be using [the wiki](https://github.com/fictivekin/openrecipes/wiki) to help organize this effort. Right now, there are two simple ways to help:

1. Add a [publisher](https://github.com/fictivekin/openrecipes/wiki/Publishers). We wanna have the most complete list of recipe publishers. This is the easiest way to contribute. Please also add [an issue](https://github.com/fictivekin/openrecipes/issues) and tag it `publisher`.
2. Claim a publisher.

Claiming a publisher means you are taking responsibility for figuring out how to parse recipes from this particular publisher into the [schema.org Recipe format](http://schema.org/Recipe), which will allow us to regularly pull recipes to add to the database.

Each publisher is a [GitHub issue](https://github.com/fictivekin/openrecipes/issues), so you can claim a publisher by claiming an issue. Just like a bug, and just as delicious.

## The Tech

To gather data for Open Recipes, we are building spiders based on [Scrapy](http://scrapy.org), a web scraping framework written in Python. We are using [Scrapy v0.16](http://doc.scrapy.org/en/0.16/) at the moment. To contribute spiders for sites, you should have basic familiarity with:

* Python
* git
* HTML and/or XML

### Setting up a dev environment

*Note: this is strongly biased towards OS X. Feel free to contribute instructions for other operating systems.*

To get things going, you will need the following tools:

1. Python 2.7
1. Git
1. `pip`
1. `virtualenv`

You will probably already have the first two. If you don't have `pip`, follow [the installation instructions in the pip docs](http://www.pip-installer.org/en/latest/installing.html). Then you can [install `virtualenv` using pip](http://www.virtualenv.org/en/latest/#installation).

Once you have `pip` and `virtualenv`, you can clone our repo and install requirements with the following steps:

1. Open a terminal and `cd` to the directory that will contain your repo clone. **For these instructions, we'll assume you `cd ~/src`**.
2. `git clone https://github.com/fictivekin/openrecipes.git` to clone the repo. This will make an `~/src/openrecipes` directory that contains your local repo.
3. `cd ./openrecipes` to move into the newly-cloned repo.
4. `virtualenv --no-site-packages venv` to create a Python virtual environment inside `~/src/openrecipes/venv`.
5. `source venv/bin/activate` to activate your new Python virtual environment
6. `pip install -r requirements.txt` to install the required Python libraries, including Scrapy.
7. `scrapy -h` to confirm that the `scrapy` command was installed. You should get a dump of the help docs.
8. `cd scrapy_proj` to move into the Scrapy project directory
9. `scrapy crawl thepioneerwoman.feed` to test the feed spider written for [thepioneerwoman.com](http://thepioneerwoman.com). You should get output like the following:

	<pre>
    2013-03-30 14:35:37-0400 [scrapy] INFO: Scrapy 0.16.4 started (bot: openrecipes)
    2013-03-30 14:35:37-0400 [scrapy] DEBUG: Enabled extensions: LogStats, TelnetConsole, CloseSpider, WebService, CoreStats, SpiderState
    2013-03-30 14:35:37-0400 [scrapy] DEBUG: Enabled downloader middlewares: HttpAuthMiddleware, DownloadTimeoutMiddleware, UserAgentMiddleware, RetryMiddleware, DefaultHeadersMiddleware, RedirectMiddleware, CookiesMiddleware, HttpCompressionMiddleware, ChunkedTransferMiddleware, DownloaderStats
    2013-03-30 14:35:37-0400 [scrapy] DEBUG: Enabled spider middlewares: HttpErrorMiddleware, OffsiteMiddleware, RefererMiddleware, UrlLengthMiddleware, DepthMiddleware
    2013-03-30 14:35:37-0400 [scrapy] DEBUG: Enabled item pipelines: MakestringsPipeline, DuplicaterecipePipeline
    2013-03-30 14:35:37-0400 [thepioneerwoman.feed] INFO: Spider opened
    2013-03-30 14:35:37-0400 [thepioneerwoman.feed] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
    2013-03-30 14:35:37-0400 [scrapy] DEBUG: Telnet console listening on 0.0.0.0:6023
    2013-03-30 14:35:37-0400 [scrapy] DEBUG: Web service listening on 0.0.0.0:6080
    2013-03-30 14:35:38-0400 [thepioneerwoman.feed] DEBUG: Crawled (200) <GET http://feeds.feedburner.com/pwcooks> (referer: None)
    2013-03-30 14:35:38-0400 [thepioneerwoman.feed] DEBUG: Crawled (200) <GET http://thepioneerwoman.com/cooking/2013/03/beef-fajitas/> (referer: http://feeds.feedburner.com/pwcooks)
    ...
	</pre>

    If you do, [*baby you got a stew going!*](http://www.youtube.com/watch?v=5lFZAyZPjV0)

### Writing your own spiders

For now, we recommend looking at the following spider definitions to get a feel for writing them:

* [spiders/thepioneerwoman_spider.py](/blob/master/scrapy_proj/openrecipes/spiders/thepioneerwoman_spider.py)
* [spiders/thepioneerwoman_feedspider.py](blob/master/scrapy_proj/openrecipes/spiders/thepioneerwoman_feedspider.py)

Both files are extensively documented, and should give you an idea of what's involved. If you have questions, check the [Feedback section](#feedback) and hit us up.

## Feedback?

We're just trying to do the right thing, so we value your feedback as we go. You can ping [Chris](https://github.com/shiflett), [Ed](https://github.com/funkatron), or anyone from [Fictive Kin](https://github.com/fictivekin).
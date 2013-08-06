# Open Recipes

***[Download the latest DB dump](http://openrecipes.s3.amazonaws.com/recipeitems-latest.json.gz)***

## About

Open Recipes is an open database of recipe bookmarks.

Our goals are simple:

1. Help publishers make their recipes as discoverable and consumable (get it?) as possible.
2. Prevent good recipes from disappearing when a publisher goes away.

That's pretty much it. We're not trying to save the world. We're just trying to save some recipes.

## Recipe Bookmarks?

The recipes in Open Recipes do not include preparation instructions. This is why we like to think of Open Recipes as a database of recipe bookmarks. We think this database should provide everything you need to *find* a great recipe, but not everything you need to *prepare* a great recipe. For preparation instructions, please link to the source.

## The Database

Regular snapshots of the database will be provided as JSON. The format will mirror the [schema.org Recipe format](http://schema.org/Recipe). We've [posted an example dump of data](http://openrecipes.s3.amazonaws.com/openrecipes.txt) so you can get a feel for it.

## The Story

We're not a bunch of chefs. We're not even good cooks.

When we read about the [acquisition shutdown of Punchfork](http://punchfork.com/pinterest), we just shook our heads. It was the same ol' story:

> We're excited to share the news that we're gonna be rich! To celebrate, we're shutting down the site and taking all your data down with it. So long, suckers!

This part of the story isn't unique, but it continues. When one of our Studiomates spoke up about her disappointment, we listened. Then, [we acted](https://hugspoon.com/punchfork). What happens next surprised us. The CEO of Punchfork [took issue](https://twitter.com/JeffMiller/status/314899821351821312) with our good deed and demanded that we not save any data, even the data (likes) of users who asked us to save their data.

Here's the thing. None of the recipes belonged to Punchfork. They were scraped from various [publishers](https://github.com/fictivekin/openrecipes/wiki/Publishers) to begin with. But, we don't wanna ruffle any feathers, so we're starting over.

Use the force; seek the source?

## The Work

Wanna help? Fantastic. We knew we liked you.

Head over to [the wiki](https://github.com/fictivekin/openrecipes/wiki) to see how you can help out.


## Feedback?

We're just trying to do the right thing, so we value your feedback as we go. You can ping [Ed](https://github.com/funkatron), [Chris](https://github.com/shiflett), [Andreas](https://github.com/andreasb), or anyone from [Fictive Kin](https://github.com/fictivekin). General suggestions and feedback to [openrecipes@fictivekin.com](mailto:openrecipes@fictivekin.com) are welcome, too.

We're also gonna be on IRC, so please feel free to join us if you have any questions or comments. We'll be hanging out in #openrecipes on Freenode. See you there!

## License

The Open Recipes Database is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/3.0/deed.en_US">Creative Commons Attribution 3.0 Unported License</a>.

<a rel="license" href="http://creativecommons.org/licenses/by/3.0/deed.en_US"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by/3.0/88x31.png" /></a>

© 2013 Fictive Kin LLC

## CHANGELOG

*Not every change, but notable ones that may require action*

* 2013-04-15: `pipelines.MakestringsPipeline` and `pipelines.CleanDatesTimesPipeline` have been deprecated, and `pipelines.RejectinvalidPipeline` has been added. Your `ITEM_PIPELINES` config in `settings.py` should look something like this:

    ```python
    ITEM_PIPELINES = [
        'openrecipes.pipelines.RejectinvalidPipeline',
        'openrecipes.pipelines.DuplicaterecipePipeline',
        # uncomment if you want to insert results into MongoDB
        # 'openrecipes.pipelines.MongoDBPipeline',
    ]
    ```
* 2013-04-14: Spiders now use a RecipeItemLoader to store data scraped from a page. This allows us to do cleanup of properties without relying on a pipeline class, which makes testing significantly easier. See [spiders/thepioneerwoman.py](https://github.com/fictivekin/openrecipes/blob/f0f7acb1ed23098258f198b2496f53aa0e8cfe3f/scrapy_proj/openrecipes/spiders/thepioneerwoman_spider.py) with updated comments to see the new approach. Example:

    ```python
    il = RecipeItemLoader(item=RecipeItem())
    il.add_value('name', r_scope.select(name_path).extract())
    # [...]
    recipes.append(il.load_item())
    ```

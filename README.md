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

## Feedback?

We're just trying to do the right thing, so we value your feedback as we go. You can ping [Chris](https://github.com/shiflett), [Ed](https://github.com/funkatron), or anyone from [Fictive Kin](https://github.com/fictivekin).
import os.path

import pycurl
import web


## Mapping
urls = (
    '/', 'index'
)

## Define the application
app = web.application(urls, globals())

## Make sure we render templates
render = web.template.render('templates/')


## Load recipes from Amazon S3
def get_recipes():
    ## Setup a Local Recipe List 
    RECIPE_PATH = "openrecipes.txt"
    if not os.path.isfile(RECIPE_PATH):
        url = 'http://openrecipes.s3.amazonaws.com/openrecipes.txt'
        RECIPE_PATH = "openrecipes.txt"
        recipe_list = open(RECIPE_PATH, "w")
        r = pycurl.Curl()
        r.setopt(r.WRITEDATA, recipe_list)
        r.setopt(r.URL, url)
        recipes = r.perform()
        r.close()
        recipe_list.close()

    ## Setup Recipe List
    recipes = open(RECIPE_PATH, "r")
    web_recipe_list = []    

    for each_recipe in recipes:
        recipe_dict = eval(each_recipe)
        web_recipe_list.append(recipe_dict)

    ## Cleanup
    recipes.close()

    ## Debug
    print "LOADED " + str(len(web_recipe_list)) + " recipes!"

    return web_recipe_list



## Functionality
class index:
    def GET(self):
        return render.index(get_recipes())


## Start it up!
if __name__ == "__main__":
    app.run()

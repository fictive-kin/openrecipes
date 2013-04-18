from openrecipes.util import get_isodate, parse_isodate, get_isoduration, parse_isoduration, strip_html, trim_whitespace
import unittest
import datetime


class ISODateTests(unittest.TestCase):

    def test_get_isodate(self):
        self.assertEqual('2009-10-11', get_isodate("October 11 2009"))

    def test_parse_isodate(self):
        dt = datetime.date(year=2009, month=10, day=11)
        self.assertEqual(dt, parse_isodate('2009-10-11'))

    def test_get_isoduration(self):
        self.assertEqual('PT15M', get_isoduration("15 minutes"))

    def test_parse_isoduration(self):
        delta = datetime.timedelta(days=1)
        self.assertEqual(delta, parse_isoduration('P1D'))

    def test_parse_isoduration_2(self):
        delta = datetime.timedelta(minutes=15)
        self.assertEqual(delta, parse_isoduration('PT15M'))

    def test_parse_isoduration_invalid(self):
        self.assertEqual(None, parse_isoduration('PT1HPT1H'))


class StripHTMLTests(unittest.TestCase):

    def test_strip_html(self):
        html_marked = '<strong>foo</strong> <script>bar baz</script>'
        self.assertEqual('foo bar baz', strip_html(html_marked))

    def test_strip_html_complex(self):
        html_marked = """<div class="shortcode recipe-box" itemscope="" itemtype="http://data-vocabulary.org/Recipe">
                    <div class="recipe-header" title="recipe">
                        <div class="recipe-box-label">Recipe</div>
                        <h2 class="recipe-title" id="recipe-form-266104"><span itemprop="name">Pesto Pasta Salad</span></h2>
                        <dl class="recipe-data">
                            <dt>Prep Time:</dt><dd> <time itemprop="prepTime" datetime="PT1H">1 Hour</time></dd>
                            <dt>Cook Time:</dt><dd> <time itemprop="cookTime" datetime="PT12M">12 Minutes</time></dd>
                            <dt>Difficulty:</dt><dd> Easy</dd>
                            <dt>Servings:</dt><dd> <span itemprop="yield">4</span></dd>
                        </dl>
                    </div><!--/recipe-header-->
                <div class="shortcode-box">
                    <img width="213" src="http://tastykitchen.com/recipes/files/2013/04/pestopasta-420x279.jpg" class="photo" itemprop="photo">
                    <a class="print-recipe-card" href="http://tastykitchen.com/recipes/salads/pesto-pasta-salad-2/?print=1/#size3x5" id="pl_266104">Print Recipe</a>
                </div>
                                <h4 class="recipe-sub-head">Ingredients</h4>
                <ul><li><span itemprop="ingredient" itemscope="" itemtype="http://data-vocabulary.org/RecipeIngredient"><span itemprop="amount">8 ounces, weight</span><span itemprop="name"> Short Fusilli Or Rotini (corkscrew) Pasta</span></span></li><li><span itemprop="ingredient" itemscope="" itemtype="http://data-vocabulary.org/RecipeIngredient"><span itemprop="amount">1 head</span><span itemprop="name"> (large) Romaine Lettuce, Sliced Into 1-inch Pieces</span></span></li><li><span itemprop="ingredient" itemscope="" itemtype="http://data-vocabulary.org/RecipeIngredient"><span itemprop="amount">1/3 cup</span><span itemprop="name"> Prepared Pesto</span></span></li><li><span itemprop="ingredient" itemscope="" itemtype="http://data-vocabulary.org/RecipeIngredient"><span itemprop="amount">1/2 cup</span><span itemprop="name"> Shredded Parmesan Cheese</span></span></li><li><span itemprop="ingredient" itemscope="" itemtype="http://data-vocabulary.org/RecipeIngredient"><span itemprop="amount">1 cup</span><span itemprop="name"> Grape Tomatoes, Halved</span></span></li><li><span itemprop="ingredient" itemscope="" itemtype="http://data-vocabulary.org/RecipeIngredient"><span itemprop="amount">1/2 cup</span><span itemprop="name"> Black Or Kalamata Olives, Halved</span></span></li><li><span itemprop="ingredient" itemscope="" itemtype="http://data-vocabulary.org/RecipeIngredient"><span itemprop="amount">4 ounces, weight</span><span itemprop="name"> Mozzarella Cheese, Cut Into Cubes</span></span></li><li><span itemprop="ingredient" itemscope="" itemtype="http://data-vocabulary.org/RecipeIngredient"><span itemprop="amount">1/2 cup</span><span itemprop="name"> Mayonnaise</span></span></li><li><span itemprop="ingredient" itemscope="" itemtype="http://data-vocabulary.org/RecipeIngredient"><span itemprop="amount">1/2 cup</span><span itemprop="name"> Sour Cream</span></span></li><li><span itemprop="ingredient" itemscope="" itemtype="http://data-vocabulary.org/RecipeIngredient"><span itemprop="amount">1/4 cup</span><span itemprop="name"> Milk, More For Thinning</span></span></li><li><span itemprop="ingredient" itemscope="" itemtype="http://data-vocabulary.org/RecipeIngredient"><span itemprop="amount">1/2 teaspoon</span><span itemprop="name"> Salt</span></span></li><li><span itemprop="ingredient" itemscope="" itemtype="http://data-vocabulary.org/RecipeIngredient"><span itemprop="amount">1/2 teaspoon</span><span itemprop="name"> Pepper</span></span></li><li><span itemprop="ingredient" itemscope="" itemtype="http://data-vocabulary.org/RecipeIngredient"><span itemprop="amount">4 Tablespoons</span><span itemprop="name"> Pine Nuts (optional)</span></span></li><li><span itemprop="ingredient" itemscope="" itemtype="http://data-vocabulary.org/RecipeIngredient"><span itemprop="amount">8 </span><span itemprop="name"> Extra Parmesan, For Sprinkling</span></span></li></ul>              <h4 class="recipe-sub-head">Preparation Instructions</h4>
                <div itemprop="instructions">
                <p>Cook the pasta in salted water until done, then drain and rinse in cold water. Allow pasta to dry slightly, then toss in a bowl with 4 tablespoons pesto. (Add more if you want the pasta to be more coated.) Add Parmesan and toss. Cover and refrigerate pasta until cold.</p>
<p>Make the dressing by whisking together the mayonnaise, sour cream, and milk with the rest of the pesto. Add salt and pepper, then taste and adjust seasonings as needed. The dressing needs to be somewhat thin and pourable in order to coat the lettuce and pasta later. Set the dressing aside.</p>
<p>If you're using pine nuts, toast them over medium-low heat in a small skillet. Set them aside. </p>
<p>To assemble the salads, make a bed of lettuce in a large bowl, then add a generous layer of pesto-coated pasta. Add tomatoes, olives, and chunks of cheese. Spoon a good amount of dressing all over the top; it should be thin enough to seep down into the salad, not so thick it will stay on top of everything.</p>
<p>Sprinkle salads with a little extra Parmesan and serve!</p>
                </div>
                <p style="display:none;">Posted by <span itemprop="author">Ree</span> on <span itemprop="published" datetime="2013-04-15">April 15 2013</span></p>
                </div>
        """
        html_stripped = """\n                    \n                        Recipe\n                        Pesto Pasta Salad\n                        \n                            Prep Time: 1 Hour\n                            Cook Time: 12 Minutes\n                            Difficulty: Easy\n                            Servings: 4\n                        \n                    \n                \n                    \n                    Print Recipe\n                \n                                Ingredients\n                8 ounces, weight Short Fusilli Or Rotini (corkscrew) Pasta1 head (large) Romaine Lettuce, Sliced Into 1-inch Pieces1/3 cup Prepared Pesto1/2 cup Shredded Parmesan Cheese1 cup Grape Tomatoes, Halved1/2 cup Black Or Kalamata Olives, Halved4 ounces, weight Mozzarella Cheese, Cut Into Cubes1/2 cup Mayonnaise1/2 cup Sour Cream1/4 cup Milk, More For Thinning1/2 teaspoon Salt1/2 teaspoon Pepper4 Tablespoons Pine Nuts (optional)8  Extra Parmesan, For Sprinkling              Preparation Instructions\n                \n                Cook the pasta in salted water until done, then drain and rinse in cold water. Allow pasta to dry slightly, then toss in a bowl with 4 tablespoons pesto. (Add more if you want the pasta to be more coated.) Add Parmesan and toss. Cover and refrigerate pasta until cold.\nMake the dressing by whisking together the mayonnaise, sour cream, and milk with the rest of the pesto. Add salt and pepper, then taste and adjust seasonings as needed. The dressing needs to be somewhat thin and pourable in order to coat the lettuce and pasta later. Set the dressing aside.\nIf you're using pine nuts, toast them over medium-low heat in a small skillet. Set them aside. \nTo assemble the salads, make a bed of lettuce in a large bowl, then add a generous layer of pesto-coated pasta. Add tomatoes, olives, and chunks of cheese. Spoon a good amount of dressing all over the top; it should be thin enough to seep down into the salad, not so thick it will stay on top of everything.\nSprinkle salads with a little extra Parmesan and serve!\n                \n                Posted by Ree on April 15 2013\n                \n        """
        self.assertEqual(html_stripped, strip_html(html_marked))


class TrimWhitespaceTests(unittest.TestCase):

    def test_trim_whitespace(self):
        untrimmed = """\n                    \n                        Recipe\n"""
        trimmed = "Recipe"
        self.assertEqual(trimmed, trim_whitespace(untrimmed))

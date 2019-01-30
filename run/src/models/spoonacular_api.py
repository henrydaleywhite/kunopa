import json
import requests

from pprint import pprint

filename = "spoonacular_key.txt"
test_ing_list = "apples%2Cflour%2Csugar"
test_list = ['basil', 'garlic', 'tomato', 'olive oil', 'pasta', 'thyme', 'parsley', 'lemon', 'rosemary']

def get_api_key(filename):
    """get the api key from a seperately stored file. 
    Free API key for spoonacular api is available at 
    https://market.mashape.com/spoonacular/recipe-food-nutrition/pricing
    """
    with open(filename, 'r') as open_file:
        return open_file.read()


def format_ingred_list(ing_list):
    """convert a list of ingredients into a string with
    expected api format of '%2C' between search terms
    """
    return_str = ""
    for ingredient in ing_list:
        if ing_list.index(ingredient) == 0:
            return_str += ingredient
        else:
            return_str += "%2C" + ingredient
    return return_str


def api_call(api_key, ing_list, num_results):
    """return a dictionary result based on an api call with dynamic
    values for the ingredient list and number of results to display
    """
    stc_1 = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/"
    stc_2 = "recipes/findByIngredients?fillIngredients=true&ingredients="
    stc_3 = "&limitLicense=false&number="
    stc_4 = "&ranking=1"
    response = requests.get(f"{stc_1}{stc_2}{ing_list}{stc_3}{num_results}{stc_4}",
        headers={
            "X-Mashape-Key": api_key,
            "Accept": "application/json"
        }
    )
    data = response.json()
    return data


def write_file(filename, dictionary):
    """write dictionary to a json file"""
    with open(filename, 'w') as open_file:
        json.dump(dictionary, open_file)

def parse_call_results(response_list):
    """take the results of the api_call and return a dictionary
    with the id, url, and used/missed/extra ingredients
    """
    return_dict = {}
    for recipe in response_list:
        used = recipe['usedIngredients']
        unused = recipe['unusedIngredients']
        extra = recipe['missedIngredients']
        image = recipe['image']
        name = recipe['title']
        url_pt1 = "https://spoonacular.com/"
        recipe_id = recipe['id']
        url_pt3 = recipe['title'].lower().replace(' ','-')
        url = url_pt1 + url_pt3 + '-' + str(recipe_id)
        return_dict[recipe_id] = {'url': url, 'used': used, 
                                'image': image, 'name': name,
                                'unused': unused, 'extra': extra}
    return return_dict

# response = requests.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/529503/information?includeNutrition=false",
#   headers={
#     "X-Mashape-Key": "DmlB2lXUyvmshaqU6dBOJ637neXBp1wAUyYjsn4NdYKNaIr1IA",
#     "Accept": "application/json"
#   }
# )

if __name__ == "__main__":
    ingredient_list = format_ingred_list(test_list)
    api_key = get_api_key(filename)
    response = api_call(api_key, ingredient_list, 2)
    response_to_write = parse_call_results(response)
    write_file('return_dict.json', response_to_write)
    # ingredient_list = format_ingred_list(test_list)
    # api_key = get_api_key(filename)
    # response_to_write = api_call_test(api_key, ingredient_list, 2)
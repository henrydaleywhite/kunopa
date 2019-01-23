import json
import requests

from pprint import pprint

filename = "spoonacular_key.txt"
test_ing_list = "apples%2Cflour%2Csugar"
test_list = ['sugar', 'flour', 'apples']

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


def api_call_test(api_key, ing_list, num_results):
    """return a dictionary result based on an api call with dynamic
    values for the ingredient list and number of results to display
    """
    stc_1 = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/"
    stc_2 = "recipes/findByIngredients?fillIngredients=true&ingredients="
    stc_3 = "&limitLicense=false&number="
    stc_4 = "&ranking=1"
    response = f"{stc_1}{stc_2}{ing_list}{stc_3}{num_results}{stc_4}"
    print(response)


if __name__ == "__main__":
    ingredient_list = format_ingred_list(test_list)
    api_key = get_api_key(filename)
    response_to_write = api_call(api_key, ingredient_list, 2)
    write_file('api_call.json', response_to_write)
    # ingredient_list = format_ingred_list(test_list)
    # api_key = get_api_key(filename)
    # response_to_write = api_call_test(api_key, ingredient_list, 2)
import json
from pprint import pprint

from bs4 import BeautifulSoup


list_ingred_info = []
ingredient_dcty = {}


def file_to_line_list(filename):
    """take a html/text file input from the flavor bible and convert it
    to a list where each element is the parent ingredient followed by
    all associated information
    """
    with open(filename, 'r') as open_file:
        i = -1
        # Ingredients for "avoid" and "flavor affinities" attributes not
        # collected in the current iteration of the application
        find_fa_text = 'flavor affinities'
        find_av_text_1 = '<p class="noindent2"><span class="blue">avoid'
        find_av_text_2 = '<p class="noindent4"><strong class="calibre3">avoid'
        find_av_text_3 = '<p class="calibre12"><strong class="calibre3">avoid'
        # do not split variable with 3 quotes, it stops recognizing the tag
        find_av_text_4 = '<p class="calibre12"><a id="page-335"></a><strong class="calibre3">avoid'
        # list to iterate over to find which instance of avoid is present
        avoid_find_list = [find_av_text_1, find_av_text_2,
                            find_av_text_3, find_av_text_4]
        
        for line in open_file:
            if '<h1 class="sub1"' not in line:
                # parent ingredient should be the first thing put into the list
                # if the first chunk of text isn't parent, ignore it
                if len(list_ingred_info) == 0:
                    continue
                # if parent ingredient exists, concat following text
                elif len(list_ingred_info) > 0:
                    list_ingred_info[i] += line
            # append parent ingredient information as new element of list
            else:
                if i >= 0:
                    # TODO find a "nicer" solution for flavor affinities/avoid
                    # avoid case sensitivity with lower()
                    lower_text = list_ingred_info[i].lower()
                    # find index of "flavor affinities" text, -1 if not found
                    find_value_1 = lower_text.find(find_fa_text)
                    find_value_2 = -1
                    # iterate through possible tags for "avoid" to find index
                    for item in avoid_find_list:
                        if lower_text.find(item) > find_value_2:
                            find_value_2 = lower_text.find(item)
                    # if both "avoid" and "flavor affinities" exist for an
                    # entry, find index of the one that occurs first and 
                    # truncate from that value
                    if find_value_1 > -1 and find_value_2 > -1:
                        first_val_fnd = min([find_value_1, find_value_2])
                        list_ingred_info[i] = list_ingred_info[i][:first_val_fnd:]
                    # if only "flavor affinities" exists, find starting index
                    # and truncate from that value
                    elif find_value_1 > -1:
                        list_ingred_info[i] = list_ingred_info[i][:find_value_1:]
                    # if only "avoid" exists, find starting index and 
                    # truncate from that value
                    elif find_value_2 > -1:
                        list_ingred_info[i] = list_ingred_info[i][:find_value_2:]
                list_ingred_info.append(line)
                i += 1


def line_list_to_dcty():
    """Take a list and process it using beautiful soup to extract
    relevant information and insert into a dictionary. Attributes to be 
    collected are parent ingredient name, Season, Taste, Function,
    Botanical relatives, Weight, Volume, Techniques, Tips, and a list of
    child ingredients with their respective pairing strength.
    """
    for i in range(len(list_ingred_info)):
        soup = BeautifulSoup(list_ingred_info[i], 'html.parser')
        # parent ingredient info has tag <h1> and class="sub1"
        parent_ingred = soup.find('h1','sub1').text
        # The ingredient’s seasonal peak(s)
        ing_season = ""
        # The ingredient’s primary taste(s), e.g., bitter, salty, sour, sweet
        ing_taste = ""
        # The ingredient’s intrinsic property, e.g., cooling vs. warming
        ing_function = ""
        # The ingredient's botanical relatives
        ing_bot_relatives = ""
        # The ingredient’s relative density, e.g., from light to heavy
        ing_weight = ""
        # The ingredient’s relative flavor “loudness,” e.g., from quiet to loud
        ing_volume = ""
        # The most commonly used techniques to prepare the ingredient
        ing_techniques = ""
        # Suggestions for using the ingredient
        ing_tips = ""
        # Compatible flavor groups
        ing_affinities = ""
        # Incompatible flavors
        ing_avoid = ""
        # child ingredient info has tag <p> and class="calibre12"
        raw_subingred_text = soup.find_all('p','calibre12')
        # parent level 'attribute' info has <p> and class="noindent2"
        raw_subingred_attr_text = soup.find_all('p','noindent2')
        
        for k in range(len(raw_subingred_attr_text)):
            if "Season:" in raw_subingred_attr_text[k].text and not ing_season:
                ing_season = raw_subingred_attr_text[k].text[len("Season: ")::]
            elif "Taste:" in raw_subingred_attr_text[k].text and not ing_taste:
                ing_taste = raw_subingred_attr_text[k].text[len("Taste: ")::]
            elif "Function:" in raw_subingred_attr_text[k].text and not ing_function:
                ing_function = raw_subingred_attr_text[k].text[len("Function: ")::]
            elif ("Botanical relatives:" in raw_subingred_attr_text[k].text 
                    and not ing_bot_relatives):
                ing_bot_relatives = raw_subingred_attr_text[k].text[len("Botanical relatives: ")::]
            elif "Weight:" in raw_subingred_attr_text[k].text and not ing_weight:
                ing_weight = raw_subingred_attr_text[k].text[len("Weight: ")::]
            elif "Volume:" in raw_subingred_attr_text[k].text and not ing_volume:
                ing_volume = raw_subingred_attr_text[k].text[len("Volume: ")::]
            elif "Techniques:" in raw_subingred_attr_text[k].text and not ing_techniques:
                ing_techniques = raw_subingred_attr_text[k].text[len("Techniques: ")::]
            elif "Tips:" in raw_subingred_attr_text[k].text and not ing_tips:
                ing_tips = raw_subingred_attr_text[k].text[len("Tips: ")::]
        
        children = []
        # iterate through list generated by find_all to get dict ready text
        for j in range(len(raw_subingred_text)):
            subingred_text = raw_subingred_text[j].text
            # split due to child ingredients like "BUTTER, unsalted" throwing
            # off results of isupper() method. Only check first word
            subingred_split = subingred_text.split()
            if subingred_split[0].isupper():
                # uppercase text starting with '*' character is strongest
                if subingred_text[0] == "*":
                    children.append({subingred_text.lower()[1::] : 4})
                # uppercase text without '*' character is second strongest
                else:
                    children.append({subingred_text.lower() : 3})
            else:
                # lowercase bolded text is third strongest
                str_line_info = str(raw_subingred_text[j])
                if str_line_info.find('calibre3') > -1:
                    children.append({subingred_text.lower() : 2})
                # lowercase unbolded text is weakest
                else:
                    children.append({subingred_text.lower() : 1})
        
        # insert parent ingredient key with child ingredient values
        ingredient_dcty[parent_ingred.lower()] = {
            'children' : children,
            'season' : ing_season,
            'taste' : ing_taste,
            'function' : ing_function,
            'botanical relatives' : ing_bot_relatives,
            'weight' : ing_weight,
            'volume' : ing_volume,
            'techniques' : ing_techniques,
            'tips' : ing_tips
        }


def write_file(filename, dictionary):
    """write dictionary to a json file"""
    with open(filename, 'w') as open_file:
        json.dump(dictionary, open_file)


if __name__ == "__main__":
    file_to_line_list("z_test.html")
    line_list_to_dcty()
    write_file("output.json", ingredient_dcty)
    # file_to_line_list("chapter003_4.html")
    # pprint(list_ingred_info)
    # line_list_to_dcty()
    # pprint(ingredient_dcty)
    # write_file("test.json", ingredient_dcty)
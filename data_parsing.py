import json
from pprint import pprint


def load_dictionary(filename):
    """imports json file as a dictionary"""
    with open(filename, 'r') as json_file:
        return json.load(json_file)


def get_dict_keys(dictionary):
    """get key values of a given dictionary"""
    return list(dictionary.keys())


def get_dict_children(dictionary, child_key="children"):
    """gets all keys for a dictionary within a dictionary. Default child 
    key is set to search for string 'children' as its key. Returns a set
    """
    child_key_set = set()
    for key in dictionary.keys():
        for element in dictionary[key][child_key]:
            for baby in element:
                child_key_set.add(baby)
    return child_key_set


def write_txt_from_iterable(filename, iterable):
    """write a list/set to a txt file with each item on its own line"""
    with open(filename, 'w') as open_file:
        for element in iterable:
            print(element, file=open_file)


def impt_iter_from_delim_txt(filename, delimiter='|'):
    """import a delimited text file and return a list of lists where each
    parent list is a line and each child list is the delimited value
    """
    list_to_return = []
    with open(filename, 'r') as open_file:
        for line in open_file:
            # append list with lists of delimited values & strip out \n
            list_to_return.append(line.rstrip().split(delimiter))
        return list_to_return


if __name__ == "__main__":
    # my_dict = load_dictionary("output.json")
    # my_dict_parents_list = get_dict_keys(my_dict)
    # my_dict_children_set = get_dict_children(my_dict)
    # write_txt_from_iterable("parents.txt", my_dict_parents_list)
    # write_txt_from_iterable("children.txt", my_dict_children_set)
    pprint(impt_iter_from_delim_txt('initial_child.txt'))
from statistics import mean
from collections import namedtuple
from pprint import pprint

from .opencursor import OpenCursor

# dictionary that will be used to store ingredient pairing info
ingredient_weightings = {}
selected_ingredient_pks = []
api_input = []
ingredient_number = 1
full_selection_lookup = []
full_selection = []
Ingredient = namedtuple('Ingredient', 
                            ['pk',
                            'name',
                            'own_parent_pk',
                            'pairing_str'])


def clear_results():
    """reset all variables to initial values"""
    global ingredient_weightings
    global selected_ingredient_pks
    global api_input
    global ingredient_number
    global full_selection_lookup
    global full_selection
    ingredient_weightings = {}
    selected_ingredient_pks = []
    api_input = []
    ingredient_number = 1
    full_selection_lookup = []
    full_selection = []

def populate_full_selection():
    """function to populate and sort a list of all possible
    children while avoiding duplicate 'search term' values
    """
    global full_selection_lookup
    full_selection_lookup = []
    for ing_list in full_selection:
        index_for_append = len(full_selection_lookup)
        full_selection_lookup.append([])
        for ing in ing_list:
            if ing.own_parent_pk not in selected_ingredient_pks:
                weight = int(mean(ingredient_weightings[ing.own_parent_pk]))
                inst = Ingredient(ing.pk, ing.name, ing.own_parent_pk, weight)
                full_selection_lookup[index_for_append].append(inst)
        for lists in full_selection_lookup:
            lists.sort(key=sort_funct, reverse=True)


def sort_funct(val):
    """sort function on pairing_str for populate_full_selection function"""
    return val.pairing_str

        

def get_base_ingredient_list():
    """function to be run to generate list of parents to be selected for
    first ingredient. Returns a list of ParentIngredient class instances
    """
    with OpenCursor() as cur:
        SQL = """ SELECT * from parent_ingredients order by pk ASC"""
        cur.execute(SQL)
        rows = cur.fetchall()
    return [ParentIngredient(row) for row in rows]


def get_ingredient_weights():
    """get the current list of ingredients/weights that can be selected"""
    # TODO change the name/docstring of this function
    # FIXME refactoring replaces this
    display_dict = {}
    for key, value in ingredient_weightings.items():
        display_dict[key] = int(mean(value))
    return display_dict


def get_selected_ingredient_list():
    """get the current list of ingredients that have been selected"""
    return api_input


def increment_ingredient_number():
    """get the next ingredient number based on the number of search terms"""
    return len(api_input) + 1


def get_available_ingredient_list():
    """get the dict of child ingredients that can currently be selected"""
    return full_selection_lookup


def update_data_post_selection(par_pk):
    """given a ChildIngredient instance, moves ingredient from the
    ingredient_weightings dictionary to the selected_ingredients list
    """
    try:
        del ingredient_weightings[par_pk]
        selected_ingredient_pks.append(par_pk)
    except KeyError:
        selected_ingredient_pks.append(par_pk)


class ParentIngredient:
    """TODO docstring"""
    def __init__(self, row={}, pk=''):
        if pk:
            self._set_from_credentials(pk)
        else:
            self._set_from_row(row)


    def _set_from_credentials(self, pk):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM parent_ingredients 
                WHERE pk = ?; """
            cur.execute(SQL, (pk,))
            row = cur.fetchone()
        if row:
            self._set_from_row(row)
        else:
            self._set_from_row({})
        if api_input == []:
                api_input.append([self.pk, self.search_term])


    def _set_from_row(self, row):
        """iterate through sqlite3 row object and set all 
        key:value pairings as attributes of the class instance
        """
        row = dict(row)
        for key, value in row.items():
            setattr(self, key, value)
        # FIXME the two lines below this
        # self.pk = row.get('pk')        # self.name = row.get('name')        # self.season = row.get('season')        # self.taste = row.get('taste')        # self.function = row.get('function')        # self.botanical_relatives = row.get('botanical_relatives')        # self.weight = row.get('weight')        # self.volume = row.get('volume')        # self.techniques = row.get('techniques')        # self.tips = row.get('tips')        # self.search_term = row.get('search_term')


    def get_children(self):
        """get the list of paired ingredients for the parent"""
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM child_ingredients 
                WHERE pairing_pk = ? ORDER BY pairing_strength DESC; """
            cur.execute(SQL, (self.pk,))
            rows = cur.fetchall()
            # maintain list of all available pks for future selections
            next_selection_index = len(full_selection)
            full_selection.append([])
            for row in rows:
                full_selection[next_selection_index].append(ChildIngredient(row))
        return [ChildIngredient(row) for row in rows]


    def update_weightings(self, list_latest_children, ingred_number):
        """update the 'ingredient_weightings' dictionary by appending new
        values to existing value lists or inserting new key:value pair(s).
        Averages in the case that populating the weighting dict returns
        more values than expected and then adds 0 values where previously
        existing dict keys did not appear in the latest child ingredient
        """
        # add values from latest child list
        self.populate_weight_dict(list_latest_children, ingred_number)
        # check added values for duplicates
        self.average_duplicate_parent_pks(ingred_number)
        # add 0's for values not in latest child list
        self.populate_missing_ingredients(ingred_number)


    def populate_weight_dict(self, list_latest_children, ingred_number):
        """update the 'ingredient_weightings' dictionary by appending new
        values to existing value lists or inserting new key:value pair(s)
        """
        for child_ingredient in list_latest_children:
            par_pk = child_ingredient.get_column_from_child('own_parent_pk')
            p_str = child_ingredient.get_column_from_child('pairing_strength')
            # if the ingredient has not previously been selected
            if par_pk not in selected_ingredient_pks:
                # if key already exists in dict
                if par_pk in ingredient_weightings:
                    cur_val_list = ingredient_weightings[par_pk]
                    # if all list values are already populated
                    if len(cur_val_list) == ingred_number - 1:
                        cur_val_list.append(p_str)
                    else:
                        # add 0 values to value list if missing any
                        while len(cur_val_list) < ingred_number - 1:
                            cur_val_list.append(0)
                        cur_val_list.append(p_str)
                # if key DNE, add 0 values until n - 1 and then add pair strength
                else:
                    value_list = []
                    for i in range(ingred_number - 1):
                        value_list.append(0)
                    value_list.append(p_str)
                    ingredient_weightings[par_pk] = value_list


    def average_duplicate_parent_pks(self, ingred_number):
        """if there are duplicate values for own_parent_pk
        in the latest child list, average the scores"""
        for weights in ingredient_weightings.values():
            size = len(weights)
            # only run if there are more ingredients than expected
            if size > ingred_number:
                # TODO switch this to pop, mean, append
                temp_value_list = []
                # create a list of all of the values to be averaged
                for i in range(ingred_number - 1, size):
                    temp_value_list.append(weights[i])
                average_value = mean(temp_value_list)
                # remove all extra values
                del weights[ingred_number:size + 1]
                # reassign the last value to the calculated average
                weights[-1] = average_value


    def populate_missing_ingredients(self, ingred_number):
        """add 0's to lists where ingredient was not listed as a pairing"""
        for value in ingredient_weightings.values():
            while len(value) < ingred_number:
                value.append(0)


    def __bool__(self):
        return bool(self.pk)


    def __repr__(self):
        output = f'{self.pk}) {self.name}'
        if self.season:
            output += f' | Season: {self.season}'
        if self.taste:
            output += f' | Taste: {self.taste}'
        if self.function:
            output += f' | Function: {self.function}'
        if self.botanical_relatives:
            output += f' | Botanical Relatives: {self.botanical_relatives}'
        if self.weight:
            output += f' | Weight: {self.weight}'
        if self.volume:
            output += f' | Volume: {self.volume}'
        if self.techniques:
            output += f' | Techniques: {self.techniques}'
        if self.tips:
            output += f' | Tips: {self.tips}'
        return output

        
        


class ChildIngredient:
    """TODO docstring"""
    def __init__(self, row={}, pk=''):
        if pk:
            self._set_from_credentials(pk)
        else:
            self._set_from_row(row)


    def _set_from_credentials(self, pk):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM child_ingredients 
                WHERE pk = ?; """
            cur.execute(SQL, (pk,))
            row = cur.fetchone()
        if row:
            self._set_from_row(row)
        else:
            self._set_from_row({})


    def _set_from_row(self, row):
        """iterate through sqlite3 row object and set all 
        key:value pairings as attributes of the class instance
        """
        row = dict(row)
        for key, value in row.items():
            setattr(self, key, value)
        # self.pk = row.get('pk')        # self.name = row.get('name')        # self.pairing_strength = row.get('pairing_strength')        # self.search_term = row.get('search_term')        # self.pairing_pk = row.get('pairing_pk')        # self.own_parent_pk = row.get('own_parent_pk')


    def get_parent(self):
        """return an instance of the ParentIngredient class for the current
        child ingredient's own_parent_pk column and append the search term to
        the list for the api call
        """
        api_search_term = self.get_column_from_child('search_term')
        api_search_pk = self.get_column_from_child('own_parent_pk')
        api_input.append([api_search_pk, api_search_term])
        with OpenCursor() as cur:
            SQL = """ SELECT * from parent_ingredients WHERE pk = ?; """
            cur.execute(SQL, (self.own_parent_pk,))
            row = cur.fetchone()
        return ParentIngredient(row)


    def get_column_from_child(self, column):
        """return the value of child ingredient's column given the col name"""
        with OpenCursor() as cur:
            SQL = """ SELECT * from child_ingredients WHERE pk = ?; """
            cur.execute(SQL, (self.pk,))
            row = cur.fetchone()
        return row[column]


    def __bool__(self):
        return bool(self.pk)


    def __repr__(self):
        output = "Name: {}, Strength: {}"
        return output.format(self.name, self.pairing_strength)
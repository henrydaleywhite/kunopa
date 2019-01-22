from statistics import mean

import opencursor
from opencursor import OpenCursor

# dictionary that will be used to store ingredient pairing info
ingredient_weightings = {}
# list that will store the pk of ingredients on
# the parent table that have been already selected
selected_ingredient_pks = []
api_input = []
ingredient_number = 1


def get_base_ingredient_list():
    """function to be run to generate list of parents to be selected for
    first ingredient. Returns a list of ParentIngredient class instances
    """
    with OpenCursor() as cur:
        SQL = """ SELECT * from parent_ingredients"""
        cur.execute(SQL)
        rows = cur.fetchall()
    return [ParentIngredient(row) for row in rows]


def get_current_ingredient_list():
    """get the current list of ingredients that can be selected
    with their respective pairing/recommendation scores
    """
    display_dict = {}
    for key, value in ingredient_weightings.items():
        display_dict[key] = mean(value)
    return display_dict


class ParentIngredient:
    """TODO docstring"""
    def __init__(self, row={}, name=''):
        if name:
            self._set_from_credentials(name)
        else:
            self._set_from_row(row)


    def _set_from_credentials(self, name):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM parent_ingredients 
                WHERE name = ?; """
            cur.execute(SQL, (name,))
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
        # self.pk = row.get('pk')        # self.name = row.get('name')        # self.season = row.get('season')        # self.taste = row.get('taste')        # self.function = row.get('function')        # self.botanical_relatives = row.get('botanical_relatives')        # self.weight = row.get('weight')        # self.volume = row.get('volume')        # self.techniques = row.get('techniques')        # self.tips = row.get('tips')        # self.search_term = row.get('search_term')


    def get_children(self):
        """get the list of paired ingredients for the parent"""
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM child_ingredients 
                WHERE pairing_pk = ? ORDER BY pairing_strength DESC; """
            cur.execute(SQL, (self.pk,))
            rows = cur.fetchall()
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


    def update_data_post_selection(self, child_instance):
        """given a ChildIngredient instance, moves ingredient from the
        ingredient_weightings dictionary to the selected_ingredients list
        """
        par_pk = child_instance.get_column_from_child('own_parent_pk')
        del ingredient_weightings[par_pk]
        selected_ingredient_pks.append(par_pk)


    def __bool__(self):
        return bool(self.pk)


    def __repr__(self):
        output = "PK: {}, Name: {}"
        return output.format(self.pk, self.name)



class ChildIngredient:
    """TODO docstring"""
    def __init__(self, row={}, name=''):
        if name:
            self._set_from_credentials(name)
        else:
            self._set_from_row(row)


    def _set_from_credentials(self, name):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM child_ingredients 
                WHERE name = ?; """
            cur.execute(SQL, (name,))
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
        api_input.append(api_search_term)
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
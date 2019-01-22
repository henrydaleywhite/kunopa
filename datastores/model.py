import opencursor
from opencursor import OpenCursor

# dictionary that will be used to store ingredient pairing info
ingredient_weightings = {}

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
        key:value pairings as attributes of the class instance"""
        row = dict(row)
        for key, value in row.items():
            setattr(self, key, value)
        # self.pk = row.get('pk')        # self.name = row.get('name')        # self.season = row.get('season')        # self.taste = row.get('taste')        # self.function = row.get('function')        # self.botanical_relatives = row.get('botanical_relatives')        # self.weight = row.get('weight')        # self.volume = row.get('volume')        # self.techniques = row.get('techniques')        # self.tips = row.get('tips')        # self.search_term = row.get('search_term')


    def get_children_of_parent(self):
        """get the list of paired ingredients for the parent"""
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM child_ingredients 
                WHERE pairing_pk = ? ORDER BY pairing_strength DESC; """
            cur.execute(SQL, (self.pk,))
            rows = cur.fetchall()
        return [ChildIngredient(row) for row in rows]


    def update_weightings(self, list_latest_children, ingred_number):
        """update the 'ingredient_weightings' dictionary by appending new
        values to existing value lists or inserting new key:value pair(s)"""
        for child_ingredient in list_latest_children:
            parent_pk = child_ingredient.get_column_for_child('own_parent_pk')
            p_str = child_ingredient.get_column_for_child('pairing_strength')
            if parent_pk in ingredient_weightings:
                ingredient_weightings[parent_pk].append(p_str)
            else:
                value_list = []
                for i in range(ingred_number - 1):
                    value_list.append(0)
                value_list.append(p_str)
                ingredient_weightings[parent_pk] = value_list


    def __bool__(self):
        return bool(self.pk)


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
        key:value pairings as attributes of the class instance"""
        row = dict(row)
        for key, value in row.items():
            setattr(self, key, value)
        # self.pk = row.get('pk')        # self.name = row.get('name')        # self.pairing_strength = row.get('pairing_strength')        # self.search_term = row.get('search_term')        # self.pairing_pk = row.get('pairing_pk')        # self.own_parent_pk = row.get('own_parent_pk')


    def get_parent_for_child(self):
        """return an instance of the ParentIngredient class for the current
        child ingredient's own_parent_pk column"""
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
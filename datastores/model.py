import opencursor
from opencursor import OpenCursor


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
        row = dict(row)
        for key, value in row.items():
            setattr(self, key, value)
        # self.pk = row.get('pk')        # self.name = row.get('name')        # self.season = row.get('season')        # self.taste = row.get('taste')        # self.function = row.get('function')        # self.botanical_relatives = row.get('botanical_relatives')        # self.weight = row.get('weight')        # self.volume = row.get('volume')        # self.techniques = row.get('techniques')        # self.tips = row.get('tips')        # self.search_term = row.get('search_term')

    def get_children_of_parent(self):
        """get the list of paired ingredients for the parent"""
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM child_ingredients 
                WHERE pairing_pk = ? ORDER BY pairing_strength; """
            cur.execute(SQL, (self.pk,))
            rows = cur.fetchall()
        return [ChildIngredient(row) for row in rows]

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
        row = dict(row)
        for key, value in row.items():
            setattr(self, key, value)
        # self.pk = row.get('pk')        # self.name = row.get('name')        # self.pairing_strength = row.get('pairing_strength')        # self.search_term = row.get('search_term')        # self.pairing_pk = row.get('pairing_pk')        # self.own_parent_pk = row.get('own_parent_pk')
        
    def get_parent_for_child(self):
        with OpenCursor() as cur:
            SQL = """ SELECT * from parent_ingredients WHERE pk = ?; """
            cur.execute(SQL, (self.own_parent_pk,))
            row = cur.fetchone()
        return ParentIngredient(row)

    def __bool__(self):
        return bool(self.pk)

    def __repr__(self):
        output = "Name: {}, Strength: {}"
        return output.format(self.name, self.pairing_strength)
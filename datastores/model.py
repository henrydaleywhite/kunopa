import opencursor
from opencursor import OpenCursor


class ParentIngredient:
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
        self.pk = row.get('pk')
        self.name = row.get('name')
        self.season = row.get('season')
        self.taste = row.get('taste')
        self.function = row.get('function')
        self.botanical_relatives = row.get('botanical_relatives')
        self.weight = row.get('weight')
        self.volume = row.get('volume')
        self.techniques = row.get('techniques')
        self.tips = row.get('tips')
        self.search_term = row.get('search_term')

class ChildIngredient:
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
        self.pk = row.get('pk')
        self.name = row.get('name')
        self.season = row.get('season')
        self.taste = row.get('taste')
        self.function = row.get('function')
        self.botanical_relatives = row.get('botanical_relatives')
        self.weight = row.get('weight')
        self.volume = row.get('volume')
        self.techniques = row.get('techniques')
        self.tips = row.get('tips')
        self.search_term = row.get('search_term')


# TODO write select to pull children based on parent
# SELECT * FROM child_ingredients WHERE pk = ?
# cur.execute(SQL, (self.pk,))
# TODO write select to pull parent based on selected child
# SELECT * from parent_ingredients WHERE pk = ?
# cur.execute(SQL, (self.own_parent_pk,))
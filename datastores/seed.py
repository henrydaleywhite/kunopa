import sqlite3


import data_parsing as parse

full_file = "output.json"

def run(dbname="flavor_bible.db"):
    conn = sqlite3.connect(dbname)
    cur  = conn.cursor()

    PARENT_SQL = """INSERT INTO parent_ingredients (
                name, 
                season,
                taste,
                function,
                botanical_relatives,
                weight,
                volume,
                techniques,
                tips,
                search_term
            ) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?); """

    CHILD_SQL = """ INSERT INTO child_ingredients (
                name,
                pairing_strength,
                search_term,
                pairing_pk,
                self_pk
            )
                VALUES (?, ?, ?, ?, ?); """


    MAP_SQL = """SELECT pk FROM parent_ingredients WHERE name = ?;"""

    UPDATE_MAP_SQL = """UPDATE child_ingredients 
                    SET self_pk = ? WHERE name = ?;"""

    # importing the raw data json file created through a scrape of TFB html
    dcty = parse.load_dictionary(full_file)
    # returns list of lists with parent ingredient and search term
    pre_prune_parents = parse.impt_iter_from_delim_txt('pruned_parent_list.txt')
    # returns list of lists with child ingredient, 
    # self ref on the parent table, and search term
    pre_prune_children = parse.impt_iter_from_delim_txt('initial_child.txt')

    parent_search_dcty = {}
    child_search_dcty = {}
    mapping_table = {}
    unique_self_refs = set()
    i = 1

    # create a dict with parent ingredient key and search term value
    for lists in pre_prune_parents:
        parent_search_dcty[lists[0]] = lists[1]

    # create a dict with child ingredient key 
    # and a list of self ref and search term value
    for lists in pre_prune_children:
        child_search_dcty[lists[0]] = [lists[1], lists[2]]
    # create a list of all of the keys from the dictionary above
    child_search_dcty_keys = child_search_dcty.keys()

    # create a set to get unique values for child dict keys
    for key in child_search_dcty_keys:
        unique_self_refs.add(child_search_dcty[key][0])

    for key in parent_search_dcty.keys():
        # populate all values in parent_ingredients table
        par_sql_values = (key, dcty[key]['season'], dcty[key]['taste'], 
            dcty[key]['function'], dcty[key]['botanical relatives'], 
            dcty[key]['weight'], dcty[key]['volume'], 
            dcty[key]['techniques'], dcty[key]['tips'], 
            parent_search_dcty[key])
        cur.execute(PARENT_SQL, par_sql_values)

        # populate all values in child_ingredients table except self_pk
        # for each key in parent, iterate through list of dicts in child
        for child_ingred in dcty[key]['children']:
            # second layer of iteration to go through each key, val pair
            for subkey, value in child_ingred.items():
                if subkey in child_search_dcty_keys:
                    child_sql_values = (subkey, value, 
                        child_search_dcty[subkey][1], i, '')
                    cur.execute(CHILD_SQL, child_sql_values)
        
        i += 1

    # create a mapping table for self_pk column
    for item in unique_self_refs:
        cur.execute(MAP_SQL, (item,))
        result = cur.fetchone()[0]
        mapping_table[item] = result
    
    # populate self_pk on child_ingredients table using mapping table
    for key in child_search_dcty_keys:
        key_to_append = mapping_table[child_search_dcty[key][0]]
        child_search_dcty[key].append(key_to_append)
        cur.execute(UPDATE_MAP_SQL, (child_search_dcty[key][2], key))


    conn.commit()
    conn.close()

if __name__ == "__main__":
    run()
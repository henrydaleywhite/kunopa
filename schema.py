import sqlite3

CON = None
CUR = None

def setup(dbname="flavor_bible.db"):
    global CON
    global CUR
    CON = sqlite3.connect(dbname)
    CUR = CON.cursor()

def run(dbname="flavor_bible.db"):
    SQL = "DROP TABLE IF EXISTS parent_ingredients;"
    
    CUR.execute(SQL)
    
    SQL = """CREATE TABLE parent_ingredients(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR,
        season VARCHAR,
        taste VARCHAR,
        function VARCHAR,
        botanical_relatives VARCHAR,
        weight VARCHAR,
        volume VARCHAR,
        techniques VARCHAR,
        tips VARCHAR,
        search_term VARCHAR,
        CONSTRAINT unique_name UNIQUE(name)
        );"""
    
    CUR.execute(SQL)
    
    SQL = "DROP TABLE IF EXISTS child_ingredients;"
    
    CUR.execute(SQL)
    
    SQL = """CREATE TABLE child_ingredients(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR,
        pairing_strength INTEGER,
        search_term VARCHAR,
        pairing_pk INTEGER,
        own_parent_pk INTEGER,
        FOREIGN KEY(pairing_pk) REFERENCES parent_ingredients(pk),
        FOREIGN KEY(own_parent_pk) REFERENCES parent_ingredients(pk)
        );"""
    
    CUR.execute(SQL)
    
    
    CON.commit()
    CUR.close()
    CON.close()

if __name__ == "__main__":
    setup()
    run()
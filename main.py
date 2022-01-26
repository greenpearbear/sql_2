import sqlite3


def database_select(sqlite_query, name_database, params):
    if params == 0:
        con = sqlite3.connect(f"{name_database}.db")
        cur = con.cursor()
        cur.execute(sqlite_query)
        data_return = cur.fetchall()
        con.close()
    else:
        con = sqlite3.connect(f"{name_database}.db")
        cur = con.cursor()
        cur.execute(sqlite_query, params)
        data_return = cur.fetchall()
        con.close()
    return data_return


def database_insert(sqlite_query, name_database, params):
    con = sqlite3.connect(f"{name_database}.db")
    cur = con.cursor()
    if params != 0:
        for i in params:
            cur.execute(sqlite_query, i)
            con.commit()
    else:
        cur.executescript(sqlite_query)
    con.close()


def create_database():
    query = """
    CREATE TABLE IF NOT EXISTS age(
    id_age_table INTEGER PRIMARY KEY AUTOINCREMENT,
    age_upon_outcome TEXT
    );
    CREATE TABLE IF NOT EXISTS type(
    id_type_table INTEGER PRIMARY KEY AUTOINCREMENT,
    animal_type TEXT
    );
    CREATE TABLE IF NOT EXISTS name(
    id_name_table INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT DEFAULT 'NoName'
    );
    CREATE TABLE IF NOT EXISTS appearance(
    id_appearance_table INTEGER PRIMARY KEY AUTOINCREMENT,
    breed TEXT,
    color1 TEXT,
    color2 TEXT
    );
    CREATE TABLE IF NOT EXISTS date_of_birth(
    id_date_of_birth_table INTEGER PRIMARY KEY AUTOINCREMENT,
    date_of_birth TEXT
    );
    CREATE TABLE IF NOT EXISTS program(
    id_program_table INTEGER PRIMARY KEY AUTOINCREMENT,
    outcome_subtype TEXT DEFAULT 'NoProgram'
    );
    CREATE TABLE IF NOT EXISTS what_now(
    id_what_now_table INTEGER PRIMARY KEY AUTOINCREMENT,
    outcome_type TEXT DEFAULT 'Unknown'
    );
    CREATE TABLE IF NOT EXISTS date_input(
    id_date_input_table INTEGER PRIMARY KEY AUTOINCREMENT,
    outcome_month TEXT,
    outcome_year TEXT
    );
    CREATE TABLE IF NOT EXISTS animals_new(
    id_animals INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    id_age INTEGER,
    id_type INTEGER,
    id_name INTEGER,
    id_appearance INTEGER,
    id_date_of_birth INTEGER,
    id_program INTEGER,
    id_what_now INTEGER,
    id_date_input INTEGER,
    FOREIGN KEY (id_age) REFERENCES age (id_age_table) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (id_type) REFERENCES type (id_type_table)ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (id_name) REFERENCES name (id_name_table)ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (id_appearance) REFERENCES appearance (id_appearance_table)ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (id_date_of_birth) REFERENCES date_of_birth (id_date_of_birth_table)ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (id_program) REFERENCES program (id_program_table)ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (id_what_now) REFERENCES what_now (id_what_now_table)ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (id_date_input) REFERENCES date_input (id_date_input_table)ON DELETE SET NULL ON UPDATE CASCADE
    );
    """
    database_insert(query, 'animals_new', 0)


def drop_database():
    query = """
    DROP TABLE animals_new;
    DROP TABLE age;
    DROP TABLE appearance;
    DROP TABLE date_input;
    DROP TABLE date_of_birth;
    DROP TABLE name;
    DROP TABLE program;
    DROP TABLE type;
    DROP TABLE what_now;
    """
    database_insert(query, 'animals_new', 0)


def super_insert_database_func():
    dict_create_query = {
        'age': ('age_upon_outcome',),
        'type': ('animal_type',),
        'name': ('name',),
        'appearance': ('breed', 'color1', 'color2'),
        'date_of_birth': ('date_of_birth',),
        'program': ('outcome_subtype',),
        'what_now': ('outcome_type',),
        'date_input': ('outcome_year', 'outcome_month')
    }
    new_list = []
    for key, value in dict_create_query.items():
        query = f"""SELECT DISTINCT {','.join(value)} FROM animals ORDER BY {','.join(value)}"""
        list_sql = database_select(query, 'animal', 0)
        query = f"""
        INSERT INTO {key} ({','.join(value)})
        values ({','.join(['?']*len(value))})"""
        database_insert(query, 'animals_new', list_sql)


create_database()
#drop_database()
super_insert_database_func()

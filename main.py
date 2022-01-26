import sqlite3


def database_no_params(sqlite_query):
    con = sqlite3.connect("animal.db")
    cur = con.cursor()
    cur.execute(sqlite_query)
    data_return = cur.fetchall()
    con.close()
    return data_return


def database_params(sqlite_query, name_table, params):
    con = sqlite3.connect(f"{name_table}.db")
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
    CREATE TABLE animals_new(
    id_animals INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    id_age INTEGER,
    id_type INTEGER,
    id_name INTEGER,
    id_appearance INTEGER,
    id_date_of_birth INTEGER,
    id_program INTEGER,
    id_what_now INTEGER,
    id_date_input INTEGER);
    CREATE TABLE age(
    id_age_table INTEGER PRIMARY KEY AUTOINCREMENT,
    age_upon_outcome TEXT,
    FOREIGN KEY (id_age_table) REFERENCES animals_new (id_age));
    CREATE TABLE type(
    id_type_table INTEGER PRIMARY KEY AUTOINCREMENT,
    animal_type TEXT,
    FOREIGN KEY (id_type_table) REFERENCES animals_new (id_type));
    CREATE TABLE name(
    id_name_table INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT DEFAULT 'NoName',
    FOREIGN KEY (id_name_table) REFERENCES animals_new (id_name));
    CREATE TABLE appearance(
    id_appearance_table INTEGER PRIMARY KEY AUTOINCREMENT,
    breed TEXT,
    color1 TEXT,
    color2 TEXT,
    FOREIGN KEY (id_appearance_table) REFERENCES animals_new (id_appearance));
    CREATE TABLE date_of_birth(
    id_date_of_birth_table INTEGER PRIMARY KEY AUTOINCREMENT,
    date_of_birth TEXT,
    FOREIGN KEY (id_date_of_birth_table) REFERENCES animals_new (id_date_of_birth));
    CREATE TABLE program(
    id_program_table INTEGER PRIMARY KEY AUTOINCREMENT,
    outcome_subtype TEXT DEFAULT 'NoProgram',
    FOREIGN KEY (id_program_table) REFERENCES animals_new (id_program));
    CREATE TABLE what_now(
    id_what_now_table INTEGER PRIMARY KEY AUTOINCREMENT,
    outcome_type TEXT DEFAULT 'Unknown',
    FOREIGN KEY (id_what_now_table) REFERENCES animals_new (id_what_now));
    CREATE TABLE date_input(
    id_date_input_table INTEGER PRIMARY KEY AUTOINCREMENT,
    outcome_month TEXT,
    outcome_year TEXT,
    FOREIGN KEY (id_date_input_table) REFERENCES animals_new (id_date_input));
    """
    database_params(query, 'animals_new', 0)


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
    database_params(query, 'animals_new', 0)


def super_func():
    dict_column_and_dict = {'age': ['age_upon_outcome'],
                            'type': ['animal_type'],
                            'name': ['name'],
                            'appearance': ['breed', 'color1', 'color2'],
                            'date_of_birth': ['date_of_birth'],
                            'program': ['outcome_subtype'],
                            'what_now': ['outcome_type'],
                            'date_input': ['outcome_year', 'outcome_month']}
    super_insert_database_func(dict_column_and_dict)


def super_insert_database_func(dict_create_query):
    for key, value in dict_create_query.items():
        query = f"""SELECT DISTINCT {','.join(value)} FROM animals ORDER BY {','.join(value)}"""
        list_sql = database_no_params(query)
        query = f"""
        INSERT INTO {key} ({','.join(value)})
        values ({','.join(['?']*len(value))})"""
        database_params(query, 'animals_new', list_sql)


create_database()
#drop_database()
super_func()

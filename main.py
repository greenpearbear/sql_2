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
    age TEXT,
    FOREIGN KEY (id_age_table) REFERENCES animals_new (id_age));
    CREATE TABLE type(
    id_type_table INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
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
    program TEXT DEFAULT 'NoProgram',
    FOREIGN KEY (id_program_table) REFERENCES animals_new (id_program));
    CREATE TABLE what_now(
    id_what_now_table INTEGER PRIMARY KEY AUTOINCREMENT,
    what_now TEXT DEFAULT 'Unknown',
    FOREIGN KEY (id_what_now_table) REFERENCES animals_new (id_what_now));
    CREATE TABLE date_input(
    id_date_input_table INTEGER PRIMARY KEY AUTOINCREMENT,
    date_input_month TEXT,
    date_input_year TEXT,
    FOREIGN KEY (id_date_input_table) REFERENCES animals_new (id_date_input));
    """
    database_params(query, 'animals_new', 0)


def insert_age():
    query = """SELECT DISTINCT age_upon_outcome FROM animals ORDER BY age_upon_outcome"""
    list_sql = database_no_params(query)
    query = """
    INSERT INTO age (age)
    values (?)"""
    database_params(query, 'animals_new', list_sql)


def insert_type():
    query = """SELECT DISTINCT animal_type FROM animals ORDER BY animal_type"""
    list_sql = database_no_params(query)
    query = """
    INSERT INTO type (type)
    values (?)"""
    database_params(query, 'animals_new', list_sql)


def insert_name():
    query = """SELECT DISTINCT name FROM animals ORDER BY name"""
    list_sql = database_no_params(query)
    query = '''
    INSERT INTO name (name)
    values (?)'''
    database_params(query, 'animals_new', list_sql)


def insert_appearance():
    query = """SELECT DISTINCT breed, color1, color2 FROM animals ORDER BY name"""
    list_sql = database_no_params(query)
    query = """
    INSERT INTO appearance (breed, color1, color2)
    values (?,?,?)"""
    database_params(query, 'animals_new', list_sql)


def insert_date_of_birth():
    query = """SELECT DISTINCT date_of_birth FROM animals ORDER BY date_of_birth"""
    list_sql = database_no_params(query)
    query = """
    INSERT INTO date_of_birth (date_of_birth)
    values (?)"""
    database_params(query, 'animals_new', list_sql)


def insert_program():
    query = """SELECT DISTINCT outcome_subtype FROM animals ORDER BY outcome_subtype"""
    list_sql = database_no_params(query)
    query = """
    INSERT INTO program (program)
    values (?)"""
    database_params(query, 'animals_new', list_sql)


def insert_what_now():
    query = """SELECT DISTINCT outcome_type FROM animals ORDER BY outcome_type"""
    list_sql = database_no_params(query)
    query = """
    INSERT INTO what_now (what_now)
    values (?)"""
    database_params(query, 'animals_new', list_sql)


def insert_date_input():
    query = """SELECT DISTINCT outcome_month,outcome_year FROM animals ORDER BY outcome_year"""
    list_sql = database_no_params(query)
    query = """
    INSERT INTO date_input (date_input_month, date_input_year)
    values (?,?)"""
    database_params(query, 'animals_new', list_sql)


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


def my_prog():
    create_database()
    insert_age()
    insert_type()
    insert_name()
    insert_appearance()
    insert_date_of_birth()
    insert_program()
    insert_what_now()
    insert_date_input()


# my_prog()
# drop_database()

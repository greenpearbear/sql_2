import sqlite3


def database_select(sqlite_query, params):
    if params == 0:
        con = sqlite3.connect("animal.db")
        cur = con.cursor()
        cur.execute(sqlite_query)
        data_return = cur.fetchall()
        con.close()
    else:
        con = sqlite3.connect(f"animal.db")
        cur = con.cursor()
        cur.execute(sqlite_query, params)
        data_return = cur.fetchall()
        con.close()
    return data_return


def database_insert(sqlite_query, params):
    con = sqlite3.connect(f"animal.db")
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
    CREATE TABLE IF NOT EXISTS animal_color_all_color
(
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    color VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS animal_age
(
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    age VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS animal_type
(
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    type VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS animal_name
(
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    name VARCHAR(100) DEFAULT 'NoName'
);

CREATE TABLE IF NOT EXISTS animal_breed
(
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    breed VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS animal_color
(
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    id_color_1 INTEGER,
    id_color_2 INTEGER,
    FOREIGN KEY (id_color_1) REFERENCES animal_color_all_color(id),
    FOREIGN KEY (id_color_2) REFERENCES animal_color_all_color(id)
);

CREATE TABLE IF NOT EXISTS animal_date_of_birth
(
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    date_of_birth VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS animal_program
(
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    program VARCHAR(50) DEFAULT 'NoProgram'
);

CREATE TABLE IF NOT EXISTS animal_where_now
(
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    where_now VARCHAR(50) DEFAULT 'Unknown'
);

CREATE TABLE IF NOT EXISTS animal_new_month_departure
(
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    month INTEGER
);

CREATE TABLE IF NOT EXISTS animal_new_year_departure
(
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    year INTEGER
);

CREATE TABLE IF NOT EXISTS animal_new
(
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    id_age INTEGER,
    id_type INTEGER,
    id_name INTEGER,
    id_breed INTEGER,
    id_color INTEGER,
    id_date_of_birth INTEGER,
    id_program INTEGER,
    id_where_now INTEGER,
    id_month_departure INTEGER,
    id_year_departure INTEGER,
    FOREIGN KEY (id_year_departure) REFERENCES animal_new_year_departure(id),
    FOREIGN KEY (id_month_departure) REFERENCES animal_new_month_departure(id),
    FOREIGN KEY (id_where_now) REFERENCES animal_where_now(id),
    FOREIGN KEY (id_program) REFERENCES animal_program(id),
    FOREIGN KEY (id_date_of_birth) REFERENCES animal_date_of_birth(id),
    FOREIGN KEY (id_color) REFERENCES animal_color(id),
    FOREIGN KEY (id_breed) REFERENCES animal_breed(id),
    FOREIGN KEY (id_name) REFERENCES animal_name(id),
    FOREIGN KEY (id_type) REFERENCES animal_type(id),
    FOREIGN KEY (id_age) REFERENCES animal_age(id)
);
"""
    database_insert(query, 0)


def insert_no_main_tables():
    query = """
INSERT INTO animal_age (age)
SELECT DISTINCT age_upon_outcome FROM animals;

INSERT INTO animal_breed (breed)
SELECT DISTINCT breed FROM animals;

INSERT INTO animal_color_all_color (color)
SELECT DISTINCT trim(color1) as color_result FROM animals
UNION
SELECT DISTINCT trim(color2) as color_result FROM animals;

INSERT INTO animal_color (id_color_1, id_color_2)
SELECT DISTINCT trim(color1), trim(color2)
FROM animals;

INSERT INTO animal_date_of_birth (date_of_birth)
SELECT DISTINCT date_of_birth FROM animals;

INSERT INTO animal_name (name)
SELECT DISTINCT name FROM animals;

INSERT INTO animal_new_month_departure (month)
SELECT DISTINCT outcome_month FROM animals;

INSERT INTO animal_new_year_departure (year)
SELECT DISTINCT outcome_year FROM animals;

INSERT INTO animal_program (program)
SELECT DISTINCT outcome_subtype FROM animals;

INSERT INTO animal_type (type)
SELECT DISTINCT animal_type FROM animals;

INSERT INTO animal_where_now (where_now)
SELECT DISTINCT outcome_type FROM animals;
    """
    database_insert(query, 0)


def insert_main_table():
    query = """
    SELECT age_upon_outcome, animal_type, name, breed, color1, color2,
    date_of_birth, outcome_subtype, outcome_type, outcome_month, outcome_year 
    FROM animals LIMIT 1"""
    database_select(query, 0)


def update_table():
    query = """
    UPDATE animal_color
    SET id_color_1 = (SELECT id FROM animal_color_all_color WHERE id_color_1 = color),
        id_color_2 = (SELECT id FROM animal_color_all_color WHERE id_color_2 = color);"""
    database_insert(query, 0)


def drop_database():
    query = """
    DROP TABLE animal_new;
    DROP TABLE animal_age;
    DROP TABLE animal_breed;
    DROP TABLE animal_color;
    DROP TABLE animal_color_all_color;
    DROP TABLE animal_name;
    DROP TABLE animal_new_month_departure;
    DROP TABLE animal_new_year_departure;
    DROP TABLE animal_where_now;
    DROP TABLE animal_program;
    DROP TABLE animal_type;
    DROP TABLE animal_date_of_birth;
    """
    database_insert(query, 0)


create_database()
#drop_database()
insert_no_main_tables()
insert_main_table()
update_table()
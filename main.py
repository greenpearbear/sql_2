import sqlite3
from flask import Flask


app = Flask(__name__)


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
    id_color_1 INTEGER,
    id_color_2 INTEGER,
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
    FOREIGN KEY (id_color_1) REFERENCES animal_color_all_color(id),
    FOREIGN KEY (id_color_2) REFERENCES animal_color_all_color(id),
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
    INSERT INTO animal_new (id_age, id_type, id_name, id_breed, id_date_of_birth, 
    id_program, id_where_now, id_month_departure, id_year_departure, id_color_1, id_color_2)
    SELECT age_upon_outcome, animal_type, name, breed, date_of_birth, 
    outcome_subtype, outcome_type, outcome_month, outcome_year, color1, color2 
    FROM animals;
    """
    database_insert(query, 0)
    query = """
    UPDATE animal_new
    SET id_age = (SELECT id FROM animal_age WHERE id_age = age),
        id_type = (SELECT id FROM animal_type WHERE id_type = type),
        id_name = (SELECT id FROM animal_name WHERE id_name = name),
        id_breed = (SELECT id FROM animal_breed WHERE id_breed= breed),
        id_date_of_birth = (SELECT id FROM animal_date_of_birth WHERE id_date_of_birth = date_of_birth),
        id_program = (SELECT id FROM animal_program WHERE id_program = program),
        id_where_now = (SELECT id FROM animal_where_now WHERE id_where_now = where_now),
        id_month_departure = (SELECT id FROM animal_new_month_departure WHERE id_month_departure = month),
        id_year_departure = (SELECT id FROM animal_new_year_departure WHERE id_year_departure = year),
        id_color_1 = (SELECT id FROM animal_color_all_color WHERE id_color_1 = color),
        id_color_2 = (SELECT id FROM animal_color_all_color WHERE id_color_2 = color);"""
    database_insert(query, 0)


def drop_database():
    query = """
    DROP TABLE animal_new;
    DROP TABLE animal_age;
    DROP TABLE animal_breed;
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


def save_func():
    create_database()
    insert_no_main_tables()
    insert_main_table()
    #drop_database()


@app.route('/id/<uid>')
def return_data_from_database(uid):
    uid = int(uid)
    query = f"""
    SELECT age, breed, date_of_birth, name, month, year, program, type, where_now, color FROM animal_new
    LEFT JOIN animal_age aa on aa.id = animal_new.id_age
    LEFT JOIN animal_breed ab on ab.id = animal_new.id_breed
    LEFT JOIN animal_date_of_birth adob on adob.id = animal_new.id_date_of_birth
    LEFT JOIN animal_name an on animal_new.id_name = an.id
    LEFT JOIN animal_new_month_departure anmd on animal_new.id_month_departure = anmd.id
    LEFT JOIN animal_new_year_departure anyd on animal_new.id_year_departure = anyd.id
    LEFT JOIN animal_program ap on animal_new.id_program = ap.id
    LEFT JOIN animal_type at on animal_new.id_type = at.id
    LEFT JOIN animal_where_now awn on animal_new.id_where_now = awn.id
    LEFT JOIN animal_color_all_color on animal_new.id_color_1 = animal_color_all_color.id
    WHERE animal_new.id = {uid}
    ;
    """
    data_return = database_select(query, 0)
    return str(data_return)


#save_func()

if __name__ == '__main__':
    app.run()
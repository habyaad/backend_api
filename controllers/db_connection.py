import sqlite3

def create_db():
    conn = sqlite3.connect("users.sqlite")
    cursor = conn.cursor()

    sql_query = """CREATE TABLE user(
        id integer PRIMARY KEY, 
        first_name text NOT NULL, 
        email text NOT NULL UNIQUE, 
        password VARCHAR(512) NOT NULL,
        public_id text NOT NULL
        )"""


    cursor.execute(sql_query)

create_db()
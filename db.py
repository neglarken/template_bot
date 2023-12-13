import sqlite3
from typing import List

con = sqlite3.connect('database.db')
cur = con.cursor()

def create_db():
    with con:
        con.execute("""CREATE TABLE IF NOT EXISTS user (
                        id   BIGINT NOT NULL,
                        name text   NOT NULL,
                        PRIMARY KEY (id)
                    )""")
        con.commit()

# user
def create_user(id: int, name: str):
    cur.execute('insert into user (id, name) values (?, ?) on conflict do nothing', (id, name))
    con.commit()

def get_user(user_id: int):
    return cur.execute('select * from user where id = ?', (user_id, )).fetchall()

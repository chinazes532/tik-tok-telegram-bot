import sqlite3 as sq

# Функция, которая создает бд с таблицами
async def create_db():
    print('Creating database...')

    global db, cur
    db = sq.connect('database.db')
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        username TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS sponsors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        group_id INTEGER,
        link TEXT
    )""")

    db.commit()

# Функция, которая записывает user_id и username в бд
async def insert_user(user_id, username):
    print(f'Inserting user {user_id}...')
    cur.execute("INSERT OR REPLACE INTO users VALUES(?, ?)", (user_id, username))
    db.commit()

async def insert_sponsor(name, group_id, link):
    print(f'Inserting sponsor {name}...')
    cur.execute("INSERT OR REPLACE INTO sponsors(name, group_id, link) VALUES(?, ?, ?)", (name, group_id, link))
    db.commit()

async def get_users():
    users = cur.execute("SELECT * FROM users").fetchall()
    return users

async def get_sponsors():
    sponsors = cur.execute("SELECT * FROM sponsors").fetchall()
    return sponsors

async def get_sponsor(id):
    sponsor = cur.execute("SELECT * FROM sponsors WHERE id = ?", (id,)).fetchone()
    return sponsor

async def delete_sponsor(id):
    cur.execute("DELETE FROM sponsors WHERE id = ?", (id,))
    db.commit()

async def delete_user(user_id):
    cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    db.commit()

async def user_count():
    cur.execute("SELECT COUNT(*) FROM users")
    return cur.fetchone()[0]


async def update_sponsor_link(id, link):
    cur.execute("UPDATE sponsors SET link = ? WHERE id = ?", (link, id))
    db.commit()

async def update_sponsor_group_id(id, group_id):
    cur.execute("UPDATE sponsors SET group_id = ? WHERE id = ?", (group_id, id))
    db.commit()
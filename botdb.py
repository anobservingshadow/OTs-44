# botdb.py

from databases import Database

async def open_pool(dbfile):
    database = Database(dbfile)
    await database.connect()
    return database

async def affection_check(database):
    sql = "SELECT name FROM sqlite_master WHERE type='table' AND name=:name"
    rows = await database.fetch_all(query=sql, values={"name":'affection'})
    print(rows)
    if len(rows) == 0:
        sql = """CREATE TABLE affection (userid INTEGER PRIMARY KEY, username VARCHAR(100), affection_level INTEGER, state VARCHAR(100))"""
        await database.execute(query=sql)

async def affection_inc(database,love_muffinID,love_muffin):
    userid = str(love_muffinID)
    username = str(love_muffin)
    sql = "SELECT * FROM affection WHERE userid=:id"
    rows = await database.fetch_all(query=sql,values={"id":userid})
    if len(rows) == 0:
        sql = """INSERT INTO affection(userid, username, affection_level, state) VALUES (:id, :uname, 1, Friendly)"""
        await database.execute(query=sql, values={"id":userid, "uname":username})
    elif int(rows[0][2]) == 200:
        sql = """UPDATE affection SET affection_level = :level, username = :uname, state = Friendly WHERE userid = :id"""
        await database.execute(query=sql, values={"level":"0","uname":username,"id":userid})
    else:
        affection_state = await state_change(database, int(rows[0][2])+1)
        print(affection_state)
        sql = """UPDATE affection SET affection_level = :level, username = :uname, state = :a_state WHERE userid = :id"""
        await database.execute(query=sql, values={"level":int(rows[0][2])+1,"uname":username,"a_state":affection_state,"id":userid})
    return rows

async def state_change(database, level):
    if level < 10:
        return "Friendly"
    elif 10 <= level < 100:
        return "Lovey Dovey"
    elif 100 <= level < 150:
        return "Have My Children"
    elif 150 <= level < 200:
        return "Enter Me"
    else:
        return "Unknown"

async def select_from(database, s_table):
    sql = "SELECT * FROM "+s_table
    table = await database.fetch_all(query=sql)
    return table

async def check_aff_level(database, userid):
    sql = "SELECT * FROM affection WHERE userid = :id"
    table = await database.fetch_all(query=sql, values={"id":userid})
    return table

async def close_pool(database):
    await database.disconnect()

import sqlite3
import json

db = 'data/users.db'    
conn = sqlite3.connect(db)
cursor = conn.cursor()
print("database was connected")

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    userid TEXT PRIMARY KEY,
    link TEXT,
    location TEXT,
    htmlPage TEXT,
    pagedate TEXT
)
''')

def getPagedate(userid):
    try:
        cursor.execute("SELECT pagedate FROM users WHERE userid =?", (userid,))
        result = cursor.fetchone()
        return result[0]
    except Exception as e:
        print(e)
        return False

def getPage(userid):
    try:
        cursor.execute("SELECT htmlPage FROM users WHERE userid =?", (userid,))
        result = cursor.fetchone()
        return result[0]
    except Exception as e:
        print(e)
        return False

def setPage(userid, page, pagedate):
    try:
        cursor.execute('''
        UPDATE users
        SET htmlPage = ?, pagedate = ?
        WHERE userid = ?
        ''', ( page, pagedate, userid))
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False

def checkUser(userid):
    try:
        cursor.execute("SELECT COUNT(1) FROM users WHERE userid = ?", (userid,))
        result = cursor.fetchone()[0] > 0
        return result
    except Exception as e:
        print(e)
        return False

def addUser(userid, link, location):
    try:
        location_json = json.dumps(location)
        cursor.execute('''
        INSERT INTO users (userid, link, location) VALUES (?, ?, ?)
        ''', (userid, link, location_json))
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False

def getCity(userid):
    try:
        cursor.execute("SELECT location FROM users WHERE userid =?", (userid,))
        result = cursor.fetchone()
        city = json.loads(result[0])
        return city[3]
    except Exception as e:
        print(e)
        return False
    
def getLink(userid):
    try:
        cursor.execute("SELECT link FROM users WHERE userid =?", (userid,))
        result = cursor.fetchone()
        print("res in db:  ", result)
        if result[0] is not None:
            return result[0]
        else:
            return False
    except Exception as e:
        print(e)
        return False   

def resetUser(userid):
    try:
        cursor.execute('DELETE FROM users WHERE userid = ?', (userid,))
        conn.commit()
        print("user reseted")
        return True
    except Exception as e:
        print(e)
        return False
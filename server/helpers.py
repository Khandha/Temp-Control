import json
import os.path
import sqlite3
from datetime import datetime
from pathlib import Path
import random
from sqlite3 import Error


def db_connection():
    db_os_name = Path("db/t_history.db").resolve()
    try:
        db_handle = sqlite3.connect(db_os_name)
        if not os.path.isfile(db_os_name):
            db_handle.execute('''create table temperatures(
            id INTEGER PRIMARY KEY AUTOINCREMENT, time text, room_temp real, heater_temp real, set_point real)''')
        return db_handle
    except Error as e:
        print(e)  # TODO


def db_push_temp(room_temp, heater_temp, set_point):
    db = db_connection()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.execute("insert into temperatures (time, room_temp, heater_temp, set_point) values (?, ?, ?, ?)",
               (current_time, room_temp, heater_temp, set_point))
    db.commit()


def get_latest_data():
    db = db_connection()
    last_data = {}
    cursor = db.execute("select * from temperatures where id = (select max(id) from temperatures)")
    for row in cursor:
        time_out: str = str(datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S').time())
        last_data.update({"time": time_out})
        last_data.update({"roomtemp": row[2]})
        last_data.update({"heatertemp": row[3]})
        last_data.update({"set_point": row[4]})
    db.close()
    return json.dumps(last_data)


def get_some_data(count):
    db = db_connection()
    db.row_factory = sqlite3.Row
    cur = db.cursor()

    cur.execute("select * from temperatures order by id desc limit ?", [count])
    some_data = []
    for row in cur:
        data = {}
        time_out = str(datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S').time())
        data.update({"time": time_out})
        data.update({"roomtemp": row[2]})  # random.randint(17, 19)
        data.update({"heatertemp": row[3]})
        data.update({"set_point": row[4]})
        some_data.append(data)
    db.commit()
    db.close()
    return json.dumps(some_data)


def get_three_hrs():
    db = db_connection()
    db.row_factory = sqlite3.Row
    cur = db.cursor()

    cur.execute("select * from temperatures where id % 54 == 0 order by id desc limit 200")
    some_data = []
    for row in cur:
        data = {}
        time_out = str(datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S').time())
        data.update({"time": time_out})
        data.update({"roomtemp": row[2]})
        data.update({"heatertemp": row[3]})
        data.update({"set_point": row[4]})
        some_data.append(data)
    db.commit()
    db.close()
    return json.dumps(some_data)


def get_six_hrs():
    db = db_connection()
    db.row_factory = sqlite3.Row
    cur = db.cursor()

    cur.execute("select * from temperatures where id % 108 == 0 order by id desc limit 200")
    some_data = []
    for row in cur:
        data = {}
        time_out = str(datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S').time())
        data.update({"time": time_out})
        data.update({"roomtemp": row[2]})
        data.update({"heatertemp": row[3]})
        data.update({"set_point": row[4]})
        some_data.append(data)
    db.commit()
    db.close()
    return json.dumps(some_data)

def get_twelve_hrs():
    db = db_connection()
    db.row_factory = sqlite3.Row
    cur = db.cursor()

    cur.execute("select * from temperatures where id % 216 == 0 order by id desc limit 200")
    some_data = []
    for row in cur:
        data = {}
        time_out = str(datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S').time())
        data.update({"time": time_out})
        data.update({"roomtemp": row[2]})
        data.update({"heatertemp": row[3]})
        data.update({"set_point": row[4]})
        some_data.append(data)
    db.commit()
    db.close()
    return json.dumps(some_data)


def set_new_temperature(q, new_temp):
    q.put(float(new_temp))


def limit(value, mini, maxi):
    if mini is None or maxi is None or value is None:
        return None
    else:
        return min(maxi, max(mini, value))

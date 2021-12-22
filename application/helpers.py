import json
import os.path
import sqlite3
from datetime import datetime
from decimal import Decimal
from multiprocessing import current_process
from pathlib import Path
from sqlite3 import Error


def db_connection():
    db_os_name = Path("C:\\projectspy\\Temp-Control\\application\\db\\t_history.db").resolve()  # TODO: resolve this
    # print(db_os_name)
    try:
        db_handle = sqlite3.connect(db_os_name)
        if not os.path.isfile(db_os_name):
            db_handle.execute('''create table temperatures(time real, room_temp real, heater_temp real)''')
        return db_handle
    except Error as e:
        print(e)  # TODO


def db_push_temp(room_temp, heater_temp):
    db = db_connection()
    current_time = datetime.now().strftime("%H:%M:%S")
    db.execute("insert into temperatures (time, room_temp, heater_temp) values (?, ?, ?)",
               (current_time, room_temp, heater_temp))
    db.commit()


def get_latest_data():
    db = db_connection()
    last_data = {}
    cursor = db.execute("select * from temperatures where id = (select max(id) from temperatures)")
    for row in cursor:
        last_data.update({"time": row[1]})
        last_data.update({"room-temp": row[2]})
        last_data.update({"heater-temp": row[3]})
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
        data.update({"time": row[1]})
        data.update({"room-temp": row[2]})
        data.update({"heater-temp": row[3]})
        some_data.append(data)
    db.commit()
    db.close()
    return json.dumps(some_data)


def set_new_temperature(q, new_temp):
    q.put(float(new_temp))

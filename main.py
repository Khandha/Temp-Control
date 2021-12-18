import json
import os.path
from flask import Flask, request, render_template, g
from simple_pid import PID
from multiprocessing import Process, Manager
import time
from datetime import datetime
from application.routes import *
import sqlite3
from sqlite3 import Error
import os.path
from pathlib import Path

dt = 1  # s


# redundant
# x, y, setpoint = [], [], []


def db_connection():
    db_os_name = Path("C:\\projectspy\\Temp-Control\\application\\db\\t_history.db").resolve()  #TODO: resolve this
    print(db_os_name)
    try:
        db_handle = sqlite3.connect(db_os_name)
        if not os.path.isfile(db_os_name):
            db_handle.execute('''create table temperatures(time real, room_temp real, heater_temp real)''')
        return db_handle
    except Error as e:
        print(e)  # TODO


class Room:
    def __init__(self):
        self.room_temp = 17
        self.expected_temp = 32

    def update(self, heater_power):
        if heater_power > 0:
            self.room_temp += 0.002 * heater_power * dt  # play with this value for faster / slower temp changes.
        self.room_temp -= 0.02 * dt
        return self.room_temp


def worker(room1: 'Room'):
    print("Worker is running")
    db = db_connection()
    cur = db.cursor()
    pid = PID(5, 0.1, 0.1, setpoint=room1.expected_temp)
    pid.output_limits = (0, 45)
    starttime = time.time()
    while True:
        heater = pid(room1.room_temp)
        temp = room1.update(heater)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        db.execute("insert into temperatures (time, room_temp, heater_temp) values (?, ?, ?)",
                   (current_time, temp, heater))
        db.commit()
        time.sleep(dt - ((time.time() - starttime) % dt))


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

    rows = cur.execute("select * from temperatures order by id desc limit ?", [count])
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


app = Flask(__name__)

if __name__ == "__main__":
    jobs = []
    room = Room()
    p1 = Process(target=worker, args=(room,))
    jobs.append(p1)
    p1.start()

    app.register_blueprint(page)
    print(app.url_map)
    app.run()

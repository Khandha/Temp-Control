from datetime import datetime
import time
from simple_pid import PID
from multiprocessing import Queue

from helpers import db_connection, db_push_temp, db_fetch_new_set_temp


class Engine:
    dt = 0.3  # s

    def worker(self, q, room1: 'Room'):
        print("Worker is running")
        pid = PID(5, 0.1, 0.1, setpoint=room1.expected_temp)
        pid.output_limits = (0, 45)
        start_time = time.time()
        while True:
            #  TODO: split into thread
            if not q.empty():
                new_temp = q.get()
                pid.setpoint = new_temp
                room1.expected_temp = new_temp
                print("set new temp to: ", new_temp)
            # print(room1.expected_temp)
            heater_temp = pid(room1.room_temp)
            room_temp = room1.update(heater_temp, self.dt)

            #  TODO: split into thread
            db_push_temp(room_temp, heater_temp)

            time.sleep(self.dt - ((time.time() - start_time) % self.dt))


class Room:
    def __init__(self):
        self.room_temp = 19
        self.expected_temp = 32

    def update(self, heater_power, dt):
        if heater_power > 0:
            self.room_temp += 0.002 * heater_power * dt  # play with this value for faster / slower temp changes.
        self.room_temp -= 0.02 * dt
        return self.room_temp

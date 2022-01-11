import time
from multiprocessing import Process

from PID import PID

from helpers import db_push_temp
from room import Room
# testing purposes only
# not a requirement
from bokeh.plotting import figure, show
from bokeh.io import output_file


class Engine:
    dt = 1  # s

    def __init__(self):
        self.power_max = 1600  # W
        self.power_min = 0  # W
        self.heater_temp_now = 19  # C

    def worker(self, q, room1: 'Room'):
        # simulation starting
        print("Worker is running")
        # multiply self.dt to get faster results
        
        # setting pid controller
        # Cohen-Coon method
        # https://link.springer.com/article/10.1007/s42452-019-0929-y
        pid = PID(80, 0.2, 10, set_point=room1.expected_temp)

        # setting pid limits
        pid.out_min, pid.out_max = self.power_min, self.power_max

        start_time = time.time()
        while True:
            # pulls new temp from queue
            try:
                if not q.empty():
                    new_temp = q.get()
                    pid.set_point = new_temp
                    room1.expected_temp = new_temp
                    print("set new temp to: ", new_temp)
                # calculate power to heater
                power = pid(room1.room_temp, self.dt)

                # calculate heater temperature and heat given out
                heater_temp, heat = self.heater_temp_calculate(power, room1.room_temp)

                # returns room temperature based on differential equation
                room_temp = room1(heat, self.dt)

                # saves state to database
                p1 = Process(target=db_push_temp, args=(room_temp, heater_temp))
                p1.start()

                time.sleep(self.dt - ((time.time() - start_time) % self.dt))
            except ValueError:
                print("Queue error - retrying in next run")
            except KeyboardInterrupt:
                print("Program interrupted with keyboard stop signal - P2")
                quit()

    def time_prediction(self, room, queue):
        # set controller
        pid = PID(80, 0.2, 10, set_point=room.expected_temp)
        # set limits
        pid.out_min, pid.out_max = self.power_min, self.power_max
        # counter to estimate time
        i = 0
        while True:
            i += 1

            # calculate power to heater
            power = pid(room.room_temp, self.dt)

            # calculate heater temperature and heat given out
            heater_temp, heat = self.heater_temp_calculate(power, room.room_temp)

            # calculate room temperature based on heat given out
            room_temp = room(heat, self.dt)

            # check if reached set temperature
            if round(room_temp) == room.expected_temp:
                break

        # calculate amount of iterations needed * given dt (as given dt is 1 second)
        ret_value = i * self.dt

        # send to router
        queue.put(ret_value)

    def heater_temp_calculate(self, watts, room_temp):

        if self.heater_temp_now >= 70:
            watts = 0

        # copper heat capacity: 0.385 kJ/kg, water heat capacity: 4.2 kJ/kg
        cp = 0.9 * 4.2 + 0.1 * 0.385

        # mass of heater: 15 kg
        mass = 15

        # 1 watt = 1 J/s
        # 1 kJ = 1W/s / 1000
        heat = watts * self.dt / 1000

        # Q = m * cp * dT -> dT = Q / m * cp
        # C = (kJ / s) / (kg * Kj / kg / C)
        delta_temp = heat / (mass * cp)

        # surface of heater: 0.7m*0.6m*2 + 0.3m*0.6m*2 + 0.3m*0.7m*2
        surface = 0.7 * 0.6 * 2 + 0.3 * 0.6 * 2 + 0.3 * 0.7 * 2  # m^3

        # https://www.engineeringtoolbox.com/overall-heat-transfer-coefficient-d_434.html
        coefficient = 16  # W/m^3K = J/s / m^3K

        # temperature difference
        temp_difference = self.heater_temp_now - room_temp  # C
        # print("temp difference: ", temp_difference)

        # Newton's law of cooling
        # Q = h * A * dT
        transfer_out = coefficient * surface * temp_difference / 1000  # kW

        heat_given = transfer_out * self.dt  # kJ

        temperature_given = heat_given / (mass * cp)  # C

        self.heater_temp_now += delta_temp - temperature_given

        if heat_given < 0:
            heat_given = abs(heat_given)
        return self.heater_temp_now, heat_given

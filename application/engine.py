import time

from PID import PID

from helpers import db_push_temp

# testing purposes only
# not a requirement
from bokeh.plotting import figure, show
from bokeh.io import output_file


# TODO:
#  co-processing - how to implement?


class Engine:
    dt = 1  # s

    def __init__(self):
        self.power_max = 1600  # W
        self.power_min = 0  # W
        self.heater_temp_now = 19  # C

    def worker(self, q, room1: 'Room'):
        # simulation starting
        print("Worker is running")

        # setting pid controller
        # Cohen-Coon method
        # https://link.springer.com/article/10.1007/s42452-019-0929-y
        pid = PID(3.9931, 0.4144, 2.6267, set_point=room1.expected_temp)

        # setting pid limits
        pid.out_min, pid.out_max = self.power_min, self.power_max

        start_time = time.time()
        while True:
            # TODO: split into process
            # pulls new temp from queue
            if not q.empty():
                new_temp = q.get()
                pid.setpoint = new_temp
                room1.expected_temp = new_temp
                print("set new temp to: ", new_temp)

            # calculate power to heater
            power = pid(room1.room_temp)

            # calculate heater temperature and heat given out
            heater_temp, heat = self.heater_temp_calculate(power, room1.room_temp)

            # returns room temperature based on differential equation
            room_temp = room1(heat, self.dt)

            # TODO: split into process
            # saves state to database
            db_push_temp(room_temp, heater_temp)
            time.sleep(self.dt - ((time.time() - start_time) % self.dt))

    def time_prediction(self, room, queue):
        speed_increase = 10
        # increase dt to speed up the process
        self.dt *= speed_increase
        # set controller
        pid = PID(1000, 0.001, 0.1, set_point=room.expected_temp)
        # set limits
        pid.out_min, pid.out_max = self.power_min, self.power_max
        # counter to estimate time
        i = 0
        heater_temps = []
        room_temps = []
        times = []
        while True:
            i += 1

            # calculate power to heater
            power = pid(room.room_temp, self.dt)

            # calculate heater temperature and heat given out
            heater_temp, heat = self.heater_temp_calculate(power, room.room_temp)

            room_temp_last = room.room_temp

            # calculate room temperature based on heat given out
            room_temp = room(heat, self.dt)

            # testing purposes only
            # START:
            room_temps.append(room_temp)
            heater_temps.append(heater_temp)
            times.append(i * speed_increase)

            # TODO: uncomment this:
            # estimate if reached set temperature
            # if round(room.room_temp, 1) and round(room_temp_last, 1) == room.expected_temp:
            #     break
            # TODO: remove this:
            if i == 10000:
                break
            # END

        # calculate amount of iterations needed * given dt (as given dt is 1 second)
        ret_value = (i * self.dt / speed_increase)

        # Testing purposes only
        # START:
        output_file("C:/projectspy/Temp-Control/graph.html", title="estimated quick")
        fig = figure(title="estimated", plot_height=750, plot_width=1350, x_axis_label="Time[s]", y_axis_label="temps[C]")
        fig.line(times, room_temps, color="blue", legend_label="room temps[C]", line_width=3)
        fig.line(times, heater_temps, color="red", legend_label="heater temps[C]", line_width=2)
        show(fig)
        # END

        # send to router
        queue.put(ret_value)

    def heater_temp_calculate(self, watts, room_temp):

        if self.heater_temp_now >= 62:
            watts = 0

        # copper heat capacity: 0.385 kJ/kg, water heat capacity: 4.2 kJ/kg
        cp = 0.5 * 4.2 + 0.5 * 0.385

        # mass of heater: 20 kg
        mass = 20

        # 1 watt = 1 J/s
        # watt * s / 1000 = kJoules
        heat = watts * self.dt / 1000

        # Q = m * cp * dT -> dT = Q / m * cp
        # C = (kJ / s) / (kg * Kj / kg / C)
        delta_temp = heat / (mass * cp)

        # surface of heater: 0.57m*0.42m*2 + 0.19m*0.42m*2 + 0.19m*0.57m*2
        surface = 0.57 * 0.42 * 2 + 0.19 * 0.42 * 2 + 0.19 * 0.57 * 2  # m^3

        # https://www.engineeringtoolbox.com/overall-heat-transfer-coefficient-d_434.html
        coefficient = 12.5  # W/m^3K

        # temperature difference
        temp_difference = room_temp - self.heater_temp_now  # C
        # print("temp difference: ", temp_difference)

        # Newton's law of cooling
        # Q = h * A * dT
        transfer_out = coefficient * surface * temp_difference  # W

        heat_given = transfer_out * self.dt / 1000  # kJ

        temperature_given = heat_given / (mass * cp)  # C

        self.heater_temp_now += delta_temp + temperature_given

        if heat_given < 0:
            heat_given = abs(heat_given)
        return self.heater_temp_now, heat_given


class Room:
    def __init__(self, room_temp=19, expected_temp=32):
        self.room_temp = room_temp
        self.expected_temp = expected_temp
        self.room_width = 3
        self.room_height = 3
        self.room_length = 3
        self.room_surface = self.room_length * self.room_width
        self.room_volume = self.room_length * self.room_width * self.room_height

    def __call__(self, heat, dt):
        # given:
        #   mass of air = 0 kg
        #   mass of furniture = 100 kg
        #   cp of wood = 1.7 kJ/kg
        #   cp of air = 1.012 kJ/kg
        #   B = 0.005

        mass = 100  # kg
        cp = 1.012 * 0.9 + 1.7 * 0.1  # kJ / kg

        # Q = m * cp * dT  ===>  dT = Q / m * cp
        qin = heat / (mass * cp)

        # to set up amount of heat to be put in
        b = 0.001
        # print("room temp: ", self.room_temp)
        delta_temp = ((qin - b * pow(self.room_temp, 0.5)) * dt) / self.room_surface
        # print("delta temp: ", delta_temp, "\n")
        self.room_temp += delta_temp
        return self.room_temp

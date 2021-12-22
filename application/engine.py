from datetime import datetime
import time
from simple_pid import PID
from multiprocessing import Queue

from helpers import db_push_temp


# TODO:
# remove simple_pid
# heater equation?
# room heating equation
# atm: we're getting power from PID.
# should be: returning room temperature rather than power brought to room.

# what can be done:

#   argument out power to heater
#   turn that into joules
#   Q = R I^2t -> resistance * current voltage squared * time (or: wattage of radiator (joules/s) * s)
#   example heater: 1600W.
#   this is a tank, therefore differential eq has to be used here.
#   minimum of 0 J to be passed off.

#   1. additionally: turn that into celsius for heater temperature

#   calculate room temperature based on given joules of heater
#   if 0 -> flow out rate of room is constant in simulation.
#   co-processing - how to implement?

#   2. additionally: add function to return how much time left for temperature to reach set point

def clamp(mini, maxi, value):
    return None if value is None else min(maxi, max(mini, value))


class Engine:
    dt = 0.1  # s

    def __init__(self):
        self.power_max = 1600  # W
        self.power_min = 0  # W
        self.heater_temp_now = 19  # C

    def worker(self, q, room1: 'Room'):
        print("Worker is running")
        # Cohen-Coon method
        # https://link.springer.com/article/10.1007/s42452-019-0929-y
        pid = PID(3.9931, 0.4144, 2.6267, setpoint=room1.expected_temp)
        pid.output_limits = (self.power_min, self.power_max)
        start_time = time.time()
        while True:
            # TODO: split into thread
            # below pulls new temp from queue
            if not q.empty():
                new_temp = q.get()
                pid.setpoint = new_temp
                room1.expected_temp = new_temp
                print("set new temp to: ", new_temp)

            power = pid(room1.room_temp)
            # below calculates heater temp and heat put in
            heater_temp, heat = self.heater_temp_calculate(power)

            print("power [W]: ", power)
            print("heat [J]: ", heat)
            print("heater temp [C]: ", heater_temp)

            # this returns room temperature based on differential equation
            room_temp = room1.update(heat, self.dt)
            #  TODO: split into thread
            db_push_temp(room_temp, heater_temp)

            time.sleep(self.dt - ((time.time() - start_time) % self.dt))

    def heater_temp_calculate(self, watts):
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

        self.heater_temp_now += delta_temp
        # TODO: To finish up nicely
        return self.heater_temp_now, heat


class Room:
    def __init__(self):
        self.room_temp = 19
        self.expected_temp = 32
        self.room_width = 3
        self.room_height = 3
        self.room_length = 3
        self.room_surface = self.room_length * self.room_width
        self.room_volume = self.room_length * self.room_width * self.room_height

    def update(self, heat, dt):
        # if heater_power > 0:
        #     self.room_temp += 0.002 * heater_power * dt  # play with this value for faster / slower temp changes.
        # self.room_temp -= 0.02 * dt

        # heater power - what units into room temp? Joule -> celsius
        # given:
        #   mass of air = 0 kg
        #   mass of furniture = 400 kg
        #   cp of wood = 1.7 kJ/kg
        #   cp of air = 1.012 kJ/kg
        #   B = 0.005

        mass = 400  # kg
        cp = 1.012 * 0.9 + 1.7 * 0.1  # kJ / kg
        # Q = m * cp * dT -> dT = Q / m * cp
        # C = (kJ / s) / (kg * kJ / kg / C)
        qin = heat / (mass * cp)
        print("Q in: ", qin)

        # to set up amount of heat to be put in
        b = 0.001
        print("room temp: ", self.room_temp)
        delta_temp = ((qin - b * pow(self.room_temp, 0.5)) * dt) / self.room_surface
        print("delta temp: ", delta_temp, "\n")
        self.room_temp += delta_temp
        return self.room_temp

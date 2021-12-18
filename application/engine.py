import sqlite3


class engine:
    def __init__(self) -> None:
        self.roomsize = 4.3 * 4.9 * 2.75  # m^3

        self.Tp = 0.1  # step [s]

        self.ti = 0.75  # integral term
        self.td = 5  # differential term
        self.kp = 0.015  # proportional term

        self.e = []  # error value
        self.e.append(0)

        self.umin = 0  # V
        self.umax = 10  # V
        self.udiff = self.umax - self.umin  # V
        self.u = []  # V in time
        self.u.append(0)

        self.temp = []  # C
        self.temp.append(0)
        self.tempRequested = 20  # C ?necessary
        self.tempMax = 32  # C
        self.tempMin = 20  # C
        # self.tempDiff = self.temperatureMax - self.temperatureMin

        self.B = 0.035  # heat loss factor

    def calculate_regulator(self):
        # needs inserting:
        # previous temp
        # previous error value
        # this will calculate the regulation in V
        # returns the upid ? which should be temperature of the heater # # #
        pass

    def calculate_heater(self):
        # needs inserting:
        # upid
        # tempRequested
        # returns the temperature of room
        pass

import time
from helpers import limit


class PID(object):

    def __init__(self, kp=1.0, ki=0.0, kd=0.0, set_point=0, out_min=None, out_max=None):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.set_point = set_point
        self.out_min, self.out_max = out_min, out_max
        self.prop = self.int = self.der = 0
        self.time_last = time.monotonic()
        self.out_last = self.in_last = None

    def __call__(self, temp_in, dt=None):
        # setting dt
        time_now = time.monotonic()
        if dt is None:  # if no time step is passed
            dt = time_now - self.time_last
            if not dt:  # handling 0 values as seen by interpreter
                dt = 1e-12  # tiny value larger than 0 as seen by interpreter
        elif dt <= 0:  # else if passed negative value
            raise ValueError('negative dt')
        # else dt is given by engine, this will result in time simulation

        # counting error value
        error_val = self.set_point - temp_in
        if self.in_last is None:  # if first call
            delta_in = temp_in
        else:  # else difference in temperature
            delta_in = temp_in - self.in_last

        # proportional term
        self.prop = self.kp * error_val

        # integral term
        self.int += self.ki * error_val * dt
        self.int = limit(self.int, self.out_min, self.out_max)

        # derivative termp
        self.der = (-self.kd * delta_in) / dt

        # output value - sum of all terms
        out_value = self.prop + self.int + self.der
        out_value = limit(out_value, self.out_min, self.out_max)

        self.out_last = out_value
        self.in_last = temp_in
        self.time_last = time_now

        return out_value

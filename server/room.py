class Room:
    def __init__(self, room_temp=19, expected_temp=32):
        self.room_temp = room_temp
        self.expected_temp = expected_temp
        self.room_width = 2
        self.room_height = 2
        self.room_length = 2
        self.room_surface = self.room_length * self.room_width
        self.room_volume = self.room_length * self.room_width * self.room_height

    def __call__(self, heat, dt):
        # given:
        #   mass of air = 0 kg
        #   mass of furniture = 100 kg
        #   cp of wood = 1.7 kJ/kg
        #   cp of air = 1.012 kJ/kg
        #   B = 0.0001

        mass = 40  # kg
        cp = 1.012 * 0.9 + 1.7 * 0.1  # kJ / kg

        # Q = m * cp * dT  ===>  dT = Q / m * cp
        qin = heat / (mass * cp)

        # heat loss coefficient
        b = 0.0001

        delta_temp = ((qin - b * pow(self.room_temp, 0.5)) * dt) / self.room_volume
        self.room_temp += delta_temp
        return self.room_temp

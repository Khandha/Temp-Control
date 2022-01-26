class Room:
    def __init__(self, room_temp=19, expected_temp=32):
        self.room_temp = room_temp
        self.expected_temp = expected_temp
        self.room_width = 2
        self.room_height = 2
        self.room_length = 2
        self.room_surface = self.room_length * self.room_width
        self.room_volume = self.room_length * self.room_width * self.room_height

        # given:
        #   mass of furniture = 100 kg
        #   cp of wood = 1.7 kJ/kg
        #   cp of air = 1.012 kJ/kg
        #   B = 0.0001
        self.mass_of_air = 1.225 * self.room_volume  # kg
        self.mass = 100 + self.mass_of_air  # kg
        self.cp = 1.012 * 0.9 + 1.9 * 0.1  # kJ / kg
        self.b = 0.0001

    def __call__(self, heat, dt):
        # Q = m * cp * dT  ===>  dT = Q / m * cp
        delta_temp = heat / (self.mass * self.cp)
        # zmiana temperatury - wzór 2).
        # Q = h * A * delta temperatury
        self.room_temp += delta_temp - self.room_temp * self.b
        return self.room_temp

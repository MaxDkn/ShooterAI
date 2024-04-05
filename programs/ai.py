import random


class ArtificialIntelligence:
    def __init__(self, map_size):
        self.map_size = map_size

    def choose_direction(self):
        x = random.randint(-1, self.map_size[0]/self.map_size[0])
        y = random.randint(-1, 1)
        return x, y

    def choose_shooting(self):
        if random.randint(0, 10) == 0:
            x_shoot = random.randint(0, self.map_size[0])
            y_shoot = random.randint(0, self.map_size[1])
            return x_shoot, y_shoot
        else:
            return None

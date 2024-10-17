from entity import Entity

class Human(Entity):
    def __init__(self, id, hp, damage, speed, attack_speed, x, y, width, height, attack_range):
        super().__init__(id, hp, damage, speed, attack_speed,x,y, width, height, attack_range)
        
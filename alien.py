from entity import Entity
import pygame

class Alien(Entity):
    def __init__(self, id, hp, damage, speed, attack_speed, x, y, width, height, attack_range):
        super().__init__(id, hp, damage, speed, attack_speed,x,y, width, height, attack_range)
        
    def render(self, screen):
        super().render(screen)
        pygame.draw.rect(screen, "red", self)
        
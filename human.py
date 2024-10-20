from entity import Entity
import pygame

class Human(Entity):
    def __init__(self, id, hp, damage, speed, attack_speed, x, y, width, height, attack_range):
        super().__init__(id, hp, damage, speed, attack_speed,x,y, width, height, attack_range)
    
    def render(self, screen):
        super().render(screen)
        pygame.draw.rect(screen, "blue", self)
        
        if self.attack_animation:
            pygame.draw.line(screen, "blue", (self.centerx, self.centery), (self.enemy.centerx, self.enemy.centery), 4)
            self.attack_animation = False
    
        
from entity import Entity
import pygame

class Human(Entity):
    def __init__(self, id, hp, damage, speed, attack_speed, x, y, width, height, attack_range):
        super().__init__(id, hp, damage, speed, attack_speed,x,y, width, height, attack_range)
        self.bg = pygame.image.load("images/human.png")
        self.bg = pygame.transform.scale(self.bg, (width * 2, height * 2))
        self.color_hp = "blue"
    
    def render(self, screen):
        super().render(screen)
        screen.blit(self.bg, (self.x, self.y))

        if self.attack_animation:
            pygame.draw.line(screen, "blue", (self.centerx, self.centery), (self.enemy.centerx, self.enemy.centery), 4)
            self.attack_animation = False
    
        
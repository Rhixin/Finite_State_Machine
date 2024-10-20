import pygame
import math

class Potion():
    def __init__(self, x, y, radius):
        self.x = x  
        self.y = y  
        self.radius = radius  
        self.current_state = 0
        self.spawn_state()
        
    def render(self, screen):
        pygame.draw.circle(screen, "green", (self.x, self.y), self.radius)
        
    def update_state(self, entities):
        entity = self.detect_entities(entities)

        if not entity:
            self.current_state = 1
        else:
            self.current_state = 2
            
        if self.current_state == 1:
            self.idle_state()
        else:
            self.dead_state()
    
    def detect_entities(self, entities):
        for entity in entities:
            
            distance = math.sqrt((self.x - entity.centerx) ** 2 + (self.y - entity.centery) ** 2)

            if distance <= self.radius * 2: 
                entity.hp = 100  
                print("Collision detected with entity!")
                return entity
        
        return None

        
    #STATES
    def spawn_state(self):
        print(f"A potion appeared at x {self.x} and y {self.y}")
        
    def idle_state(self):
        print("Doing nothing...")
        
    def dead_state(self):
        print("Potion has been used")
        
        
    
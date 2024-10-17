import pygame
import math

class Potion(pygame.Rect):
    def __init__(self, id):
        self.id = id
        self.current_state = 0
        self.update_state()
        
    def render(self, screen):
        self.draw_health_bar(screen)
        self.draw_range(screen)
        
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
            distance = math.sqrt((self.centerx - entity.centerx) ** 2 + (self.centery - entity.centery) ** 2)
            
            if distance <= self.width:
                entity.hp = 100
                return entity
        
    #STATES
    def spawn_state(self):
        print("A potion appeared")
        
    def idle_state(self):
        print("Waiting...")
        
    def dead_state(self):
        print("Dead!")
        
        
    
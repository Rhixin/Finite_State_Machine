import pygame
import random
import math

class Entity(pygame.Rect):
    def __init__(self, id, hp, damage, speed, attack_speed, x, y, width, height, attack_range):
        super().__init__(x, y, width, height)  
        self.id = id
        self.hp = hp
        self.damage = damage
        self.speed = speed
        self.attack_speed = attack_speed
        self.direction = pygame.Vector2(1, 0)  
        self.attack_range = attack_range
        
        #private attributes
        self.current_state = 0
        self.attack_timer = 0
        self.move_timer = 0
        
    def update_state(self, enemies, dt):
        
        
        enemy = self.detect_enemies(enemies)
        
        if enemy:
            self.current_state = 3
        else:
            self.current_state = 2
        
        if self.current_state == 0:
            self.spawn_state()
        elif self.current_state == 1:
            self.idle_state()
        elif self.current_state == 2:
            self.hunting_state(dt)
        elif self.current_state == 3:
            self.attacking_state(enemy, dt)  
        
    #HELPER FUNCTIONS
    def move(self, dt):
        self.move_timer += dt
        
        if self.move_timer >= self.speed:
            self.direction = random.choice([self.direction.rotate(-90), self.direction.rotate(90)])
            
            new_position = self.center + (self.direction * (self.speed + 10))
            
            if 0 <= new_position.x < 1280 - self.width and 0 <= new_position.y < 720 - self.height:
                self.move_ip(self.direction * 10)  
                self.move_timer = 0
            


    def attack(self, enemy, dt):
        self.attack_timer += dt
        
        if self.attack_timer >= self.attack_speed:
            self.attack_timer = 0
            enemy.hp -= self.damage
            #print(f"Enemy {enemy.id} hp: {enemy.hp}")
            
    def random_state(self):
        states = [self.idle, self.move, self.defend, self.attack]
        state_chosen = random.choice(states)
        state_chosen()
        
    def detect_enemies(self, enemies):
        for enemy in enemies:
            distance = math.sqrt((self.centerx - enemy.centerx) ** 2 + (self.centery - enemy.centery) ** 2)
            
            if distance <= (self.width * 5):
                return enemy
        return None
    
    
    #STATES
    
    #state 0
    def spawn_state(self):
        print(f"Entity {self.id} just spawned.")
        
    #state 1 
    def idle_state(self):
        print(f"Entity {self.id} is doing nothing.")
        
    #state 2
    def hunting_state(self, dt):
        self.move(dt)
        
    #state 3
    def attacking_state(self, enemy, dt):
        self.attack(enemy, dt)
    
    #state 4
    def finding_ammo_state(self):
        print(f"Entity {self.id} is moving, unable to detect enemies, prioritizing ammo.")
        
    #state 5
    def finding_potion_state(self):
        print(f"Entity {self.id} is moving, unable to detect enemies, prioritizing potion.")
        
    #state 6
    def dead_state(self):
        print(f"Entity {self.id} is dead.")
        
        
    #GRAPHICS
    def draw_health_bar(self,entity, screen):
        max_health = 100
        health_ratio = entity.hp / max_health  
        health_bar_width = 40  
        health_bar_height = 5  

        bar_x = entity.x + (entity.width - health_bar_width) // 2  
        bar_y = entity.y - 30  

        pygame.draw.rect(screen, 'black', (bar_x, bar_y, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, 'pink', (bar_x, bar_y, health_bar_width * health_ratio, health_bar_height))
        
    def draw_range(self, screen):
        pygame.draw.circle(screen, 'gray', self.center, self.attack_range, 1)
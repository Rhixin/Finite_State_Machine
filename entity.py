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
        self.current_state = 0
        self.attack_timer = 0
        self.move_timer = 0
        
    def render(self, screen):
        self.draw_health_bar(screen)
        #self.draw_range(screen)
        
        
    def update_state(self, enemies,potions, dt):
        enemy = self.detect_enemies(enemies)
        
        if enemy:
            self.current_state = 3
        else:
            self.current_state = 2
        
        if self.hp <= 30:
            
            self.current_state = 4
            
            if self.find_nearest_potion(potions) is None:
                self.current_state = 1
                
            if self.hp <= 0:
                self.current_state = 5
            
        
        if self.current_state == 0:
            self.spawn_state()
        elif self.current_state == 1:
            self.idle_state()
        elif self.current_state == 2:
            self.hunting_state(enemies, dt)
        elif self.current_state == 3:
            self.attacking_state(enemy, dt)  
        elif self.current_state == 4:
            self.finding_potion_state(potions, dt)
        
    #HELPER FUNCTIONS
    def move_towards_potion(self, potion, dt):
        self.move_timer += dt
        
        if self.move_timer >= self.speed:
            self.direction = pygame.Vector2(potion.x - self.centerx, potion.y - self.centery)
        
            if self.direction.length() > 0: 
                self.direction.normalize_ip()  
                
            new_position = self.center + (self.direction * self.speed)
            
            if 0 <= new_position.x < 1280 - self.width and 0 <= new_position.y < 720 - self.height:
                self.move_ip(self.direction * 20)  
                self.move_timer = 0
                
    def find_nearest_potion(self, potions):
        nearest_potion = None
        nearest_distance = float('inf') 

        for potion in potions:

            distance = math.sqrt((self.centerx - potion.x) ** 2 + (self.centery - potion.y) ** 2)

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_potion = potion

        if nearest_potion is not None:
            return nearest_potion 
        else:
            return None
        
    def move_towards_enemy(self, enemy, dt):
        self.move_timer += dt
        
        if self.move_timer >= self.speed:
            self.direction = pygame.Vector2(enemy.x - self.centerx, enemy.y - self.centery)
        
            if self.direction.length() > 0: 
                self.direction.normalize_ip()  
                
            new_position = self.center + (self.direction * self.speed)
            
            if 0 <= new_position.x < 1280 - self.width and 0 <= new_position.y < 720 - self.height:
                self.move_ip(self.direction * 7)  
                self.move_timer = 0
        
    def find_nearest_enemy(self, enemies):
        nearest_potion = None
        nearest_distance = float('inf') 

        for enemy in enemies:

            distance = math.sqrt((self.centerx - enemy.x) ** 2 + (self.centery - enemy.y) ** 2)

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_potion = enemy

        if nearest_potion is not None:
            return nearest_potion 
        else:
            return None
        
    

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
    def hunting_state(self,enemies, dt):
        nearest_enemy = self.find_nearest_enemy(enemies)
        if nearest_enemy is not None:
            self.move_towards_enemy(nearest_enemy, dt)
        
    #state 3
    def attacking_state(self, enemy, dt):
        self.attack(enemy, dt)
        
    #state 4
    def finding_potion_state(self, potions, dt):
        nearest_potion = self.find_nearest_potion(potions)
        if nearest_potion is not None:
            self.move_towards_potion(nearest_potion, dt)
        
    #state 5
    def dead_state(self):
        print(f"Entity {self.id} is dead.")
        
        
    #GRAPHICS
    def draw_health_bar(self, screen):
        max_health = 100
        health_ratio = self.hp / max_health  
        health_bar_width = 40  
        health_bar_height = 5  

        bar_x = self.x + (self.width - health_bar_width) // 2  
        bar_y = self.y - 30  

        pygame.draw.rect(screen, 'black', (bar_x, bar_y, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, 'pink', (bar_x, bar_y, health_bar_width * health_ratio, health_bar_height))
        
    def draw_range(self, screen):
        pygame.draw.circle(screen, 'gray', self.center, self.attack_range, 1)
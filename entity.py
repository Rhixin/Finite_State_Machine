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
        self.attack_timer = 0
        self.move_timer = 0
        self.attack_animation = False
        self.enemy = None
        
        self.current_state = 0
        self.transition_table = [
            [ 1,  1,  1,  1,  1,  1,  1,  1],
            [ 1,  2, -1, -1, -1, -1, -1, -1],
            [-1, -1,  2,  3, -1, -1, -1, -1],
            [-1, -1,  1,  3,  4, -1, -1, -1],
            [-1, -1, -1, -1,  4,  5,  1,  3],
            [ 5,  5,  5,  5,  5,  5,  5,  5],
        ]
        
    def render(self, screen):
        self.draw_health_bar(screen)
        font = pygame.font.SysFont('Arial', 12)  
        text_surface = font.render(f'State: {self.current_state}', True, "black") 
        
        text_x = self.x - 10
        text_y = self.y + 20
    
        screen.blit(text_surface, (text_x, text_y))
          
    def update_state(self, enemies,potions, dt):
        machine_input = None
        enemy_in_map = self.find_nearest_enemy(enemies)
        enemy_in_range = self.detect_enemies(enemies)
        potion_in_map = self.find_nearest_potion(potions)
        
        if self.current_state == 0:
            #always go to idle
            machine_input = 0
        elif self.current_state == 1:
            if enemy_in_map:
                machine_input = 1
            else:
                machine_input = 0
        elif self.current_state == 2:
            if enemy_in_range:
                machine_input = 3
            else:
                machine_input = 2
        elif self.current_state == 3:
            if enemy_in_range:
                machine_input = 3
            else:
                machine_input = 2
                
            if self.hp <= 30:
                machine_input = 4
        elif self.current_state == 4:
            if self.hp <= 0:
                machine_input = 5
            elif self.hp <= 30:
                machine_input = 4
            else:
                machine_input = 6
            
            if potion_in_map is None:
                machine_input = 7
        else:
            #dead state
            machine_input = 5
            
            
        self.current_state = self.transition_table[self.current_state][machine_input]
        
        if self.current_state == 0:
            self.spawn_state()
        elif self.current_state == 1:
            self.idle_state()
        elif self.current_state == 2:
            self.hunting_state(enemies, dt)
        elif self.current_state == 3:
            self.attacking_state(enemy_in_range, dt)  
        elif self.current_state == 4:
            self.finding_potion_state(potions, dt)
        elif self.current_state == 5:
            self.dead_state()
            
    
            
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
        
    
        
    #HELPER FUNCTIONS
    def move_towards_potion(self, potion, dt):
        self.move_timer += dt
        
        if self.move_timer >= self.speed:
            self.direction = pygame.Vector2(potion.x - self.centerx, potion.y - self.centery)
        
            if self.direction.length() > 0: 
                self.direction.normalize_ip()  
                
            new_position = self.center + (self.direction * self.speed)
            
            if 0 <= new_position.x < 1280 - self.width and 0 <= new_position.y < 720 - self.height:
                self.move_ip(self.direction * 10)  
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
        nearest_enemy = None
        nearest_distance = float('inf') 

        for enemy in enemies:

            distance = math.sqrt((self.centerx - enemy.x) ** 2 + (self.centery - enemy.y) ** 2)

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_enemy = enemy

        if nearest_enemy is not None:
            return nearest_enemy 
        else:
            return None
        
    

    def attack(self, enemy, dt):
        self.attack_timer += dt
        self.enemy = enemy
        
        # Draw a line from the attacker to the enemy when the timer exceeds attack_speed
        if self.attack_timer >= self.attack_speed:
            
            self.attack_animation = True
            
            # Reset the attack timer and apply damage to the enemy
            self.attack_timer = 0
            enemy.hp -= self.damage
        else:
            self.attack_animation = False

        
    def detect_enemies(self, enemies):
        for enemy in enemies:
            distance = math.sqrt((self.centerx - enemy.centerx) ** 2 + (self.centery - enemy.centery) ** 2)
            
            if distance <= (self.width * 5):
                return enemy
        return None
    
        
        
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
        
        
# Example file showing a circle moving on screen
import pygame
from human import Human
from alien import Alien
from potion import Potion
import random

class Potion_Generator():
    def __init__(self):
        self.cooldown = 5
        self.cooldown_timer = 0
    
    def generate(self, dt):
        self.cooldown_timer += dt
        
        if self.cooldown_timer >= self.cooldown:
            x = random.randint(20, 1260)
            y = random.randint(20, 700)
            
            new_potion = Potion(x, y, 10)
            self.cooldown_timer = 0
            return new_potion
        else:
            return None
        
def draw_text(screen, text, x, y, color="black", fontsize = 10):
    font = pygame.font.SysFont('Arial', fontsize)  
    text_surface = font.render(text, True, color) 
    screen.blit(text_surface, (x,y))

# pygame setup
pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

#List to hold all NPCs
aliens = []
humans = []
potions = []
potion_generator = Potion_Generator()
    

id_counter = 1


while running:
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Check for mouse button down event
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()  
                new_alien = Alien(id_counter, 100, 10, 0.1, 1, mouse_x, mouse_y, 20, 20, 50)
                aliens.append(new_alien) 
            elif event.button == 1:  # Left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()  
                new_human = Human(id_counter, 100, 10, 0.1, 1, mouse_x, mouse_y, 20, 20,50)
                humans.append(new_human)

            id_counter += 1

    screen.fill("white")
    
    draw_text(screen, "Humans VS Alien Simulator", 1, 8, color="black", fontsize = 28)
    draw_text(screen, "Left Click to spawn a Human", 1, 50, color="black", fontsize = 18)
    draw_text(screen, "Right Click to spawn an Alien", 1, 70, color="black", fontsize = 18)
    
    #potions logic
    new_potion = potion_generator.generate(dt)
    
    if new_potion is not None:
        #only 5 potions max sa map
        if len(potions) < 5:
            potions.append(new_potion)
    
    for potion in potions:
        potion.render(screen)
        potion.update_state(aliens + humans)
        
    potions = [potion for potion in potions if potion.current_state != 2]
    
    #aliens logic
    for alien in aliens:
        alien.render(screen)
        alien.update_state(humans,potions, dt)
        
    aliens = [alien for alien in aliens if alien.hp > 0]
    
    #humans logic
    for human in humans:
        human.render(screen)
        human.update_state(aliens,potions, dt)
        
    humans = [human for human in humans if human.hp > 0]

    pygame.display.flip()
    
    dt = clock.tick(60) / 1000

pygame.quit()

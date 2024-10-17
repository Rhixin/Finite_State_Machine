# Example file showing a circle moving on screen
import pygame
from human import Human
from alien import Alien

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# List to hold all NPCs
aliens = []
humans = []

id_counter = 1


while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Check for mouse button down event
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()  
                new_alien = Alien(id_counter, 100, 10, 0.25, 1, mouse_x, mouse_y, 20, 20, 50)
                aliens.append(new_alien) 
            elif event.button == 3:  # Right mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()  
                new_human = Human(id_counter, 100, 10, 0.25, 1, mouse_x, mouse_y, 20, 20,50)
                humans.append(new_human)

            id_counter += 1

    screen.fill("white")

    for alien in aliens:
        pygame.draw.rect(screen, "red", alien)
        alien.draw_health_bar(alien, screen)
        alien.draw_range(screen) 
        
        alien.update_state(humans, dt)
        
    aliens = [alien for alien in aliens if alien.hp > 0]
        
    for human in humans:
        pygame.draw.rect(screen, "blue", human)
        human.draw_health_bar(human, screen) 
        human.draw_range(screen)
        
        human.update_state(aliens, dt)
        
    humans = [human for human in humans if human.hp > 0]

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()

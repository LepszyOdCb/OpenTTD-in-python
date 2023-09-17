import pygame
import sys

# Initialization
pygame.init()

# Info about monitor display
info = pygame.display.Info()

# Screen settigs
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
pygame.display.set_caption('Gra na pełnym ekranie')

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (10, 205, 100)
blue = (0, 0, 255)
yellow = (255, 255, 0)
purple = (128, 0, 128)
cyan = (0, 255, 255)
magenta = (255, 0, 255)
orange = (255, 165, 0)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

   
    screen.fill((green))

    
    pygame.display.flip()

# Zakończenie gry
pygame.quit()
sys.exit()

import pygame
from pygame.locals import *
import sys

pygame.init()
window = pygame.display.set_mode((800, 600))
window.fill((224, 210, 121))

while True:
    # Handle user input
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            print(event)

    
    pygame.display.flip()

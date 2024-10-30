import pygame
from pygame.locals import *
import sys

pygame.init()
window = pygame.display.set_mode((800, 600))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

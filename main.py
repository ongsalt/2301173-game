import pygame
from pygame.locals import *
from kaoyum.overlay import Scene, GameplayScene
import sys

from kaoyum.ui.event import NAVIGATION_EVENT

pygame.init()
# pygame.freetype.init()

DISPLAY_SIZE = (800, 600)
screen = pygame.display.set_mode(DISPLAY_SIZE)
clock = pygame.time.Clock()

active_scene = GameplayScene(DISPLAY_SIZE)

while True:
    # fixed frame rate
    dt = clock.tick(1)

    # Event processing queue
    unconsumed_events = []
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        unconsumed_events.append(event)
    
    # Let the scene do it's thing
    active_scene.run(screen, dt, events=unconsumed_events)

    pygame.display.flip()

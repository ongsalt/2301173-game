import pygame
from pygame.locals import *
from kaoyum.scene import Scene, GameplayScene, HomeScene
import sys

from kaoyum.ui.event import NAVIGATION_EVENT

pygame.init()
# pygame.freetype.init()

DISPLAY_SIZE = (800, 600)
screen = pygame.display.set_mode(DISPLAY_SIZE)
clock = pygame.time.Clock()

scenes_stack: list[Scene] = [
    HomeScene(DISPLAY_SIZE),
    GameplayScene(DISPLAY_SIZE),
]
active_scene = scenes_stack[0]

while True:
    # fixed frame rate
    dt = clock.tick(60)

    # Event processing queue
    unconsumed_events = []
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == NAVIGATION_EVENT:
            if event.to == "game":
                active_scene = scenes_stack[1]
            # cursed early return
        # print(event)
        unconsumed_events.append(event)
    
    # Let the scene do it's thing
    messages = active_scene.run(screen, dt, events=unconsumed_events)

    pygame.display.flip()

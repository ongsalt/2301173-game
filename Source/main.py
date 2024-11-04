import pygame
from pygame.locals import *
from scene import Scene, GameScene, HomeScene
import sys

pygame.init()
pygame.freetype.init()

DISPLAY_SIZE = (800, 600)
screen = pygame.display.set_mode(DISPLAY_SIZE)
clock = pygame.time.Clock()

scenes_stack: list[Scene] = [
    HomeScene(DISPLAY_SIZE),
    GameScene(DISPLAY_SIZE),
]
active_scene = scenes_stack[0]

while True:
    # fixed frame rate
    clock.tick(60)

    # Event processing queue
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            # cursed early return
        message = active_scene.handle_event(event)
        if message == "exit":
            pygame.quit()
            sys.exit()
        elif message == "to:game":
            active_scene = scenes_stack[1]
    
    # Let the scene do it's thing
    active_scene.run(screen)

    pygame.display.flip()

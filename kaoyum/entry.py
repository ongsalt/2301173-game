import sys
from threading import Thread
import pygame
from pygame.locals import *
from kaoyum.map import initialize_blocks
from kaoyum.ui.scene import Scene, GameplayScene

def main():
    game_entry()

def game_entry():
    pygame.init()

    DISPLAY_SIZE = (800, 600)
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Kaoyum Adventure')

    active_scene = GameplayScene(DISPLAY_SIZE)

    while True:
        # fixed frame rate
        dt = clock.tick(60)

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

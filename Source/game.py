from typing import Literal
import pygame
from player import Player
from pygame.locals import * 

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.obstacles = []
        self.score_points = []
        self.state: Literal["running", "pause"] = "pause"
        self.player = Player()

    def run(self, screen: pygame.Surface):
        self.handle_input()
        self.player.update()

        screen.fill((253, 238, 173))
        self.player.draw(screen)

    def handle_input(self):
        keys_pressed = pygame.key.get_pressed()
        key_up = keys_pressed[K_w] or keys_pressed[K_UP]
        key_down = keys_pressed[K_s] or keys_pressed[K_DOWN]
        if key_up and not key_down:
            self.player.move_y(-10)
        elif key_down and not key_up:
            self.player.move_y(10)
        
    def handle_event(self, event: pygame.event.Event):
        pass

    def generate_obstacles(self):
        pass

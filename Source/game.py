from typing import Literal
import pygame
from player import Player
from pygame.locals import * 
from color_change import ColorChange
from scorepoint import Scorepoint
from obstacle import Obstacle

class Game:
    def __init__(self):
        self.obstacles: list[Obstacle] = []
        self.score_points: list[Scorepoint] = []
        self.color_changers: list[ColorChange] = []
        self.state: Literal["running", "pause"] = "pause"
        self.player = Player()
        self.image = pygame.image.load("Assets/images/ThaiRice.jpg")

    def run(self, screen: pygame.Surface):
        self.handle_input()

        # update
        self.player.update()

        # draw
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

    def load_block(self):
        pass

    def remove_dead_objects(self):
        new_obstacles = self.obstacles
        for obstacle in self.obstacles:
           if obstacle.x < 0:
              new_obstacles.remove(obstacle)
        self.obstacles = new_obstacles

        new_color_changers = self.color_changers
        for color_changer in self.color_changers:
           if color_changer.x < 0:
              new_color_changers.remove(color_changer)
        self.color_changers = new_color_changers

        new_score_point = self.score_points
        for score_point in self.score_points:
           if score_point.x < 0:
              new_score_point.remove(score_point)
        self.score_points = new_score_point
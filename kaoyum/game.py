import pygame
from pygame.locals import * 
from typing import Literal
from kaoyum.player import Player
from kaoyum.color_change import ColorChange
from kaoyum.scorepoint import Scorepoint
from kaoyum.obstacle import Obstacle

class Game:
    def __init__(self, screen_size: tuple[int, int]):
        self.obstacles: list[Obstacle] = []
        self.score_points: list[Scorepoint] = []
        self.color_changers: list[ColorChange] = []
        self.state: Literal["running", "pause"] = "pause"
        self.player = Player(screen_size)

    def run(self, screen: pygame.Surface, dt: int):
        # update
        self.player.update()

        # draw
        screen.fill((253, 238, 173))
        self.player.draw(screen)

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
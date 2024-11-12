import pygame
from pygame.locals import * 
from pygame.event import Event
from typing import Literal
from kaoyum.player import Player
from kaoyum.color_change import ColorChange
from kaoyum.scorepoint import Scorepoint
from kaoyum.obstacle import Obstacle
from kaoyum.assets_manager import AssetsManager

class Game:
    def __init__(self, screen_size: tuple[int, int]):
        self.obstacles: list[Obstacle] = []
        self.score_points: list[Scorepoint] = []
        self.color_changers: list[ColorChange] = []
        self.state: Literal["running", "pause"] = "pause"
        self.player = Player(screen_size)
        self.load_mock_block()
        self.score = 0

    def run(self, screen: pygame.Surface, dt: int):
        # update
        self.player.update()

        for score_point in self.score_points:
           score_point.update()         

        for score_point in self.score_points[:]:
            if score_point.is_collided(self.player.rect):
                self.score += score_point.score
                self.score_points.remove(score_point)

        # draw
        screen.fill((253, 238, 173))
        self.player.draw(screen)

        for score_point in self.score_points:
            score_point.draw(screen)

    def handle_event(self, event: Event):
        pass

    def load_block(self):
        pass

    def load_mock_block(self):
        image = AssetsManager().get("slime_2.gif")
        self.obstacles.append(Obstacle(100, 100, 64, 64, 10, image))
        self.obstacles.append(Obstacle(200, 100, 64, 64, 10, image))
        self.score_points.append(Scorepoint(300, 100, 64, 64, 10, image))
        self.score_points.append(Scorepoint(400, 100, 64, 64, 10, image))
        self.score_points.append(Scorepoint(700, 100, 64, 64, 10, image))
        
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
import pygame
from pygame.locals import * 
from pygame.event import Event
from typing import Literal
from kaoyum.background import Background
from kaoyum.player import Player
from kaoyum.color_change import ColorChange
from kaoyum.scorepoint import Scorepoint
from kaoyum.obstacle import Obstacle
from kaoyum.assets_manager import AssetsManager
from kaoyum.block import Block, initialize_block

class Game:
    def __init__(self, screen_size: tuple[int, int]):
        self.obstacles: list[Obstacle] = []
        self.score_points: list[Scorepoint] = []
        self.color_changers: list[ColorChange] = []
        self.state: Literal["waiting", "running", "paused", "finished"] = "waiting"
        self.player = Player(screen_size)
        self.background = Background(screen_size)
        self.score = 0
        self.blocks = initialize_block()
        self.load_mock_block()

    def run(self, screen: pygame.Surface, dt: int):
        # update player
        if self.state == "running" or self.state == "waiting":
            self.player.rotate_frame(dt)

        if self.state == "running": 
            self.player.update(dt)
            self.background.update(dt)
            
            # update scorepoint
            for score_point in self.score_points:
                score_point.update()    
            for score_point in self.score_points[:]:
                if score_point.is_collided(self.player.rect):
                    self.score += score_point.score
                    self.player.hp += 5
                    self.score_points.remove(score_point)

            # update obstacle
            for obstacle in self.obstacles:
                obstacle.update()

            for obstacle in self.obstacles[:]:
                if obstacle.is_collided(self.player.rect):
                    self.player.take_damage(obstacle.damage)
            
            # update color_changer
            for colorchanger in self.color_changers:
                colorchanger.update()         

            for colorchanger in self.color_changers[:]:
                if colorchanger.is_collided(self.player.rect):
                    pass # เปลี่ยนสี

            if self.player.hp <= 0:
                self.state = "finished"

        # draw
        screen.fill((179, 169, 160))
        self.background.draw(screen)
        self.player.draw(screen)

        for score_point in self.score_points:
            score_point.draw(screen)
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        for colorchanger in self.color_changers:
            colorchanger.draw(screen)

        # should_append_block
        # if should_append_block:
        #     block = random.choice(self.blocks)
        #     self.load_block(block)

    def load_block(self, block: Block):
        new_block = block.copy()
        for ob in new_block.obstacles:
            self.obstacles.append(ob)
        for sc in new_block.score_points:
            self.score_points.append(sc)
        for cc in new_block.color_changers:
            self.color_changers.append(cc)

    def load_mock_block(self):
        image = AssetsManager().get("slime_2.gif")
        self.obstacles.append(Obstacle(1800, 100, 64, 64, 100, image))
        self.obstacles.append(Obstacle(1000, 100, 64, 64, 10, image))
        self.score_points.append(Scorepoint(1100, 100, 64, 64, 10, image))
        self.score_points.append(Scorepoint(1200, 100, 64, 64, 10, image))
        self.score_points.append(Scorepoint(1500, 100, 64, 64, 10, image))

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


    # For state management
    @property
    def is_started(self):
        return self.state != "waiting"

    def start(self):
        if self.state == "waiting":
            self.state = "running"
            self.player.start_moving()

    def pause(self):
        if self.state == "running":
            self.state = "paused"

    def resume(self):
        if self.state == "paused":
            self.state = "running"

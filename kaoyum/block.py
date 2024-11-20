from .obstacle import Obstacle
from .scorepoint import Scorepoint
from .color_changer import ColorChanger
from .assets_manager import AssetsManager

class Block:
    def __init__(self, obstacles: list[Obstacle], score_points: list[Scorepoint], color_changers: list[ColorChanger], offset):
        self.obstacles = obstacles
        self.score_points = score_points
        self.color_changers = color_changers
        self.offset = offset
    
    def copy(self):
        copied_obs = []
        copied_scs = []
        copied_ccs = []
        for obstacle in self.obstacles:
            copied_op = obstacle.copy()
            copied_op.x += self.offset
            copied_op.hitbox.x += self.offset
            copied_obs.append(copied_op)
        for score_point in self.score_points:
            copied_sc = score_point.copy()
            copied_sc.x += self.offset
            copied_sc.hitbox.x += self.offset
            copied_scs.append(copied_sc)
        for color_changer in self.color_changers:
            copied_cc = color_changer.copy()
            copied_cc.x += self.offset
            copied_cc.rect.x += self.offset
            copied_ccs.append(copied_cc)
        return Block(copied_obs,copied_scs,copied_ccs, self.offset)

import pygame


def is_collided(self, player_hitbox: pygame.Rect) -> bool: ...

# velocity = 10px / sec
# velocity = 10/60 px / frame
# รันทุกเฟรม ต้องขยับวัตถุ
def update(self): ...
def draw(self, screen: pygame.Surface): ...

class Obstacle:
    def is_collided(self, player_hitbox: pygame.Rect) -> bool: ...
    def update(self): ...
    def draw(self, screen: pygame.Surface): ...
    def copy(self): ...

class ScorePoint:
    def is_collided(self, player_hitbox: pygame.Rect) -> bool: ...
    def update(self): ...
    def draw(self, screen: pygame.Surface): ...
    def copy(self): ...

class ColorChanger:
    def is_collided(self, player_hitbox: pygame.Rect) -> bool: ...
    def update(self): ...
    def draw(self, screen: pygame.Surface): ...
    def copy(self): ...


# ทำพร้อมกับ load_block()
class Block:
    def __init__(self, obstacles: list[Obstacle], score_points: list[ScorePoint], color_changers: list[ColorChanger]):
        pass


# block = Block(
#         [
#             Obstacle(),
#         ],
#         [], 
#         []
#     ),

# make load_obstracles run every 80 frame
class Game:
    def run():
        # เพิ่มการ update กับ draw ของ 
        # self.obstacles = []
        # self.score_points = []
        # self.color_changers: list[ColorChange] = []
        pass

    # ทำพร้อมกับคลาส Block
    def load_block(self): ...

    # remove all objects that are out of the screen
    def remove_dead_objects(self): ...

class Background:
    pass

# Ongsa 
# game logic
class Scene:
    pass
class Player:
    pass

# HP bar
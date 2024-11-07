import pygame


def is_collided(self, player_hitbox: pygame.Rect) -> bool: ...

# velocity = 10px / sec
# velocity = 10/60 px / frame
# รันทุกเฟรม ต้องขยับวัตถุ
def update(self): ...
def draw(self, screen: pygame.Surface): ...

# nine | 8 Nov
class Obstacle:
    pass

# - 
class ScorePoint:
    pass

# one | 6 Nov
class ColorChanger:
    pass

class Background:
    pass

# Block
# an arrays of dictionary of game object definition
# {
#     "type": "obstacle",
#     "x": 100,
#     "y": 100,
#     "width": 50,
#     "height": 50,
#     "color": (255, 0, 0),
#     "image": "path/to/image.png",
#     "velocity": 10,
# }
# need a function to translate this to a real game object and add some offset to its position first
# this should be a method of the game class

class Game:
    def append_block(self, block: dict): ...

    # remove all objects that are out of the screen
    def remove_dead_objects(self): ...

# Ongsa 
# game logic
class Scene:
    pass
class Player:
    pass

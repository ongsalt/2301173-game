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
class Block:
    pass
class Game:
    pass

# Ongsa 
# game logic
class Scene:
    pass
class Player:
    pass

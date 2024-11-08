import pygame
from pygame import Rect
from dataclasses import dataclass
from typing import Self

# Bruh this is just Flutter

type Size = tuple[int, int]

@dataclass
class Constraints:
    min_width: int
    min_height: int
    max_width: int
    max_height: int

    def coerce(self, w: int, h: int) -> Size:
        w = max(min(w, self.max_width), self.min_width)
        h = max(min(h, self.max_height), self.min_height)
        return (w, h)

@dataclass
class Padding:
    top: int
    right: int
    bottom: int
    left: int

    @property
    def height(self) -> int:
        return self.top + self.bottom

    @property
    def width(self) -> int:
        return self.left + self.right
    
    @property
    def topleft(self) -> tuple[int, int]:
        return self.top, self.left

    def zero() -> Self:
        return Padding(0, 0, 0, 0)
    
    def all(value: int) -> Self:
        return Padding(value, value, value, value)

    def both(vertical: int, horizontal: int) -> Self:
        return Padding(vertical, horizontal, vertical, horizontal)


# TODO: 
#  - raw surface node
#  - box node (with bg)
#  - click handling
class UINode:
    _damaged: bool = True
    children: list[Self]

    def __init__(self, padding: Padding | None = None):
        self.children = []
        self.padding = padding or Padding.zero()
        self.rect = pygame.Rect(0, 0, 0, 0)

    # MUST BE CALL IN THIS ORDER: measure -> layout -> draw
    # accept parent constraints and it own size afer measuring its children
    def measure(self, constraints: Constraints) -> Size:
        return (0, 0)

    # set the rect (absolute position) of each child node
    def layout(self, area: Rect):
        self.rect = area

    # design to draw the node itself NOT THE CHILDREN as it will be handled by the renderer
    def draw(self, screen: pygame.Surface):
        pass

    def draw_bound(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (255, 0, 0, 140), self.rect, 1)

    def __setattr__(self, name, value):
        # Well you should not update the surface directly anyway
        if name not in ["_damaged", "rect"]:
            self._damaged = True
        return super().__setattr__(name, value)

    @property
    def damaged(self):
        return self._damaged
    
    @damaged.setter
    def damaged(self, value: bool):
        self._damaged = value


# Need to measure bounding box
# minimum size is reported itself
# while maximum size is reported by the parent
# im gonna copy jetpack compose's layout system4
# measure -> size -> placing(aka layouting) -> draw
# after measure the parent node should set the rect of the child node
# currently we are drawing children nodes immediately after measuring them and before parent node

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    DISPLAY_SIZE = (800, 600)
    screen = pygame.display.set_mode((800, 600))
    node = UINode()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # เทสตรงนี้นะครับ
        screen.fill((0, 0, 0))
        node.draw(screen)

        pygame.display.flip()

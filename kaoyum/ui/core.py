import pygame
from pygame import Rect
from dataclasses import dataclass
from typing import Self

# Bruh this is just Flutter

# TODO: 
#  - click handling: GestureDetector
#  - shadow
#  - High level things like button, slider, dropdown, etc

type Size = tuple[int, int]

@dataclass(frozen=True)
class Constraints:
    min_width: int
    min_height: int
    max_width: int
    max_height: int

    def coerce(self, w: int, h: int) -> Size:
        w = max(min(w, self.max_width), self.min_width)
        h = max(min(h, self.max_height), self.min_height)
        return (w, h)
    
    def coerce_and_round(self, w: float, h: float) -> Size:
        return self.coerce(round(w), round(h))

@dataclass(frozen=True)
class Padding:
    top: int = 0
    right: int = 0
    bottom: int = 0
    left: int = 0

    @property
    def height(self) -> int:
        return self.top + self.bottom

    @property
    def width(self) -> int:
        return self.left + self.right
    
    @property
    def topleft(self) -> tuple[int, int]:
        return round(self.left), round(self.top)

    def zero() -> Self:
        return Padding(0, 0, 0, 0)
    
    def all(value: int) -> Self:
        return Padding(value, value, value, value)

    def both(vertical: int, horizontal: int) -> Self:
        return Padding(vertical, horizontal, vertical, horizontal)

type ChildrenProp = list[Self | None] | None
class UINode:
    node_type: str = "UINode"
    children: list[Self]

    def __init__(self, padding: Padding | None = None, children: ChildrenProp = None):
        self.children = [] if not children else [child for child in children if child is not None] 
        self.padding = padding or Padding.zero()

    # MUST BE CALL IN THIS ORDER: measure -> layout -> draw
    # well, the runtime will do that for you so you don't have to worry about it
    # accept parent constraints and it own size afer measuring its children
    def measure(self, constraints: Constraints) -> Size:
        return (0, 0)

    # return the relative position of each child node
    def layout(self) -> list[Rect]:
        return []

    # design to draw the node itself NOT THE CHILDREN as it will be handled by the renderer
    # target size is from the measured size
    def draw(self, target: pygame.Surface):
        pass

    # in case there is something depend on time
    def update(self, dt: int):        
        for child in self.children:
            child.update(dt)

    # We need to compare the pointer AND the hash
    # def __eq__(self, value):
    #     return self.__hash__() == value.__hash__()

    def __hash__(self):
        return hash((*self.children, self.padding))
    
    def __repr__(self):
        return f"{self.node_type}(padding={self.padding})"    

# Need to measure bounding box
# minimum size is reported itself
# while maximum size is reported by the parent
# im gonna copy jetpack compose's layout system4
# measure -> size -> placing(aka layouting) -> draw
# after measure the parent node should set the rect of the child node
# currently we are drawing children nodes immediately after measuring them and before parent node

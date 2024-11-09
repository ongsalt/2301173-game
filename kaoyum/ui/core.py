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
#  - stack alignment
#  - shadow
#  - animation
#  - High level things like button, slider, dropdown, etc

class UINode:
    _damaged: bool = True
    _hash: int | None = None
    node_type: str = "UINode"
    children: list[Self]

    def __init__(self, padding: Padding | None = None):
        self.children = []
        self.padding = padding or Padding.zero()

    # MUST BE CALL IN THIS ORDER: measure -> layout -> draw
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

    # def __setattr__(self, name, value):
    #     # Well you should not update the surface directly anyway
    #     if name not in ["_damaged", "rect"]:
    #         self._damaged = True
    #         self._hash = None # Invalidate hash
    #     return super().__setattr__(name, value)

    # @property
    # def damaged(self):
    #     return self._damaged
    
    # @damaged.setter
    # def damaged(self, value: bool):
    #     self._damaged = value    

    def __hash__(self):
        if self._hash is None:
            self._hash = self.hash()
        return self._hash
    
    def __eq__(self, value):
        return self.__hash__() == value.__hash__()

    def hash(self):
        return hash(self.children, self.padding)

class Widget(UINode):
    node_type: str = "Widget"

    def __init__(self):
        self._built: None | UINode = None

    def build(self) -> UINode:
        raise NotImplementedError

    @property
    def built(self) -> UINode:
        if self._built is None:
            self._built = self.build()
        return self._built

    def measure(self, constraints: Constraints) -> Size:
        return self.built.measure(constraints)

    def layout(self) -> list[Rect]:
        return self.built.layout()
    
    def draw(self, target):
        return self.built.draw(target)

    @property
    def padding(self):
        return self.built.padding
    
    @property
    def children(self):
        return self.built.children
    
# Need to measure bounding box
# minimum size is reported itself
# while maximum size is reported by the parent
# im gonna copy jetpack compose's layout system4
# measure -> size -> placing(aka layouting) -> draw
# after measure the parent node should set the rect of the child node
# currently we are drawing children nodes immediately after measuring them and before parent node

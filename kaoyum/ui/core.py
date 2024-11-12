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
        # w, h = self.coerce(w, h)
        # return (round(w), round(h))
        # TODO: handle infinity
        return self.coerce(w, h)

type ChildrenProp = list[Self | None] | None
class UINode:
    node_type: str = "UINode"
    children: list[Self]

    def __init__(self, children: ChildrenProp = None):
        self.children = [] if not children else [child for child in children if child is not None] 
        self._measure_cache = None
        self._measure_constraints = None

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
            # print(self, child)
            child.update(dt)

    def cached_measure(self, constraints: Constraints) -> Size:
        if self._measure_cache is None or self._measure_constraints != constraints:
            self._measure_cache = self.measure(constraints)
            self._measure_constraints = constraints
        return self._measure_cache

    # We need to compare the pointer AND the hash
    # def __eq__(self, value):
    #     return self.__hash__() == value.__hash__()

    def __hash__(self):
        return hash((*self.children, ))
    
    def __repr__(self):
        return f"{self.node_type})"    

# Need to measure bounding box
# minimum size is reported itself
# while maximum size is reported by the parent
# im gonna copy jetpack compose's layout system4
# measure -> size -> placing(aka layouting) -> draw
# after measure the parent node should set the rect of the child node
# currently we are drawing children nodes immediately after measuring them and before parent node

class WrapperNode(UINode):
    node_type: str = "WrapperNode"
    
    def __init__(self, child: UINode | None = None):
        super().__init__()
        self.children = [child] if child else []

    def measure(self, constraints: Constraints) -> Size:
        return self.children[0].measure(constraints)

    def layout(self) -> list[Rect]:
        return [Rect((0, 0), self.cached_measure(self._measure_constraints))]

    def draw(self, target: pygame.Surface):
        if self.child is not None:
            self.child.draw(target)

    @property
    def child(self):
        # refactor this
        return self.children[0] if len(self.children) == 1 else None

    @child.setter
    def child(self, value):
        if value is None:
            self.children = []
        self.children = [value]

    def __repr__(self):
        return f"{self.node_type}(children={self.child})"
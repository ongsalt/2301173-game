import pygame
from pygame import Rect
from dataclasses import dataclass
from typing import Self
from .state import State
from .animation import Animatable

# Bruh this is just Flutter

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


# TODO: 
#  - box node (with bg)
#  - click handling
#  - shadow
#  - High level things like button, slider, dropdown, etc

class UINode:
    node_type: str = "UINode"
    children: list[Self]

    def __init__(self, padding: Padding | None = None):
        self.children = []
        self.padding = padding or Padding.zero()

    # MUST BE CALL IN THIS ORDER: measure -> layout -> draw
    # well, the renderer will do that for you so you don't have to worry about it
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

    # We need to compare the pointer AND the hash
    # def __eq__(self, value):
    #     return self.__hash__() == value.__hash__()

    def __hash__(self):
        return hash((*self.children, self.padding))
    
    def __repr__(self):
        return f"{self.node_type}(padding={self.padding})"

# TODO: testing nest widget
class Widget(UINode):
    node_type: str = "Widget"
    _should_rebuild = True

    def __init__(self):
        self._built: None | UINode = None
        self._states: list[State] = []
        self._animatables: list[Animatable] = []
        self._track_state()

    def build(self) -> UINode:
        raise NotImplementedError
    
    # SUMMARY: I do this the svelte way AND the State object way
    # I have 4 choices here: 
    # 1. flutter way: extract a state to other class
    # 2. manuanlly call invalidate
    def invalidate(self):
        self._should_rebuild = True

    # 3. just force the user to use State object, btw this make animation easier
    def _track_state(self):
        for key in dir(self):
            prop = getattr(self, key)
            if isinstance(prop, State) and prop not in self._states:
                unsub = prop.subscribe(lambda _: self.invalidate()) # this binding ptsd from js
                self._states.append(prop)
                if isinstance(prop, Animatable) and prop not in self._animatables:
                    self._animatables.append(prop)

    # 4. or mark a variable as a state somehow 
    # 4.1 Svelte way: force the user to reassign the variable
    # 4.2 _states = ["variable_name", ...] which is probably the worst way to do it
    def __setattr__(self, name, value):
        if name not in ["_built", "_should_rebuild"]: 
            self.invalidate()
        return super().__setattr__(name, value)
    
    # Should be called recursively
    def update_animatables(self, dt: int):
        for animatables in self._animatables:
            animatables.update(dt)
        
        for child in self.children:
            if isinstance(child, Widget):
                child.update_animatables(dt)

    @property
    def built(self) -> UINode:
        if self._should_rebuild or self._built is None:
            self._built = self.build()
            self._should_rebuild = False
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
    
    def __hash__(self):
        return hash(self.built)
    

# Need to measure bounding box
# minimum size is reported itself
# while maximum size is reported by the parent
# im gonna copy jetpack compose's layout system4
# measure -> size -> placing(aka layouting) -> draw
# after measure the parent node should set the rect of the child node
# currently we are drawing children nodes immediately after measuring them and before parent node

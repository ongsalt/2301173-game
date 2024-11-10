from ..core import UINode, Constraints, Padding, Size, Rect, ChildrenProp
from ..state import State
from ..animation import Animatable
import pygame
from pygame import Color, Surface
from typing import Literal

# DONT DIRECTLY USE THIS CLASS
class SizedNode(UINode):
    def __init__(self, children: ChildrenProp = None, padding: Padding | None = None, width: int | None = None, height: int | None = None, fill_max_width: bool = False, fill_max_height: bool = False):
        super().__init__(padding, children)
        self.width = width
        self.height = height
        self.fill_max_width = fill_max_width
        self.fill_max_height = fill_max_height

    def measure(self, constraints: Constraints) -> Size:
        width = self.width if self.width is not None else constraints.min_width if self.fill_max_width else constraints.max_width
        height = self.height if self.height is not None else constraints.min_height if self.fill_max_height else constraints.max_height
        return constraints.coerce_and_round(width, height)

type OutlineSide = Literal["top", "bottom", "left", "right"]
type OutlineProp = bool | list[OutlineProp]
class Box(SizedNode): # More like a div
    def __init__(self, children: ChildrenProp = None, padding: Padding | None = None, width: int | None = None, height: int | None = None, fill_max_width: bool = False, fill_max_height: bool = False, background_color: Color | None = None, outline: OutlineProp = False, outline_color: Color | None = None, outline_width: int = 1):
        super().__init__(children, padding, width, height, fill_max_width, fill_max_height)
        self.background_color = background_color
        self.outline = outline
        self.outline_color = outline_color
        self.outline_width = outline_width
    
    def draw(self, target: Surface):
        target.fill(self.background_color or Color(0, 0, 0, 0))
        if self.outline:
            if isinstance(self.outline, list):
                for side in self.outline:
                    self._draw_outline(target, side)
            else:
                for side in ["top", "bottom", "left", "right"]:
                    self._draw_outline(target, side)
    
    def _draw_outline(self, target: Surface, side: OutlineSide):
        if side == "top":
            pygame.draw.rect(target, self.outline_color, Rect(0, 0, self.width, self.outline_width))
        elif side == "bottom":
            pygame.draw.rect(target, self.outline_color, Rect(0, self.height - self.outline_width, self.width, self.outline_width))
        elif side == "left":
            pygame.draw.rect(target, self.outline_color, Rect(0, 0, self.outline_width, self.height))
        elif side == "right":
            pygame.draw.rect(target, self.outline_color, Rect(self.width - self.outline_width, 0, self.outline_width, self.height))

# TODO: testing nest widget
class Widget(UINode):
    node_type: str = "Widget"

    def __init__(self):
        self._built: None | UINode = None
        self._states: list[State] = []
        self._animatables: list[Animatable] = []
        self._invalidated = True
        self._track_state()

    def build(self) -> UINode | None:
        raise NotImplementedError
    
    # SUMMARY: I do this the svelte way AND the State object way
    # I have 4 choices here: 
    # 1. flutter way: extract a state to other class
    # 2. manually call invalidate
    def invalidate(self):
        self._invalidated = True

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
        if name not in ["_built", "_invalidated"]: 
            self.invalidate()
        return super().__setattr__(name, value)
    
    def update(self, dt: int):
        for animatables in self._animatables:
            animatables.update(dt)
        
        super().update(dt)

    @property
    def built(self) -> UINode | None:
        if self._invalidated:
            self._built = self.build()
            self._invalidated = False
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

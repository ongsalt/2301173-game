from ..core import UINode, Constraints, Size, Rect, ChildrenProp, WrapperNode
from ..state import State
from ..animation import Animatable
import pygame
from pygame import Color, Surface
from typing import Literal, Self

# DONT DIRECTLY USE THIS CLASS
class SizedNode(UINode):
    def __init__(self, children: ChildrenProp = None, width: int | None = None, height: int | None = None, fill_max_width: bool = False, fill_max_height: bool = False):
        super().__init__(children)
        self.width = width
        self.height = height
        self.fill_max_width = fill_max_width
        self.fill_max_height = fill_max_height
        self._width = 0
        self._height = 0

    def measure(self, constraints: Constraints) -> Size:
        self._width = self.width if self.width is not None else constraints.min_width if not self.fill_max_width else constraints.max_width
        self._height = self.height if self.height is not None else constraints.min_height if not self.fill_max_height else constraints.max_height
        return constraints.coerce_and_round(self._width, self._height)

type OutlineSide = Literal["top", "bottom", "left", "right"]
type OutlineProp = bool | list[OutlineProp]
class Box(SizedNode): # More like a div
    def __init__(self, children: ChildrenProp = None, width: int | None = None, height: int | None = None, fill_max_width: bool = False, fill_max_height: bool = False, background_color: Color | None = None, outline: OutlineProp = False, outline_color: Color | None = None, outline_width: int = 1, border_radius: int = 0):
        super().__init__(children, width, height, fill_max_width, fill_max_height)
        self.background_color = background_color
        self.outline = outline
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.border_radius = border_radius
    
    def draw(self, target: Surface):
        w = self._width
        h = self._height
        pygame.draw.rect(target, self.background_color or Color(0, 0, 0, 0), Rect(0, 0, w, h), border_radius=self.border_radius)
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

# TODO: make child accept a builder lambda
class Widget(WrapperNode):
    node_type: str = "Widget"

    def __init__(self, child: UINode | None = None):
        super().__init__(child)
        self._dirty = True
        self._measure_cache = None
        self._measure_constraints = None

    def build(self) -> UINode | None:
        return self.child
    
    @property
    def built(self) -> UINode | None:
        if self._dirty:
            self.rebuild()
        return self.child

    def rebuild(self):
        self.child = self.build()
        self._dirty = False

    def measure(self, constraints: Constraints) -> Size:
        return self.built.cached_measure(constraints) if self.built is not None else (0, 0)
    
    def draw(self, target):
        return self.built.draw(target) if self.built is not None else None
        
    def __hash__(self):
        return hash(self.built)
    
# Well there's gonna be a massive rewrite if i do this
# so let's just leave it here
class StatefulWidget(Widget):
    node_type: str = "StatefulWidget"

    def __init__(self, child: UINode | None = None):
        super().__init__(child)
        self.state = self._initialize_state()

    def create_state(self):
        return State()

    def _initialize_state(self):
        state = self.create_state()
        return state

    # runtime can replace this state freely
    # @property
    # def built(self) -> UINode | None:
    #     if self.state._dirty:
    #         self._built = self.build()
    #         self.state._dirty = False
    #     return self._built

    
    def rebuild(self):
        super().rebuild()
        self.state._dirty = False

    def retach_state(self, state: State):
        # print(" - Retaching state")
        self.state = state
        self.state._dirty = True
    
    def __hash__(self):
        # return hash(self.built)
        return hash((self.built, self.state))
    
    def update(self, dt: int):        
        super().update(dt)
        self.state._update_animatables(dt)
    
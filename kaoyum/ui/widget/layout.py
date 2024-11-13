from math import inf, isinf
from ..core import UINode, Constraints, Size, Rect, ChildrenProp, WrapperNode
from ..state import State
from ..animation import Animatable
import pygame
from pygame import Color, Surface
from typing import Literal, Self

class SizedNode(UINode):
    def __init__(self, children: ChildrenProp = None, width: int | None = None, height: int | None = None, fill_max_width: bool = False, fill_max_height: bool = False):
        super().__init__(children)
        self.prefered_width = width
        self.prefered_height = height
        self.fill_max_width = fill_max_width
        self.fill_max_height = fill_max_height

    def measure(self) -> Constraints:
        children_constraints = [child.measure() for child in self.children]
        min_w = 0
        max_w = inf
        min_h = 0
        max_h = inf
        if self.fill_max_width:
            min_w = inf
        elif self.prefered_width is not None:
            min_w = self.prefered_width
            max_w = self.prefered_width
        else: 
            for constraint in children_constraints:
                min_w = max(min_w, constraint.min_width)
                max_w = max(max_w, constraint.max_width)

        if self.fill_max_height:
            min_h = inf
        elif self.prefered_height is not None:
            min_h = self.prefered_height
            max_h = self.prefered_height
        else:
            for constraint in children_constraints:
                min_h = max(min_h, constraint.min_height)
                max_h = max(max_h, constraint.max_height)
        
        return Constraints(min_w, min_h, max_w, max_h)
        
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
    
    def draw(self, target: Surface, size: Size):
        w, h = size
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


class Padding(WrapperNode):
    node_type: str = "Padding"
    
    def __init__(self, child: UINode = None, all = None, x = None, y = None, left = None, top = None, right = None, bottom = None):
        super().__init__(child)
        self.left = left or x or all or 0
        self.top = top or y or all or 0
        self.right = right or x or all or 0
        self.bottom = bottom or y or all or 0

    def measure(self):
        c = self.children[0].measure()
        return Constraints(c.min_width + self.left + self.right, c.min_height + self.top + self.bottom, c.max_width + self.left + self.right, c.max_height + self.top + self.bottom)

        # w, h = super().measure(constraints)
        # return w + self.left + self.right, h + self.top + self.bottom
    
    def layout(self, size) -> list[Rect]:
        w = size[0] - self.left - self.right
        h = size[1] - self.top - self.bottom
        return [Rect(self.left, self.top, w, h)]


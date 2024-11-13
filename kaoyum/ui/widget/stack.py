import pygame
from pygame import Rect, Color
from ..core import UINode, Constraints, ChildrenProp, Size
from .layout import SizedNode, Box, OutlineProp
from typing import Literal
from math import inf

type Arrangement = Literal["start", "center", "end", "between"] # im not gonna do "around" and "evenly"
type Alignment = Literal["start", "center", "end"]
# no rtl btw

class Stack(Box):
    node_type: str = "Stack"
    
    # I should think of better way to do this
    def __init__(self, children: ChildrenProp = None, width: int | None = None, height: int | None = None, fill_max_width: bool = False, fill_max_height: bool = False, background_color: Color | None = None, outline: OutlineProp = False, outline_color: Color | None = None, outline_width: int = 1, border_radius: int = 0, gap: int = 0, alignment: Alignment = "start", arrangement: Arrangement = "start", reverse: bool = False):
        super().__init__(children, width, height, fill_max_width, fill_max_height, background_color, outline, outline_color, outline_width, border_radius)
        # self.placeables: list[Rect] = []
        self.gap = gap if arrangement != "between" else 0
        self.alignment = alignment
        self.arrangement = arrangement
        self.reverse = reverse

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
                min_h = max(min_h, constraint.max_height)
                max_h = max(max_h, constraint.max_height)
        
        return Constraints(min_w, min_h, max_w, max_h)

    def layout(self, size):
        children_constraints = [child.measure() for child in self.children]
        placements: list[Rect] = []
        for constraint in children_constraints:
            w = min(constraint.min_width, size[0])
            h = min(constraint.min_height, size[1])
            if self.alignment == "start":
                x = 0
            elif self.alignment == "center":
                x = (size[0] - w) / 2
            else:
                x = size[0] - w
            if self.arrangement == "start":
                y = 0
            elif self.arrangement == "center":
                y = (size[1] - h) / 2
            else:
                y = size[1] - h
            placements.append(Rect(x, y, w, h))
        
        return placements

    def add_children(self, *children: UINode):
        self.children.extend(children)
    
    def __hash__(self):
        return hash((self.node_type, *self.children, self.alignment, self.gap))

class VStack(Stack):
    node_type: str = "VStack"

    def measure(self) -> Constraints:
        children_constraints = [child.measure() for child in self.children]
        min_w = 0
        max_w = inf
        min_h = 0 # TODO: handle scrollable
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
                min_h += constraint.min_height + self.gap
                max_h = max(max_h, constraint.max_height)
        
        return Constraints(min_w, min_h, max_w, max_h)

    def layout(self, size):
        children_constraints = [child.measure() for child in self.children]
        placements: list[Rect] = []
        # TODO: handle scrollable and reverse
        y = 0
        gap = self.calculate_gap(size[1], children_constraints)
        if self.arrangement == "end":
            content_height = sum([constraint.min_height for constraint in children_constraints]) + gap * (len(children_constraints) - 1)
            y = size[1] - content_height
        elif self.arrangement == "center":
            content_height = sum([constraint.min_height for constraint in children_constraints]) + gap * (len(children_constraints) - 1)
            y = (size[1] - content_height) / 2
        for constraint in children_constraints:
            h = constraint.min_height
            w = min(constraint.min_width, size[0])
            if self.alignment == "start":
                x = 0
            elif self.alignment == "center":
                x = (size[0] - w) / 2
            else:
                x = size[0] - w
            placements.append(Rect(x, y, w, h))
            y += h + gap

        return placements

    def calculate_gap(self, height, children_constraints: list[Constraints]):
        if self.arrangement != "between":
            return self.gap
        
        total_height = sum([constraint.min_height for constraint in children_constraints])
        total_gap = height - total_height
        return total_gap / (len(children_constraints) - 1)

class HStack(Stack):
    node_type: str = "HStack"

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
                min_w += constraint.min_width + self.gap
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

    def layout(self, size):
        children_constraints = [child.measure() for child in self.children]
        placements: list[Rect] = []
        x = 0
        gap = self.calculate_gap(size[0], children_constraints)
        if self.arrangement == "end":
            content_width = sum([constraint.min_width for constraint in children_constraints]) + gap * (len(children_constraints) - 1)
            x = size[0] - content_width
        elif self.arrangement == "center":
            content_width = sum([constraint.min_width for constraint in children_constraints]) + gap * (len(children_constraints) - 1)
            x = (size[0] - content_width) / 2
        for constraint in children_constraints:
            w = constraint.min_width
            h = min(constraint.min_height, size[1])
            if self.alignment == "start":
                y = 0
            elif self.alignment == "center":
                y = (size[1] - h) / 2
            else:
                y = size[1] - h
            placements.append(Rect(x, y, w, h))
            x += w + gap

        return placements
    
    def calculate_gap(self, width, children_constraints: list[Constraints]):
        if self.arrangement != "between":
            return self.gap
        
        total_width = sum([constraint.min_width for constraint in children_constraints])
        total_gap = width - total_width
        return total_gap / (len(children_constraints) - 1)
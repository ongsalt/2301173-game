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
        for constraint in children_constraints:
            h = constraint.min_height
            if self.alignment == "start":
                x = 0
            elif self.alignment == "center":
                x = (size.width - constraint.min_width) / 2
            else:
                x = size.width - constraint.min_width
            placements.append(Rect(x, y, size[0], h))
            y += h + gap

        return placements

    def calculate_gap(self, height, children_constraints: list[Constraints]):
        if self.arrangement != "between":
            return self.gap
        
        total_height = sum([constraint.min_height for constraint in children_constraints])
        total_gap = height - total_height
        return total_gap / (len(children_constraints) - 1)

class HStack(Stack):
    pass

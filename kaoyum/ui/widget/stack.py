import pygame
from pygame import Rect, Color
from ..core import UINode, Constraints, ChildrenProp
from .core import SizedNode, Box, OutlineProp
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
        self.placeables: list[Rect] = []
        self.gap = gap
        self.alignment = alignment
        self.arrangement = arrangement
        self.reverse = reverse

    def layout(self) -> list[Rect]:
        return self.placeables
    
    def measure(self, constraints: Constraints) -> tuple[int, int]:
        width = self.width
        height = self.height

        children_constraints = Constraints(0, 0, constraints.max_width, constraints.max_height)
        measureds = [child.cached_measure(children_constraints) for child in self.children]

        if width == None:
            content_width = max(measureds, key=lambda x: x[0], default=(0, 0))[0]
            if self.fill_max_width:
                width = constraints.max_width
            else:
                width = content_width
        
        if height == None:
            content_height = max(measureds, key=lambda x: x[1], default=(0, 0))[1]
            if self.fill_max_height:
                height = constraints.max_height
            else:
                height = content_height

        self.placeables = []

        for measured in measureds:
            w, h = measured
            if self.alignment == "start":
                x = 0     
            elif self.alignment == "center":
                x = (width - w) / 2
            else:
                x = width - w

            if self.arrangement == "start":
                y = 0
            elif self.arrangement == "center":
                y = (height - h) / 2
            elif self.arrangement == "end":
                y = height - h
            else:
                raise ValueError("Stack does not support 'between' arrangement")

            self.placeables.append(Rect(x, y, w, h))
            
        self._width = width
        self._height = height
        return constraints.coerce_and_round(width, height)

    def add_children(self, *children: UINode):
        self.children.extend(children)
    
    def __hash__(self):
        return hash((self.node_type, *self.children, self.alignment, self.gap))

class VStack(Stack):
    node_type: str = "VStack"
    def measure(self, constraints: Constraints) -> tuple[int, int]:
        width = self.width
        height = self.height
        children = self.children if not self.reverse else reversed(self.children)

        children_constraints = Constraints(0, 0, constraints.max_width, inf)
        measureds = [child.cached_measure(children_constraints) for child in children]

        content_height = sum(map(lambda x: x[1], measureds)) + max(self.gap * (len(self.children) - 1), 0) if self.arrangement != "between" else constraints.max_height

        if width == None:
            content_width = max(measureds, key=lambda x: x[0], default=(0, 0))[0]
            if self.fill_max_width:
                width = constraints.max_width
            else:
                width = content_width
            
        if height == None:
            if self.fill_max_height:
                height = constraints.max_height
            else:
                height = content_height

        self.placeables = []
        gap = self.gap

        if self.arrangement == "start":
            y = 0
        elif self.arrangement == "center":
            y = (height - content_height) / 2
        elif self.arrangement == "end":
            y = height - content_height
        else: # between
            y = 0
            gap = (height - sum(h for w, h in measureds)) / (len(self.children) - 1)

        for measured in measureds:
            w, h = measured
            if self.alignment == "start":
                x = 0     
            elif self.alignment == "center":
                x = (width - w) / 2
            else:
                x = width - w

            self.placeables.append(Rect(x, y, w, h))
            y += h + gap

        if self.reverse:
            self.placeables.reverse()

        self._width = width
        self._height = height
        return constraints.coerce_and_round(width, height)
                
class HStack(Stack):
    node_type: str = "HStack"

    def measure(self, constraints: Constraints) -> tuple[int, int]:
        width = self.width
        height = self.height
        children = self.children if not self.reverse else reversed(self.children)

        children_constraints = Constraints(0, 0, constraints.max_width, inf)
        measureds = [child.cached_measure(children_constraints) for child in children]

        content_width = sum(map(lambda x: x[0], measureds)) + max(self.gap * (len(self.children) - 1), 0) if self.arrangement != "between" else constraints.max_width

        if width == None:
            if self.fill_max_width:
                width = constraints.max_width
            else:
                width = content_width
        
        if height == None:
            content_height = max(measureds, key=lambda x: x[1], default=(0, 0))[1]
            if self.fill_max_height:
                height = constraints.max_height
            else:
                height = content_height

        self.placeables = []
        gap = self.gap

        if self.arrangement == "start":
            x = 0
        elif self.arrangement == "center":
            x = (width - content_width) / 2
        elif self.arrangement == "end":
            x = width - content_width
        else: # between
            x = 0
            gap = (width - sum(w for w, h in measureds)) / (len(self.children) - 1)

        for measured in measureds:
            w, h = measured
            if self.alignment == "start":
                y = 0    
            elif self.alignment == "center":
                y = (height - h) / 2
            else:
                y = height - h

            self.placeables.append(Rect(x, y, w, h))
            x += w + gap

        if self.reverse:
            self.placeables.reverse()

        self._width = width
        self._height = height
        return constraints.coerce_and_round(width, height)

import pygame
from pygame import Rect
from kaoyum.ui.core import UINode, Constraints, Padding
from typing import Literal
from math import inf

type Arrangement = Literal["start", "center", "end", "between"] # im not gonna do "around" and "evenly"
type Alignment = Literal["start", "center", "end"]
# no rtl btw

class Stack(UINode):
    node_type: str = "Stack"
    def __init__(self, padding: Padding | None = None, gap: int = 0, alignment: Alignment = "start", arrangement: Arrangement = "start", children: list[UINode] = [], fill_max_width: bool = False, fill_max_height: bool = False, reverse: bool = False):
        super().__init__()
        self.children = children
        self.placeables: list[Rect] = []
        self.padding = padding or Padding.zero()
        self.gap = gap
        self.alignment = alignment
        self.arrangement = arrangement
        self.fill_max_width = fill_max_width
        self.fill_max_height = fill_max_height
        self.reverse = reverse

    def layout(self) -> list[Rect]:
        return self.placeables
    
    def measure(self, constraints: Constraints) -> tuple[int, int]:
        children_constraints = Constraints(0, 0, constraints.max_width, constraints.max_height)
        measureds = [child.measure(children_constraints) for child in self.children]

        content_width = max(measureds, key=lambda x: x[0])[0]
        content_height = sum(map(lambda x: x[1], measureds)) + max(self.gap * (len(self.children) - 1), 0) if self.arrangement != "between" else constraints.max_height

        if self.fill_max_width:
            width = constraints.max_width
        else:
            width = content_width + self.padding.width
        
        if self.fill_max_height:
            height = constraints.max_height
        else:
            height = content_height + self.padding.height

        self.placeables = []
        gap = self.gap

        if self.arrangement == "start":
            y = self.padding.top
        elif self.arrangement == "center":
            y = (height - content_height) / 2
        elif self.arrangement == "end":
            y = height - content_height
        else: # between
            y = self.padding.top
            gap = (height - content_height) / (len(self.children) - 1)

        for measured in measureds:
            w, h = measured
            if self.alignment == "start":
                x = self.padding.left     
            elif self.alignment == "center":
                x = (width - w) / 2
            else:
                x = width - w

            if self.arrangement == "start":
                y = self.padding.top     
            elif self.arrangement == "center":
                y = (height - h) / 2
            elif self.arrangement == "end":
                y = height - h
            else:
                raise ValueError("Stack does not support 'between' arrangement")

            self.placeables.append(Rect(x, y, w, h))
            
        return constraints.coerce(width, height)

    def add_children(self, *children: UINode):
        self.children.extend(children)
    
    def __hash__(self):
        return hash((self.node_type, *self.children, self.padding, self.alignment, self.gap))

class VStack(Stack):
    node_type: str = "VStack"
    def measure(self, constraints: Constraints) -> tuple[int, int]:
        children_constraints = Constraints(0, 0, constraints.max_width, inf)
        measureds = [child.measure(children_constraints) for child in self.children]

        content_width = max(measureds, key=lambda x: x[0])[0]
        content_height = sum(map(lambda x: x[1], measureds)) + max(self.gap * (len(self.children) - 1), 0) if self.arrangement != "between" else constraints.max_height

        if self.fill_max_width:
            width = constraints.max_width
        else:
            width = content_width + self.padding.width
        
        if self.fill_max_height:
            height = constraints.max_height
        else:
            height = content_height + self.padding.height

        self.placeables = []
        gap = self.gap

        if self.arrangement == "start":
            y = self.padding.top
        elif self.arrangement == "center":
            y = (height - content_height) / 2
        elif self.arrangement == "end":
            y = height - content_height
        else: # between
            y = self.padding.top
            gap = (height - content_height) / (len(self.children) - 1)

        for measured in measureds:
            w, h = measured
            if self.alignment == "start":
                x = self.padding.left     
            elif self.alignment == "center":
                x = (width - w) / 2
            else:
                x = width - w

            self.placeables.append(Rect(x, y, w, h))

            if self.reverse:
                y -= h + gap
            else:
                y += h + gap

        return constraints.coerce(width, height)
        
class HStack(Stack):
    node_type: str = "HStack"

    def measure(self, constraints: Constraints) -> tuple[int, int]:
        children_constraints = Constraints(0, 0, constraints.max_width, inf)
        measureds = [child.measure(children_constraints) for child in self.children]

        content_height = max(measureds, key=lambda x: x[1])[1]
        content_width = sum(map(lambda x: x[0], measureds)) + max(self.gap * (len(self.children) - 1), 0) if self.arrangement != "between" else constraints.max_width

        if self.fill_max_width:
            width = constraints.max_width
        else:
            width = content_width + self.padding.width
        
        if self.fill_max_height:
            height = constraints.max_height
        else:
            height = content_height + self.padding.height

        self.placeables = []
        gap = self.gap

        if self.arrangement == "start":
            x = self.padding.left
        elif self.arrangement == "center":
            x = (width - content_width) / 2
        elif self.arrangement == "end":
            x = width - content_width
        else: # between
            x = self.padding.left
            gap = (width - content_width) / (len(self.children) - 1)

        for measured in measureds:
            w, h = measured
            if self.alignment == "start":
                y = self.padding.top     
            elif self.alignment == "center":
                y = (height - h) / 2
            else:
                y = height - h

            self.placeables.append(Rect(x, y, w, h))

            if self.reverse:
                x -= w + gap
            else:
                x += w + gap

        return constraints.coerce(width, height)

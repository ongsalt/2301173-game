import pygame
from pygame import Rect
from kaoyum.ui.core import UINode, Constraints, Padding
from typing import Literal
from math import inf

type Alignment = Literal["start", "center", "end", "between"]

# TODO: redraw only the damaged children
class Stack(UINode):
    def __init__(self, padding: Padding | None = None, gap: int = 0, alignment: Alignment = "start", children: list[UINode] = []):
        super().__init__()
        self.children = children
        self.placeables: list[tuple[UINode, Rect]] = []
        self.padding = padding or Padding.zero()
        self.gap = gap
        self.alignment = alignment

    def layout(self, area: Rect):
        self.rect = area
        x, y = area.topleft
        for node, target in self.placeables:
            node.layout(Rect(target.x + x, target.y + y, target.width, target.height))

    def add_children(self, *children: UINode):
        self.children.extend(children)
        self.damaged = True

    @property
    def damaged(self):
        self._damaged |= any(child.damaged for child in self.children)
        return self._damaged

class VStack(Stack):
    def measure(self, constraints: Constraints) -> tuple[int, int]:
        # TODO: handle alignment here
        children_constraints = Constraints(0, 0, constraints.max_width, inf)
        self.placeables = []
        y = self.padding.top
        for child in self.children:
            w, h = child.measure(children_constraints)
            # x, y = child.offset
            target = Rect(self.padding.left, y, w, h)
            y += h + self.gap
            self.placeables.append((child, target))

        width = max(self.placeables, key=lambda x: x[1].width)[1].width + self.padding.width
        height = sum(map(lambda x: x[1].height, self.placeables)) + max(self.gap * (len(self.children) - 1), 0) + self.padding.height
        return constraints.coerce(width, height)
        
class HStack(Stack):
    def measure(self, constraints: Constraints) -> tuple[int, int]:
        # TODO: handle alignment here
        children_constraints = Constraints(0, 0, constraints.max_width, inf)
        self.placeables = []
        x = self.padding.left
        for child in self.children:
            w, h = child.measure(children_constraints)
            # x, y = child.offset
            target = Rect(x, self.padding.top, w, h)
            x += w + self.gap
            self.placeables.append((child, target))

        height = max(self.placeables, key=lambda x: x[1].height)[1].height + self.padding.width
        width = sum(map(lambda x: x[1].width, self.placeables)) + max(self.gap * (len(self.children) - 1), 0) + self.padding.height
        return constraints.coerce(width, height)


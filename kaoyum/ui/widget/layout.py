from .core import SizedNode, WrapperNode
from ..core import Constraints
from pygame import Rect
from math import isinf

class Padding(WrapperNode):
    node_type: str = "Padding"
    
    def __init__(self, child = None, all = None, x = None, y = None, left = None, top = None, right = None, bottom = None):
        super().__init__(child)
        self.left = left or x or all or 0
        self.top = top or y or all or 0
        self.right = right or x or all or 0
        self.bottom = bottom or y or all or 0

    def measure(self, constraints):
        min_width = constraints.min_width
        min_height = constraints.min_height
        max_width = (constraints.max_width - self.left - self.right) if not isinf(constraints.max_width) else constraints.max_width
        max_height = (constraints.max_height - self.top - self.bottom) if not isinf(constraints.max_height) else constraints.max_height
        c = Constraints(min_width, min_height, max_width, max_height)
        w, h = self.children[0].measure(c)
        # if not isinf(constraints.max_width):
        #     w -= self.left + self.right
        # if not isinf(constraints.max_height):
        #     h -= self.top + self.bottom
        self._w = w
        self._h = h
        return (w + self.left + self.right, h + self.top + self.bottom)

        # w, h = super().measure(constraints)
        # return w + self.left + self.right, h + self.top + self.bottom
    
    def layout(self) -> list[Rect]:
        return [Rect(self.left, self.top, self._w, self._h)]


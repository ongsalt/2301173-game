from .core import WrapperNode
from pygame import Rect

class Padding(WrapperNode):
    node_type: str = "Padding"
    
    def __init__(self, child = None, left = 0, top = 0, right = 0, bottom = 0):
        super().__init__(child)
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
    
    def measure(self, constraints):
        w, h = super().measure(constraints)
        return (w + self.left + self.right, h + self.top + self.bottom)
    
    def layout(self) -> list[Rect]:
        return [Rect((self.left, self.top), self.cached_measure(self._measure_constraints))]


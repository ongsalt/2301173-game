from math import inf
from pygame import Surface
from pygame import Rect
from dataclasses import dataclass
from typing import Self

# TODO: 
#  - click handling: GestureDetector
#  - shadow
#  - High level things like button, slider, dropdown, etc

type Size = tuple[int, int]

@dataclass(frozen=True)
class Constraints:
    min_width: float = 0
    min_height: float = 0
    max_width: float = inf
    max_height: float = inf

    def coerce(self, w: int, h: int) -> Size:
        w = max(min(w, self.max_width), self.min_width)
        h = max(min(h, self.max_height), self.min_height)
        return (w, h)
    
    def coerce_and_round(self, w: float, h: float) -> Size:
        # w, h = self.coerce(w, h)
        # return (round(w), round(h))
        # TODO: handle infinity
        return self.coerce(w, h)

type ChildrenProp = list[Self | None] | None
class UINode:
    node_type: str = "UINode"
    children: list[Self]

    def __init__(self, children: ChildrenProp = None):
        self.children = [] if not children else [child for child in children if child is not None] 
    
    def measure(self) -> Constraints:
        return Constraints()

    # return the relative position of each child node
    def layout(self, size: Size) -> list[Rect]:
        return []

    # design to draw the node itself NOT THE CHILDREN as it will be handled by the renderer
    # target size is from the measured size
    def draw(self, target: Surface, size: Size):
        pass

    # in case there is something depend on time
    # TODO: call this in the runtime
    def update(self, dt: int):        
        pass

    def __hash__(self):
        return hash((*self.children, ))
    
    def children_hash(self):
        return hash((*self.children, ))

    def __repr__(self):
        return f"{self.node_type}"    

class WrapperNode(UINode):
    node_type: str = "WrapperNode"
    
    def __init__(self, child: UINode | None = None):
        super().__init__()
        self.children = [child] if child else []

    def measure(self) -> Constraints:
        return self.child.measure()

    def layout(self, size: Size) -> list[Rect]:
        return [
            Rect((0, 0), size)
        ]
    
    @property
    def child(self):
        # refactor this
        return self.children[0] if len(self.children) == 1 else None

    @child.setter
    def child(self, value):
        if value is None:
            self.children = []
        self.children = [value]

    def __repr__(self):
        return f"{self.node_type}(*)"
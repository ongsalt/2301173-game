from math import inf
from ..core import UINode, Constraints, Size, Rect, ChildrenProp, WrapperNode
from ..state import State

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
        return self.built.measure(constraints) if self.built is not None else (0, 0)
    
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
    
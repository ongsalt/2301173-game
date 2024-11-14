from math import inf
from ..core import UINode, Constraints, Size, Rect, ChildrenProp, WrapperNode
from ..state import State

# TODO: make child accept a builder lambda
# THIS MUST HAVE ONLY ONE CHILD 
# generally you should build the child in the build method and not temper with UINode.children
class Widget(WrapperNode):
    node_type: str = "Widget"

    def __init__(self, child: UINode | None = None):
        super().__init__(child)

    def build(self) -> UINode | None:
        return self.child
    
    def rebuild(self):
        self.child = self.build()
        return self.child

    def measure(self) -> Constraints:
        return self.child.measure() if self.child is not None else Constraints(0, 0, inf, inf)
    
    def draw(self, target, size: tuple[int, int]):
        pass
        
    def __hash__(self):
        return hash((*self.children, self.node_type))
    
# Well there's gonna be a massive rewrite if i do this
# so let's just leave it here
class StatefulWidget(Widget):
    node_type: str = "StatefulWidget"

    def __init__(self, child: UINode | None = None):
        super().__init__(child)
        self.state = None
        self._initialized = False

    def create_state(self):
        return State()

    def _initialize_state(self):
        self._initialized = True
        self.state = self.create_state()
        return self.state
    
    def __hash__(self):
        # return hash(self.built)
        # Problem is hash got called before the state is reattached
        return hash((*self.children, self.state))
    
    def update(self, dt: int):   
        super().update(dt)
        # print(self._initialized)
        self.state._update_animatables(dt)

    def __repr__(self):
        return f"{self.node_type}(state={self.state})"
    
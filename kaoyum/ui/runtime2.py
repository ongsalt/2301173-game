import pygame
from pygame import Rect, Surface
from pygame.event import Event
from typing import Self
from itertools import zip_longest
from kaoyum.utils import add
from .core import UINode, Constraints
from .widget.core import Widget, StatefulWidget
from .state import State
from .widget.input import GestureHandler
from ..assets_manager import AssetsManager

# it mean we will have to diff these trees 3 times
# Definitions Tree -> Reattach State (rebuild if needed) -> Layout (handling event????) -> Composite 
# TODO: Event handling: set a listener to some rect area and call the callback if the event is in the rect area
# Definitions:
#   - from build() method
# State reattaching:
#   - Should call create state() method of StatefulWidget
#   - extract state from StatefulWidget and store it in StateNode
#   - reattach the state to the StatefulWidget with the same key if any or else same position 
# Layouting:
#   - how to layout the nodes
#   - children report their constraints to the parent (measure() will not take any argument)
#   - parent decides the children's size and position
#   - fill_max_size handling: constraints.min_size = inf
#   - PARENT UI NODE MUST REPORT THE CHILDREN PLACEMENT after it's got it's size determined : layout(w, h)
#     - must take fill_max_size into account (via min_size inf)

# Node list:
#   - UINode
#   - UIText
#   - SizedNode
#   - Box
#   - Stack
    #   - VStack
    #   - HStack
#   - StatefulWidget
#   - GestureHandler
class RenderTextureRegistry:
    # TODO: texture recycling
    pass

class ImmediateNode:
    def __init__(self, ui_node: UINode):
        self.ui_node = ui_node
        self.state: State | None = None
        self.surface = None
        self.absolute_rect: Rect | None = None
        self.children: list[ImmediateNode] = []
        self.dirty = True

    def resize(self, size: tuple[int, int]):
        # TODO: check if we can reuse the surface 
        if self.surface is None:
            print("[ImmediateNode] Creating new surface")
            self.surface = Surface(size, pygame.SRCALPHA, 32)
        elif self.surface.get_size() != size:
            # TextureRegistry.recycle(self.surface)
            print("[ImmediateNode] Resizing immediate node")
            self.surface = Surface(size, pygame.SRCALPHA, 32)
        # check node type before reattaching the state

    def set_nth_child(self, child: Self, index: int):
        if index == len(self.children):
            self.children.append(child)
        elif index < len(self.children):
            self.children[index] = child
        else:
            raise IndexError("Index out of range")
    
    def dispose_since(self, index: int):
        for i in range(len(self.children) - 1, index, -1):
            del self.children[i]

    def reuse(self, ui_node: UINode, state: State | None = None):
        self.ui_node = ui_node
        self.state = state
        self.absolute_rect = None
        self.dirty = True
        self.children = []

    def blit_to(self, target: Surface):
        position = self.absolute_rect.topleft
        if self.dirty:
            self.surface.fill((0, 0, 0, 0))
            self.ui_node.draw(self.surface, self.absolute_rect.size)
            print(f"[composite] Redrawing {self.ui_node.node_type}")
        self.dirty = False
        
        target.blit(self.surface, position, Rect((0, 0), self.absolute_rect.size))

class UIRuntime2:
    def __init__(self, root: Widget, size: tuple[int, int], draw_bound: bool = False):
        self.root_node = root
        self.root_immediate_node = None
        self.draw_bound = draw_bound
        self.size = size
        self.screen = Surface(size, pygame.SRCALPHA, 32)

    def init(self):
        self.diff_and_reattach_state()
        self.layout()
        self.composite()

    def diff_and_reattach_state(self):
        def traverse(ui_node: UINode, immediate_node: ImmediateNode | None = None, path = "@", skippable = True) -> ImmediateNode:
            is_stateful = isinstance(ui_node, StatefulWidget)
            dirty = False
            if immediate_node is None:
                print(f"[diff] {path} Creating new immediate node")
                immediate_node = ImmediateNode(ui_node)
                dirty = True
            else:
                # print(f"[diff] {path} Reusing immediate node")
                pass
            
            if is_stateful:
                # TODO: check node typ
                if immediate_node.state is not None:
                    print(f"[diff] {path} Reattaching state")
                    ui_node.state = immediate_node.state
                    dirty = immediate_node.state._dirty
                    if dirty:
                        print(f"[diff] {path} State changed: {immediate_node.state}")
                    immediate_node.state._dirty = False
                else:
                    print(f"[diff] {path} Creating a new state")
                    immediate_node.state = ui_node._initialize_state()
                
            if hash(ui_node) != hash(immediate_node.ui_node) or dirty:    
                if is_stateful:
                    print(f"[diff] {path} Rebuilding")
                    ui_node.rebuild() # TODO: dont rebuild if state is the same
                    
                immediate_node.dirty = True
                    # immediate_node.reuse(ui_node)
            else:
                # print(f"[diff] {path} same hash: Skipping")
                return immediate_node

            # skippable = skippable and not is_stateful
            print(f"[diff] {path} is different: Rebuilding")
            for index, (ui, immediate) in enumerate(zip_longest(ui_node.children, immediate_node.children)):
                if ui is None:
                    break
                immediate_child = traverse(ui, immediate, f"{path}/{index}")
                print(immediate_child.ui_node)
                immediate_node.set_nth_child(immediate_child, index)
            immediate_node.dispose_since(len(ui_node.children))

            immediate_node.ui_node = ui_node
            return immediate_node

        self.root_immediate_node = traverse(self.root_node, self.root_immediate_node)

    def layout(self):
        def traverse(immediate_node: ImmediateNode, size: tuple[int, int], offset: tuple[int, int], path = "@"):
            if not immediate_node.dirty:
                # print(f"[layout] {path} {immediate_node.absolute_rect} {immediate_node.ui_node.node_type} is not dirty: Skipping")
                return
            immediate_node.absolute_rect = Rect(offset, size)
            immediate_node.resize(size)
            childden_placements = immediate_node.ui_node.layout(size)

            # print(f"[layout] {path} {immediate_node.absolute_rect} {childden_placements}")

            if len(childden_placements) != len(immediate_node.children):
                raise ValueError("WTF: Children placements must be the same as children count")

            for index, (immediate, placement) in enumerate(zip(immediate_node.children, childden_placements)):
                traverse(immediate, placement.size, add(placement.topleft, offset), f"{path}/{index}")
        
        # determine root node placement
        width, height = self.size
        if self.root_immediate_node is not None:
            constraints = self.root_immediate_node.ui_node.measure()
            width = min(constraints.max_width, self.size[0])
            height = min(constraints.max_height, self.size[1])
        traverse(self.root_immediate_node, (width, height), (0, 0))

    def composite(self):
        def traverse(immediate_node: ImmediateNode, path = "@"):
            immediate_node.blit_to(self.screen)
            if self.draw_bound:
                pygame.draw.rect(self.screen, (255, 0, 0), immediate_node.absolute_rect, 1)
            for index, child in enumerate(immediate_node.children):
                traverse(child, f"{path}/{index}")
                
        self.screen.fill((0, 0, 0, 0))
        traverse(self.root_immediate_node)

    def print_tree(self):
        def traverse(immediate_node: ImmediateNode, path = ""):
            print(f"{path} {immediate_node.ui_node}")
            for index, child in enumerate(immediate_node.children):
                traverse(child, f"{path}  ")
                
        traverse(self.root_immediate_node)

    def run(self, screen: Surface, dt = 1000 /60, position: tuple[int, int] = (0, 0), events: list[Event] | None = None):
        self.diff_and_reattach_state()
        self.layout()
        # self.print_tree()
        self.composite()

        screen.blit(self.screen, position)

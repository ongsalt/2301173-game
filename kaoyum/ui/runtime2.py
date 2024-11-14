import pygame
from pygame import Rect, Surface, Color
from pygame.event import Event
from typing import Self
from itertools import zip_longest
from kaoyum.utils import add, Singleton
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
#   - GestureHandler
class RenderTextureRegistry(metaclass=Singleton):
    def __init__(self):
        self.registry: dict[str, Surface] = {}
        self.recycled: list[Surface] = []

    def get(self, key: str, size: tuple[int, int], strict=False) -> Surface:
        if key not in self.registry:
            self.registry[key] = Surface(size, pygame.SRCALPHA, 32)

        surface_size = self.registry[key].get_size()
        self.registry[key] = self.reuse_or_create(size, strict)

        return self.registry[key]
    
    def reuse_or_create(self, size: tuple[int, int], strict=False) -> Surface:
        for surface in self.recycled:
            surface_size = surface.get_size()
            if strict:
                if surface_size == size:
                    self.recycled.remove(surface)
                    surface.fill((0, 0, 0, 0))
                    return surface
            else:
                if surface_size[0] >= size[0] and surface_size[1] >= size[1]:
                    self.recycled.remove(surface)
                    surface.fill((0, 0, 0, 0))
                    return surface

        return Surface(size, pygame.SRCALPHA, 32)
    
    def recycle(self, surface: Surface):
        self.auto_dispose()
        self.recycled.append(surface)

    def auto_dispose(self):
        if len(self.recycled) > 50:
            for surface in self.recycled:
                del surface

class IntermediateNode:
    def __init__(self, ui_node: UINode):
        self.ui_node = ui_node
        self.state: State | None = None
        self.surface = None
        self.absolute_rect: Rect | None = None # well, it's still relative to runtime root node
        self.children: list[IntermediateNode] = []
        self.previous_hash: int | None = None
        self.dirty = True

    def resize(self, size: tuple[int, int]):
        # TODO: check if we can reuse the surface 
        if self.surface is None:
            # print("[composite] Creating new surface")
            self.surface = RenderTextureRegistry().reuse_or_create(size)
        elif self.surface.get_size() != size:
            # print("[composite] Resizing intermediate node")
            RenderTextureRegistry().recycle(self.surface)
            self.surface = RenderTextureRegistry().reuse_or_create(size)
            self.dirty = True
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
        self.previous_hash = None

    # this should be in the runtime
    def render_to(self, target: Surface):
        position = self.absolute_rect.topleft
        if self.dirty:
            self.surface.fill((0, 0, 0, 0))
            self.ui_node.draw(self.surface, self.absolute_rect.size)
            # print(f"[composite] Redrawing {self.ui_node}")
        self.dirty = False
        
        target.blit(self.surface, position, Rect((0, 0), self.absolute_rect.size))

class UIRuntime2:
    def __init__(self, root: Widget, size: tuple[int, int], draw_bound: bool = False, bound_color: Color | None = None, lazy: bool = False):
        self.root_node = root
        self.root_intermediate_node = None
        self.draw_bound = draw_bound
        self.bound_color = bound_color or (255, 0, 0)
        self.size = size
        self.screen = Surface(size, pygame.SRCALPHA, 32)
        if not lazy:
            self.diff_and_reattach_state(0)
            self.layout()
            self.composite()

    def diff_and_reattach_state(self, dt = 1000 / 60):
        def traverse(ui_node: UINode, intermediate_node: IntermediateNode | None = None, path = "@") -> IntermediateNode:
            nonlocal dt
            is_stateful = isinstance(ui_node, StatefulWidget)
            dirty = False
            if intermediate_node is None:
                print(f"[diff] {path} Creating new intermediate node")
                intermediate_node = IntermediateNode(ui_node)
                dirty = True
            else:
                # print(f"[diff] {path} Reusing intermediate node")
                pass
            
            if is_stateful:
                # TODO: check node typ
                if intermediate_node.state is not None:
                    # print(f"[diff] {path} Reattaching state")
                    ui_node.state = intermediate_node.state
                    dirty = intermediate_node.state._dirty
                    if dirty:
                        print(f"[diff] {path} State changed: {intermediate_node.state}")
                        pass
                    intermediate_node.state._dirty = False
                else:
                    # print(f"[diff] {path} Initializing a new state for {ui_node.node_type}")
                    intermediate_node.state = ui_node._initialize_state()
                    print(f"[diff] {path} State initialized: {ui_node.state}")
                    print(f"[diff] {intermediate_node.ui_node}")
                    dirty = True

                # print(f"[diff] {path} {ui_node} is stateful")
                
            ui_node_hash = hash(ui_node)
            if ui_node_hash == intermediate_node.previous_hash and not dirty:   
                # print(f"[diff] {path} {ui_node} same hash: Skipping")
                return intermediate_node
 
            intermediate_node.dirty = True
            intermediate_node.previous_hash = ui_node_hash
            intermediate_node.ui_node = ui_node

            if is_stateful:
                # print(f"[diff] {path} Rebuilding")
                ui_node.rebuild() # TODO: dont rebuild if state is the same
                    
                    # intermediate_node.reuse(ui_node)
            # skippable = skippable and not is_stateful
            print(f"[diff] {path} {ui_node} is different: Rebuilding")
            for index, (ui, intermediate) in enumerate(zip_longest(ui_node.children, intermediate_node.children)):
                if ui is None:
                    break
                intermediate_child = traverse(ui, intermediate, f"{path}/{index}")
                intermediate_node.set_nth_child(intermediate_child, index)
            intermediate_node.dispose_since(len(ui_node.children))

            return intermediate_node

        self.root_intermediate_node = traverse(self.root_node, self.root_intermediate_node)

    def update(self, dt: int):
        def traverse(intermediate_node: IntermediateNode, path = "@"):
            nonlocal dt
            for index, child in enumerate(intermediate_node.children):
                traverse(child, f"{path}/{index}")
            intermediate_node.ui_node.update(dt)
            # print(f"[update] {path} {intermediate_node.ui_node.node_type} {intermediate_node.state}")
                
        traverse(self.root_intermediate_node)

    def layout(self):
        def traverse(intermediate_node: IntermediateNode, size: tuple[int, int], offset: tuple[int, int], path = "@", skippable = True):
            # print(f"[layout] {path} {intermediate_node.ui_node.node_type} {size} {offset}")
            new_rect = Rect(offset, size)
            same_size = intermediate_node.absolute_rect == new_rect
            if not intermediate_node.dirty and same_size:
                # print(f"[layout] {path} {intermediate_node.absolute_rect} {intermediate_node.ui_node.node_type} is not dirty: Skipping")
                return
            intermediate_node.absolute_rect = new_rect
            intermediate_node.resize(size)
            childden_placements = intermediate_node.ui_node.layout(size)
            # print(f"[layout] {path} {intermediate_node.absolute_rect} {childden_placements}")
            if len(childden_placements) != len(intermediate_node.children):
                raise ValueError("WTF: Children placements must be the same as children count")

            for index, (intermediate, placement) in enumerate(zip(intermediate_node.children, childden_placements)):
                traverse(intermediate, placement.size, add(placement.topleft, offset), f"{path}/{index}")
        
        # determine root node placement
        width, height = self.size
        if self.root_intermediate_node is not None:
            constraints = self.root_intermediate_node.ui_node.measure()
            width = min(constraints.max_width, self.size[0])
            height = min(constraints.max_height, self.size[1])
        traverse(self.root_intermediate_node, (width, height), (0, 0))

    def composite(self):
        def traverse(intermediate_node: IntermediateNode, path = "@"):
            intermediate_node.render_to(self.screen)
            if self.draw_bound:
                pygame.draw.rect(self.screen, self.bound_color, intermediate_node.absolute_rect, 1)
            for index, child in enumerate(intermediate_node.children):
                traverse(child, f"{path}/{index}")
                
        self.screen.fill((0, 0, 0, 0))
        traverse(self.root_intermediate_node)

    def print_tree(self, root: UINode):
        def traverse(ui_node: UINode, path = ""):
            print(f"{path} {ui_node}")
            for index, child in enumerate(ui_node.children):
                traverse(child, f"{path}  ")
                
        traverse(root)

    def print_tree2(self, root: IntermediateNode):
        def traverse(node: IntermediateNode, path = ""):
            print(f"{path} {node.ui_node.node_type} {node.state}")
            # if isinstance(node.ui_node, StatefulWidget):
                # print(f"{path} - {node.ui_node.state}")
            for index, child in enumerate(node.children):
                traverse(child, f"{path}  ")
                
        traverse(root)

    def handle_events(self, events: list[Event], offset: tuple[int, int] = (0, 0)) -> list[Event]:
        def traverse(intermediate_node: IntermediateNode, events: list[Event], path = "@") -> list[Event]:
            nonlocal offset
            for index, child in enumerate(intermediate_node.children):
                events = traverse(child, events, f"{path}/{index}")
            if isinstance(intermediate_node.ui_node, GestureHandler):
                for event in reversed(events):
                    if self.is_event_inside(event, intermediate_node.absolute_rect, offset):
                    # if intermediate_node.absolute_rect.collidepoint(event.pos):
                        consumed = intermediate_node.ui_node.handle_event(event)
                        if consumed:
                            events.remove(event)
                    else:
                        intermediate_node.ui_node.handle_outside_event(event)
            return events

        return traverse(self.root_intermediate_node, events)
    
    def is_event_inside(self, event: Event, rect: Rect, offset: tuple[int, int]) -> bool:
        if not hasattr(event, "pos"):
            return False
        return Rect(add(rect.topleft, offset), rect.size).collidepoint(event.pos)

    def run(self, screen: Surface, dt = 1000 /60, position: tuple[int, int] = (0, 0), events: list[Event] | None = None) -> list[Event]:
        # start_time = pygame.time.get_ticks()
        self.diff_and_reattach_state(dt)
        self.update(dt)
        # self.print_tree2(self.root_intermediate_node)

        self.layout()
        self.composite()
        unconsumed_events = self.handle_events(events[:] if events is not None else [], offset=position)
        screen.blit(self.screen, position)

        # raise ValueError("Stop")
        # print("=====================================")
        end_time = pygame.time.get_ticks()

        return unconsumed_events

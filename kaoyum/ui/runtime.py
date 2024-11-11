import pygame
from pygame import Rect
from pygame.event import Event
from typing import Self
from itertools import zip_longest
from kaoyum.utils import add
from .core import UINode, Constraints
from .widget.core import Widget, StatefulWidget
from .state import State
from .widget.input import GestureHandler

# i should just do tree transformation and be done with everything

# Should be UINodeImmediateWhatever
class UINodeTexture:
    def __init__(self, size: tuple[int, int], node: UINode | None = None):
        self.node = node
        self.state = None
        self.surface = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.children: list[UINodeTexture] = []
        self.render_hash: None | int = None
        self.size = size
    
    def resize(self, size: tuple[int, int]):
        if not self.can_contain(size):
            self.surface = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.size = size

    def can_contain(self, size: tuple[int, int]):
        return self.actual_size[0] >= size[0] and self.actual_size[1] >= size[1]
    
    @property
    def actual_size(self):
        return self.surface.get_size()
    
    def clear(self):
        self.surface.fill((0, 0, 0, 0))

    def set_nth_child(self, texture: Self, index: int):
        if index == len(self.children):
            self.children.append(texture)
        elif index < len(self.children):
            self.children[index] = texture
        else:
            raise IndexError("Index out of range")
    
    def dispose_since(self, index: int):
        # TODO: test this
        for i in range(len(self.children) - 1, index, -1):
            del self.children[i]

    def blit_to(self, target: pygame.Surface, position: tuple[int, int]):
        target.blit(self.surface, position, Rect((0, 0), self.size))
        
    def __repr__(self):
        return f"Texture(size={self.size}, node={self.node})"

class Compositor:
    def __init__(self, size: tuple[int, int], root: Widget, draw_bound: bool = False):
        self.size = size
        self.root = root
        self.screen = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.constraints = Constraints(0, 0, size[0], size[1])
        self.draw_bound = draw_bound

        # Should remove the none variant
        self.root_texture: UINodeTexture | None = None

    def draw_to(self, screen: pygame.Surface, position: tuple[int, int]):
        screen.blit(self.screen, position)

    # it's not only rendering anymore
    def render(self) -> UINodeTexture:
        def traverse(node: UINode, old_texture: None | UINodeTexture, path: str = "/") -> UINodeTexture:
            # print(f"Traversing [{path}]: {node}")

            # TODO: reattach lost state
            size = node.cached_measure(self.constraints)
            # we can keep the old texture if the size is the larger than needed
            if old_texture is None:
                # print("Creating new texture")
                texture = UINodeTexture(size, node)
            else:
                # print("Reusing texture")
                old_texture.resize(size)
                texture = old_texture

            render_hash = hash(node)
            is_stateful = isinstance(node, StatefulWidget)

            if is_stateful:
                if texture.state is None:
                    texture.state = node.state
                    # print(f"Caching state [{node.state._invalidation_marker}]")
                else:
                    # render_hash == texture.render_hash
                    if texture.state._invalidation_marker != node.state._invalidation_marker:
                        # print(f"Reusing state [{node.state._invalidation_marker}] [{texture.state._invalidation_marker}]")
                        # TODO: think about node insertion, deletion and reordering
                        # probably gonna need a node type and Keyed
                        node.retach_state(texture.state) 
                        node.rebuild()

            texture.node = node
            
            # we should invalidate the hash here but it likely would never collide 
            if is_stateful and node.state._dirty:
                # print(f"Rebuilding [{path}, {render_hash}]: {node}")
                node.rebuild()

            if render_hash == texture.render_hash:
                return texture

            texture.clear()
            node.draw(texture.surface)
            print(f"Rendering [{path}, {render_hash}]: {node}")
            texture.render_hash = render_hash

            old_children = old_texture.children if old_texture is not None else []
            for i, (child, node_texture) in enumerate(zip_longest(node.children, old_children)):
                if child is None:
                    break
                child_texture = traverse(child, node_texture, f"{path}{i}/")
                texture.set_nth_child(child_texture, i)
            texture.dispose_since(len(node.children))
            
            return texture
    
        old_root_texture = self.root_texture
        self.root_texture = traverse(self.root, old_root_texture)
        return self.root_texture 

    def composite(self, events: list[Event], global_offset: tuple[int, int]):
        def traverse(texture: UINodeTexture, offset: tuple[int, int]) -> bool:
            nonlocal global_offset, events
            for event in reversed(events):
                if isinstance(texture.node, GestureHandler): 
                    if self.is_event_inside(event, Rect(offset, texture.size), global_offset):
                            # print("GestureHandler") 
                        # print(f"Event inside {texture.node}")
                        consumed = texture.node.handle_event(event)
                    else:
                        consumed = texture.node._on_mouse_leave(event)
                    if consumed:
                        events.remove(event)
                    # Will be handled by the outermost node

            placeables = texture.node.layout()
            # print(f"Compositing {texture.node} at {offset}")
            # We can skip this if the node is gauranteed to not overlap
            # which will be mark from parent node
            # self.screen.fill((0, 0, 0, 0), Rect(offset, texture.size))
            if self.draw_bound:
                pygame.draw.rect(self.screen, (0, 255, 0), Rect(offset, texture.actual_size), 1)
                pygame.draw.rect(self.screen, (255, 0, 0), Rect(offset, texture.size), 1)
            self.screen.blit(texture.surface, offset)

            for child, rect in zip(texture.children, placeables):
                traverse(child, add(offset, rect.topleft))

        self.screen.fill((0, 0, 0, 0))
        traverse(self.root_texture, (0, 0))

    def is_event_inside(self, event: Event, rect: Rect, global_offset: tuple[int, int]) -> bool:
        if not hasattr(event, "pos"):
            return False
        
        x, y = event.pos
        rect.x += global_offset[0]
        rect.y += global_offset[1]
        return rect.collidepoint(x, y)

    def run(self, screen: pygame.Surface, position: tuple[int, int] = (0, 0), events: list[Event] | None = None):
        self.render() # actually this will do the diffing and it will redraw the damaged part

        self.composite(events or [], position)
        
        screen.blit(self.screen, position)


class UIRuntime:
    def __init__(self, root: Widget, size: tuple[int, int], draw_bound: bool = False):
        self.root = root
        self.compositor = Compositor(size, self.root, draw_bound)
        self.draw_bound = draw_bound
        self.compositor.render()

    def run(self, screen: pygame.Surface, position: tuple[int, int] = (0, 0), events: list[Event] | None = None, dt: int = 1000/60):
        self.root.update(dt)
        # should i build the event listener tree
        self.compositor.run(screen, position, events)

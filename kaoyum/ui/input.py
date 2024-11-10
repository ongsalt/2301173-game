from dataclasses import dataclass
from pygame.event import Event
from typing import Callable
import pygame
from core import Widget

@dataclass
class MouseEventHandler:
    on_hover: Callable[[tuple[int, int]]] | None = None
    on_click: Callable[[tuple[int, int]]] | None = None
    on_release: Callable[[tuple[int, int]]] | None = None

    def handle_event(self, event: Event, area: pygame.Rect) -> bool: # indicate if the event is consumed
        pos = pygame.mouse.get_pos()
        if not area.collidepoint(pos):
            return False
        if event.type == pygame.MOUSEMOTION and self.on_hover:
            self.on_hover(pos)
            return True
        elif event.type == pygame.MOUSEBUTTONDOWN and self.on_click:
            self.on_click(pos)
            return True
        elif event.type == pygame.MOUSEBUTTONUP and self.on_release:
            self.on_release(pos)
            return True
        return False
    
class GestureDetector(Widget):
    def __init__(self, child: Widget, on_tap: Callable[[tuple[int, int]]] = lambda _: None):
        self.child = child
        self.on_tap = on_tap

    def build(self):
        return self.child
    
    def handle_event(self, event: Event, area: pygame.Rect) -> bool:
        return self.event_handler.handle_event(event, area) or self.child.handle_event(event, area)

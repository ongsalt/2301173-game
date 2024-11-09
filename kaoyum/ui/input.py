from dataclasses import dataclass
from pygame.event import Event
from typing import Callable
import pygame

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
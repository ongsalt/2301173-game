from pygame import Surface
from pygame.locals import *
from pygame.event import Event

# TODO: cache rendered surface
class Scene:
    def __init__(self, size: tuple[int, int]):
        self._event_queue = []
        
    def run(self, display: Surface, dt: int = 1000/60, events: list[Event] | None = None) -> list[Event]: # return the events that are not consumed
        for event in reversed(events or []):
            if self.handle_event(event):
                events.remove(event)

    
    def handle_event(self, event: Event) -> bool:
        return False

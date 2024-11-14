from pygame import Surface
from pygame.locals import *
from pygame.event import Event
from kaoyum.game import Game


class Scene:
    def run(self, display: Surface, dt: int = 1000/60, events: list[Event] | None = None) -> list[Event]: # return the events that are not consumed
        pass
        # for event in reversed(events or []):
        #     if self.handle_event(event):
        #         events.remove(event)


class GameplayScene(Scene):
    def __init__(self, size: tuple[int, int]):
        self.game = Game(size)
        
    def run(self, display: Surface, dt: int = 1000/60, events: list[Event] | None = None):
        # print(dt)
        self.game.run(display, dt)
    
    def handle_event(self, event: Event):
        if event.type == KEYDOWN:
            # print(event)
            if event.key == 32:
                self.game.start()

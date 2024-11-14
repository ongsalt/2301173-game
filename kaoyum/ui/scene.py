from pygame import Surface
from pygame.locals import *
from pygame.event import Event
from kaoyum.game import Game

from .widget.home import HomeUI

class Scene:
    def run(self, display: Surface, dt: int = 1000/60, events: list[Event] | None = None) -> list[Event]: # return the events that are not consumed
        pass
        # for event in reversed(events or []):
        #     if self.handle_event(event):
        #         events.remove(event)

class GameplayScene(Scene):
    def __init__(self, size: tuple[int, int]):
        self.game = Game(size)
        self.home_ui = HomeUI(size)
        
    def run(self, display: Surface, dt: int = 1000/60, events: list[Event] | None = None):
        for event in reversed(events or []):
            if self.handle_event(event):
                events.remove(event)
        self.game.run(display, dt)
        self.home_ui.update(dt=dt, is_game_started=self.game.is_started)

        self.home_ui.draw(display)
    
    def handle_event(self, event: Event):
        if event.type == KEYDOWN:
            # print(event)
            if event.key == 32:
                self.game.start()
                return True
            
        return False

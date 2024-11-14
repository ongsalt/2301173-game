from pygame.surface import Surface
from pygame.event import Event
from pygame import KEYDOWN, KEYUP
from .scene import Scene
from .home import HomeUI
from .gameplay import StatusUI
from kaoyum.game import Game
from kaoyum.ui import UIRuntime, State
from kaoyum.ui.widget import StatefulWidget, Stack

class GameOverlay(StatefulWidget):
    def create_state(self):
        return State()
    
    def build(self):
        return Stack(
            children=[
                HomeUI(),
                StatusUI()
            ]
        )

class GameplayScene(Scene):
    def __init__(self, size: tuple[int, int]):
        super().__init__(size)
        self.game = Game(size)
        self.status_ui = GameOverlay()
        self.ui_runtime = UIRuntime(
            root=self.status_ui,
            size=size,
            # draw_bound=True
        )
        
    def update_status(self):
        # print(f"{self.status_ui}")
        self.status_ui.state.score = self.game.score

    def run(self, display: Surface, dt: int = 1000/60, events: list[Event] | None = None):
        # print(dt)
        self.game.run(display, dt)
        self.update_status()
        events = self.ui_runtime.run(display, dt=dt, events=events)
        for event in events:
            self.handle_event(event)
    
    def handle_event(self, event: Event):
        if event.type == KEYDOWN:
            # print(event)
            if event.key == 32:
                self.game.start()

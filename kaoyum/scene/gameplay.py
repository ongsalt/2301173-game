from .scene import Scene
from kaoyum.game import Game
from pygame.surface import Surface
from pygame.event import Event
from kaoyum.ui import State, Loop, UIRuntime2
from kaoyum.ui.widget import StatefulWidget, Stack, HStack, Padding, VStack, UIText

class StatusUIState(State):
    def __init__(self):
        super().__init__()
        self.text_opacity = Loop(150, 220, angular_frequency=0.2)
        self.score = 0

class StatusUI(StatefulWidget):
    state: StatusUIState

    def create_state(self):
        return StatusUIState()

    def build(self):
        return Padding(
            left=12,
            right=12,
            top=12,
            child=HStack(
                arrangement="between",
                fill_max_width=True,
                children=[
                    Stack(
                        width=300,
                        height=6,
                        background_color=(0, 0, 0, 100)
                    ),
                    UIText(f"{self.state.score}", size=20, color=(0, 0, 0, 200)),
                ]
            )     
        )

class GameplayScene(Scene):
    def __init__(self, size: tuple[int, int]):
        super().__init__(size)
        self.game = Game(size)
        self.status_ui = StatusUI()
        self.ui_runtime = UIRuntime2(
            root=self.status_ui,
            size=size,
            # draw_bound=True
        )
        
    def update_status(self):
        # print(f"{self.status_ui}")
        self.status_ui.state.score = self.game.score

    def run(self, display: Surface, dt: int = 1000/60, events: list[Event] | None = None):
        self.game.run(display, dt)
        self.update_status()
        events = self.ui_runtime.run(display, dt=dt, events=events)
        for event in events:
            self.game.handle_event(event)
    
    def copy(self):
        return GameplayScene(self.x, self.y) 

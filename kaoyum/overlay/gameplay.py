from .scene import Scene
from kaoyum.game import Game
from pygame.surface import Surface
from pygame.event import Event
from kaoyum.ui import State, Loop, UIRuntime
from kaoyum.ui.widget import StatefulWidget, Stack, HStack, Padding, VStack, UIText
from .home import HomeUI

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
    

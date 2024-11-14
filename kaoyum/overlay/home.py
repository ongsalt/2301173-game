from pygame.locals import K_SPACE, KEYDOWN
from pygame import Surface
from pygame.event import Event, post as post_event
from kaoyum.ui import UIRuntime, Loop, State
from kaoyum.ui.widget import StatefulWidget, VStack, UIText, Stack, Image, Box, Padding

class HomeUIState(State):
    def __init__(self):
        super().__init__()
        self.selected_index = 0
        self.text_opacity = Loop(150, 220, angular_frequency=0.2)

class HomeUI(StatefulWidget):
    state: HomeUIState

    def __init__(self):
        super().__init__()

    def create_state(self):
        return HomeUIState()

    def build(self):
        state = self.state
        return Stack(
            children=[
                Padding(
                    all=12,
                    child=Stack(
                        alignment="center",
                        arrangement="center",
                        fill_max_width=True,
                        fill_max_height=True,
                        children=[
                            Stack(
                                alignment="center",
                                arrangement="end",
                                fill_max_width=True,
                                fill_max_height=True,
                                gap=30,
                                children=[
                                    UIText("Press space to begin", size=18, color=(255, 255, 255, state.text_opacity.rounded)),
                                ]
                            ),
                            VStack(
                                gap=10,
                                alignment="center",
                                children=[
                                    UIText("Game Title", size=40),
                                    Box(
                                        height=1,
                                        width=200,
                                        background_color=(255, 255, 255, 100),
                                    ),
                                    UIText("Some random text", size=18)
                                ]
                            ),
                            VStack(
                                alignment="end",
                                arrangement="end",
                                fill_max_width=True,
                                fill_max_height=True,
                                gap=6,
                                children=[
                                    UIText("Settings", size=18),
                                    UIText("Exit", size=18)
                                ]
                            )    
                        ]
                    )
                ),
            ]
        )

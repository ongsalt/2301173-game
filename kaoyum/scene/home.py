from pygame.locals import K_SPACE, KEYDOWN
from pygame import Surface
from pygame.event import Event, post as post_event
from kaoyum.ui import UIRuntime2, Loop, State
from kaoyum.ui.widget import StatefulWidget, VStack, UIText, Stack, Image, Box, Padding
from kaoyum.ui.event import NavigationEvent
from .scene import Scene

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
                Image("bg.800x600.jpg"),
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

class HomeScene(Scene):
    def __init__(self, size: tuple[int, int]):
        super().__init__(size)
        self.ui = HomeUI()
        self.ui_runtime = UIRuntime2(
            draw_bound=True,
            root=self.ui,
            size=size
        )

    def run(self, display: Surface, dt: int = 1000/60, events: list[Event] | None = None):
        super().run(display, dt, events)
        display.fill((0, 0, 0))
        self.ui_runtime.run(display, dt=dt, events=self._event_queue)
    
    def handle_event(self, event) -> bool:
        if event.type == KEYDOWN:
            key = event.dict["key"]
            if key == K_SPACE:
                post_event(NavigationEvent("game"))
                # fire a navigation event
                return True
        #     if key == K_s or key == K_DOWN:
        #         self.ui.selected_index = (self.ui.selected_index + 1) % 3
        #     elif key == K_w or key == K_UP:
        #         self.ui.selected_index = (self.ui.selected_index - 1) % 3
        #     elif key == K_RETURN or key == K_SPACE:
        #         if self.ui.selected_index == 0:
        #             return "to:game"
        #         elif self.ui.selected_index == 1:
        #             return "to:settings"
        #         elif self.ui.selected_index == 2:
        #             return "exit"

from .core import StatefulWidget
from typing import Callable
from .input import GestureHandler
from .stack import Stack
from .text import UIText
from ..animation import Spring
from ..core import Padding
from ..state import State

class ButtonState(State):
    def __init__(self):
        super().__init__()
        self.opacity = Spring(20)
        self.on_mouse_leave()
    
    def on_mouse_enter(self):
        self.opacity.animate_to(40)
    
    def on_mouse_leave(self):
        self.opacity.animate_to(20)

    def on_mouse_up(self):
        self.opacity.animate_to(40)

    def on_mouse_down(self):
        self.opacity.animate_to(80)

    @property
    def background_color(self): 
        return (0, 0, 0, self.opacity.value)

class Button(StatefulWidget):
    node_type: str = "Button"
    state: ButtonState

    def __init__(self, text: str, on_click: Callable[[], None] = None):
        super().__init__()
        self.text = text
        self.on_click = on_click

    def create_state(self):
        return ButtonState()

    def build(self):
        return GestureHandler(
            on_click=lambda pos: self._on_click(pos),
            on_mouse_up=lambda pos: self.state.on_mouse_up(),
            on_mouse_enter=lambda _: self.state.on_mouse_enter(),
            on_mouse_leave=lambda _: self.state.on_mouse_leave(),
            child=Stack(
                alignment="center",
                arrangement="center",
                background_color=self.state.background_color,
                border_radius=8,
                children=[
                    UIText(self.text, padding=Padding.all(10)),
                ]
            )
        )
    
    def _on_click(self, pos):
        self.state.on_mouse_down()
        if self.on_click:
            self.on_click(pos)


if __name__ == "__main__":
    from kaoyum.ui import UIRuntime, UIText, VStack, StatefulWidget
    import pygame

    class ExampleState(State):
        def __init__(self):
            super().__init__()
            self.show = False

        def toggle(self):
            self.show = not self.show

    class ExampleWidget(StatefulWidget):
        node_type: str = "ExampleWidget"
        state: ExampleState

        def __init__(self):
            super().__init__()

        def create_state(self):
            return ExampleState()
                
        def build(self):
            return VStack(
                gap=10,
                fill_max_width=True,
                fill_max_height=True,
                children=[
                    UIText("Bottom text", size=18),
                    Button(
                        "Click me",
                        on_click=lambda pos: self.state.toggle()
                    ),
                    UIText("Hello World", size=30) if self.state.show else None,
                ]
            )

    pygame.init()
    clock = pygame.time.Clock()
    DISPLAY_SIZE = (800, 600)
    screen = pygame.display.set_mode(DISPLAY_SIZE)

    widget = ExampleWidget()
    ui = UIRuntime(
        size=(600, 400),
        # draw_bound=True,
        root=widget
    )

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    surface = pygame.Surface((100, 100))
    surface.fill((255, 0, 0))

    while True:
        dt = clock.tick(60)
        unprocessed_events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()                

            unprocessed_events.append(event)

        screen.fill((16, 163, 240))
        ui.run(screen, dt=dt, position=(100, 100), events=unprocessed_events)

        pygame.display.flip()

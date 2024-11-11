from kaoyum.ui.state import State
from .core import Widget, StatefulWidget
from ..core import UINode, WrapperNode
from  typing import Callable
from pygame.event import Event
from pygame.locals import MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP

class GestureHandlerState(State):
    def __init__(self):
        super().__init__()
        self.is_mouse_over = False

type Handler = Callable[[tuple[int, int]], None] | None

# I should make a StatefulWrapper
class GestureHandler(StatefulWidget):
    node_type: str = "GestureHandler"
    state: GestureHandlerState # TODO: maybe we can use this type information to implement the default state creation in the base class

    def __init__(self, child: UINode, on_click: Handler = None, on_mouse_up: Handler = None, on_mouse_enter: Handler = None, on_mouse_leave: Handler = None):
        super().__init__(child)
        self.on_click = on_click
        self.on_mouse_enter = on_mouse_enter
        self.on_mouse_leave = on_mouse_leave
        self.on_mouse_up = on_mouse_up
        # To implement this, gesturehandler must be a stateful widget

    def create_state(self) -> GestureHandlerState:
        return GestureHandlerState()

    def handle_event(self, event: Event) -> bool:
        if not hasattr(event, "pos"):
            return False
        if event.type == MOUSEMOTION:
            if not self.state.is_mouse_over:
                self.state.is_mouse_over = True
                if self.on_mouse_enter:
                    self.on_mouse_enter(event.pos)
                    return True
        elif event.type == MOUSEBUTTONDOWN:
            if self.on_click:
                print("Mouse clicked")
                self.on_click(event.pos)
                return True
        elif event.type == MOUSEBUTTONUP:
            if self.on_mouse_up:
                self.on_mouse_up(event.pos)
                return True
            
        return False

    def _on_mouse_leave(self, event: Event):
        if self.state.is_mouse_over:
            self.state.is_mouse_over = False
            if self.on_mouse_leave:
                self.on_mouse_leave(event)

    def __hash__(self):
        return hash((self.child, self.on_click, self.on_mouse_enter, self.on_mouse_leave, self.on_mouse_up))
    
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
                    GestureHandler(
                        UIText("Click me", size=30),
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
        draw_bound=True,
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

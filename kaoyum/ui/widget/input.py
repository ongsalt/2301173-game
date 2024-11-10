from .common import Widget
from ..core import UINode
from  typing import Callable

class GestureHandler(Widget):
    node_type: str = "GestureHandler"

    def __init__(self, child: UINode, on_tap: Callable[[tuple[int, int]], None] | None = None):
        self.child = child
        super().__init__()
        self.on_tap = on_tap

    def build(self) -> UINode:
        return self.child
    
if __name__ == "__main__":
    from kaoyum.ui import Spring, UIRuntime, UIText, VStack
    import pygame

    class ExampleWidget(Widget):
        def __init__(self):
            self.show = False
            super().__init__()
        
        def toggle(self):
            self.show = not self.show

        def build(self):
            return VStack(
                gap=10,
                fill_max_width=True,
                fill_max_height=True,
                children=[
                    GestureHandler(
                        UIText("Click me", size=30),
                        on_tap=lambda pos: self.toggle()
                    ),
                    UIText("Hello World", size=30) if self.show else None,
                    UIText("Bottom text", size=18),
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

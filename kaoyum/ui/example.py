from kaoyum.ui import UIRuntime, StatefulWidget, Spring, Padding, VStack, HStack, UIText, State, Button
import pygame
    
class ExampleState(State):
    def __init__(self):
        super().__init__()
        self.time: int = 0
        self.y_padding = Spring(0)

class ExampleWidget(StatefulWidget):
    state: ExampleState

    def create_state(self):
        return ExampleState()

    def build(self):
        return VStack(
            gap=10,
            # padding=Padding(0, 0, 0, 24),
            fill_max_width=True,
            fill_max_height=True,
            alignment="center",
            arrangement="center",
            children=[
                UIText(f"from svelte style state: {self.state.time}", size=24),
                UIText("Text 2"),
                HStack(
                    gap=25,
                    reverse=True,
                    alignment="center",
                    arrangement="end",
                    fill_max_width=True,
                    children=[
                        UIText("1"),
                        UIText("Hello World"),
                        VStack(
                            width=240,
                            height=80,
                            alignment="end",
                            children=[
                                UIText("Nested 1"),
                                UIText("Nested ashufguyafkhk"),
                            ]
                        ),
                        Button(
                            text="Click me",
                            on_click=lambda _: print("Clicked")
                        )
                    ]
                ),
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

while True:
    dt = clock.tick(60)
    unprocessed_events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()                

        unprocessed_events.append(event)

    widget.state.time += dt

    screen.fill((16, 163, 240))
    ui.run(screen, dt=dt, position=(100, 100), events=unprocessed_events)

    pygame.display.flip()
    
from kaoyum.ui import UIRuntime2, Spring, State
from kaoyum.ui.widget import StatefulWidget, VStack, UIText, HStack, Button, Padding
import pygame
    
class ExampleState(State):
    def __init__(self):
        super().__init__()
        self.time: int = 0
        self.y_padding = Spring(0)
        self.expanded = False

    def toggle(self):
        self.expanded = not self.expanded
        self.y_padding.animate_to(42 if self.expanded else 0)

    def __repr__(self):
        return f"ExampleState(time={self.time}, expanded={self.expanded})"

class ExampleWidget(StatefulWidget):
    state: ExampleState

    def create_state(self):
        return ExampleState()

    def build(self):
        return VStack(
            gap=10,
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
                                Padding(
                                    all=10,
                                    child=UIText("Nested ashufguyafkhk"),
                                )
                            ]
                        ),
                        # Button(
                        #     text="Expand" if not self.state.expanded else "Collapse",
                        #     on_click=lambda _: self.state.toggle()
                        # ),
                    ]
                ),
                UIText(
                    "Hello World", 
                    # Holy shit, antialiasing is non existent
                    # TODO: decimal position -> delegate the decimal position to draw_offset
                    # padding=Padding(right=self.state.y_padding.value * 4, top=self.state.y_padding.value), 
                    size=self.state.y_padding.value + 18
                ),
            ]
        )

pygame.init()
clock = pygame.time.Clock()
DISPLAY_SIZE = (800, 600)
screen = pygame.display.set_mode(DISPLAY_SIZE)

widget = ExampleWidget()
ui = UIRuntime2(
    size=(600, 400),
    draw_bound=True,
    root=widget
)

ui.init()

while True:
    dt = clock.tick(60)
    unconsumed_events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()                

        unconsumed_events.append(event)


    # print(1/dt * 1000)
    widget.state.time += dt
    screen.fill((16, 163, 240))
    ui.run(screen, dt=dt, position=(100, 100), events=unconsumed_events)

    pygame.display.flip()
    
from kaoyum.ui import UINode
import pygame
from .widget import VStack, UIText, HStack
from .runtime2 import UIRuntime2

pygame.init()
clock = pygame.time.Clock()
DISPLAY_SIZE = (800, 600)
screen = pygame.display.set_mode(DISPLAY_SIZE)

widget = VStack(
    gap=10,
    fill_max_width=True,
    fill_max_height=True,
    alignment="center",
    arrangement="center",
    children=[
        UIText(f"from svelte style state", size=24),
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
            size=18
        ),
    ]
)

ui = UIRuntime2(
    root=widget,
    size=(600, 400),
    draw_bound=True
)

while True:
    dt = clock.tick(60)
    unconsumed_events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()                

        unconsumed_events.append(event)

    # print(1/dt * 1000)
    screen.fill((16, 163, 240))
    ui.run(screen, dt=dt, position=(100, 100), events=unconsumed_events)

    pygame.display.flip()
    
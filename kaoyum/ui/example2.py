from kaoyum.ui import UINode
import pygame
from .widget import VStack, UIText
from .runtime2 import UIRuntime2

pygame.init()
clock = pygame.time.Clock()
DISPLAY_SIZE = (800, 600)
screen = pygame.display.set_mode(DISPLAY_SIZE)

widget = VStack(
    children=[
        UIText("Hello World"),
        UIText("Hello World"),
        # UIText("Hello World"),
        # UIText("Hello World"),
        # UIText("Hello World"),
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
    
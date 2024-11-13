from kaoyum.ui import UINode
import pygame

pygame.init()
clock = pygame.time.Clock()
DISPLAY_SIZE = (800, 600)
screen = pygame.display.set_mode(DISPLAY_SIZE)

node = UINode()

while True:
    dt = clock.tick(120)
    unconsumed_events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()                

        unconsumed_events.append(event)

    widget.state.time += dt

    # print(1/dt * 1000)
    screen.fill((16, 163, 240))
    ui.run(screen, dt=dt, position=(100, 100), events=unconsumed_events)

    pygame.display.flip()
    
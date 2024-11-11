from kaoyum.ui import UIRuntime, DirtyStatefulWidget, StatefulWidget, Spring, Padding, VStack, HStack, UIText, State
import pygame

# class ExampleWidget(DirtyStatefulWidget):
#     def __init__(self):
#         super().__init__()
#         self.time = 0
#         self.y_padding = Spring(0)
#         self._track_state()

#     def build(self):
#         return VStack(
#             gap=10,
#             padding=Padding(0, 0, 0, 24),
#             fill_max_width=True,
#             fill_max_height=True,
#             alignment="center",
#             arrangement="center",
#             children=[
#                 UIText(f"from svelte style state: {self.time}", size=24),
#                 UIText("Text 2"),
#                 HStack(
#                     gap=25,
#                     reverse=True,
#                     alignment="center",
#                     arrangement="end",
#                     fill_max_width=True,
#                     children=[
#                         UIText("1"),
#                         UIText("Hello World"),
#                         VStack(
#                             width=240,
#                             height=80,
#                             alignment="end",
#                             children=[
#                                 UIText("Nested 1"),
#                                 UIText("Nested ashufguyafkhk"),
#                             ]
#                         ),
#                     ]
#                 ),
#                 UIText(f"State object: click to change {self.y_padding.value}", padding=Padding(top=self.y_padding.value)),
#                 UIText(f"texture reusing", padding=Padding(top=self.y_padding.value / 2)),
#             ]
#         )

# from kaoyum.ui.widget.text import UIText
# from kaoyum.ui.widget.stack import VStack, HStack

# pygame.init()
# clock = pygame.time.Clock()
# DISPLAY_SIZE = (800, 600)
# screen = pygame.display.set_mode(DISPLAY_SIZE)

# widget = ExampleWidget()
# ui = UIRuntime(
#     size=(600, 400),
#     draw_bound=True,
#     root=widget
# )

# while True:
#     dt = clock.tick(60)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()

#         if event.type == pygame.MOUSEBUTTONDOWN:
#             widget.y_padding.animate_to(0 if widget.y_padding.final_position == 100 else 100)

#     widget.time += dt

#     screen.fill((16, 163, 240))
#     ui.run(screen, dt=dt, position=(100, 100))

#     pygame.display.flip()
    
class ExampleState(State):
    def __init__(self):
        super().__init__()
        self.time: int = 0
        self.y_padding = Spring(0)

class ExampleWidget(StatefulWidget):
    def __init__(self):
        super().__init__()
        self.state = ExampleState()

    def build(self):
        return VStack(
            gap=10,
            padding=Padding(0, 0, 0, 24),
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
    draw_bound=True,
    root=widget
)

while True:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    widget.state.time += dt

    screen.fill((16, 163, 240))
    ui.run(screen, dt=dt, position=(100, 100))

    pygame.display.flip()
    
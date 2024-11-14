import pygame
from kaoyum.ui.widget import Widget

class Button(Widget):
    def __init__(self, text, on_click=None):
        super().__init__()
        self.text = text
        self.on_click = on_click

    def draw(self, screen):
        # Draw button
        pass

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.on_click:
                self.on_click()
    
    def select(self):
        pass
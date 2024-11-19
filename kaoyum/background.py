from pygame import Surface
import pygame
from .assets_manager import AssetsManager

class Background:
    def __init__(self, size: tuple[int, int]):
        self.size = size
        self.layers = [
            self._load_image("background/Layer_0000_9.png"),
            self._load_image("background/Layer_0001_8.png"),
            self._load_image("background/Layer_0002_7.png"),
            self._load_image("background/Layer_0003_6.png"),
            self._load_image("background/Layer_0004_Lights.png"),
            self._load_image("background/Layer_0005_5.png"),
            self._load_image("background/Layer_0006_4.png"),
            self._load_image("background/Layer_0007_Lights.png"),
            self._load_image("background/Layer_0008_3.png"),
            self._load_image("background/Layer_0009_2.png"),
            self._load_image("background/Layer_0010_1.png"),
            self._load_image("background/Layer_0011_0.png"),
        ]
        self.layers.reverse()
        self.x_offset = 0
        self.y_offset = self.layers[0].get_size()[1] - size[1] - 20
        self.layer_size = self.layers[0].get_size()

    def _load_image(self, path: str) -> Surface:
        image =  AssetsManager().get(path)
        scale = self.size[1] / image.get_size()[1] * 2
        image = pygame.transform.scale_by(image, scale)
        return image.convert_alpha()

    def draw(self, screen: Surface):
        i = 11
        for layer in self.layers:
            offset = (self.x_offset // (i + 1)) % self.layer_size[0]
            screen.blit(layer, (0, 0), (offset, self.y_offset, self.size[0], self.size[1]))
            if offset > self.layer_size[0] - self.size[0]:
                end_x = self.layer_size[0] - offset
                width = self.size[0] - end_x
                screen.blit(layer, (end_x, 0), (0, self.y_offset, width, self.size[1]))
            i -= 1
    
    def update(self, dt: int):
        self.x_offset += 0.2 * dt

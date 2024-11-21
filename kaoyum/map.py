from typing import Literal
from pygame import SRCALPHA, Rect, Surface
from kaoyum.block import Block
from kaoyum.obstacle import Obstacle
from kaoyum.scorepoint import Scorepoint
from kaoyum.color_changer import ColorChanger
from kaoyum.assets_manager import AssetsManager
from kaoyum.utils import tint

# Google factory pattern for more information

def bird(x: int, y: int, variant = 1) -> Obstacle:
    return Obstacle(
        x=x,
        y=y,
        damage=10,
        image=AssetsManager().get(f"Bird/Bird{variant}.png", (48, 48)),
        hitbox=Rect(0, 18, 48, 30),
    )

def bat(x: int, y: int, variant = 1) -> Obstacle:
    return Obstacle(
        x=x,
        y=y,
        damage=10,
        image=AssetsManager().get(f"Bat/Bat{variant}.png", (48, 48)),
    )

def plane(x: int, y: int) -> Obstacle:
    return Obstacle(
        x=x,
        y=y,
        damage=100,
        image=AssetsManager().get(f"Plane/plane.png", (271, 181)),
        hitbox=Rect(0, 70, 271, 40),
    )

def coin(x: int, y: int, color: Literal["red", "green", "blue"] = "red") -> Scorepoint:
    return Scorepoint(
        x=x,
        y=y,
        width=32,
        height=32,
        score=10,
        color=color,
        image=AssetsManager().get(f"Coins/{color}.png", (32, 32)),
    )

def color_changer(x: int, color: str) -> ColorChanger:
    return ColorChanger(
        x=x,
        color=color,
    )

def _load_color_changer_image(color: str):
    for i in range(1, 10):
        image = AssetsManager().get(f"Effects/{color}/row-26-column-{i}.png")
        surface = Surface((64, 600), SRCALPHA, 32)
        surface.fill((0, 0, 0, 0))
        y = 0
        while y < 600 + image.get_height():
            y += image.get_height()
            surface.blit(image, (0, y - image.get_height()))
            # print(y)

        AssetsManager().set(f"ColorChanger/{color}-{i}.png", surface.convert_alpha())


def initialize_blocks():
    SCREEN_WIDTH = 800
    default_coin = AssetsManager().get("Coins/1.png")
    AssetsManager().set("Coins/red.png", tint(default_coin, (255, 100, 100)))
    AssetsManager().set("Coins/green.png", tint(default_coin, (100, 255, 100)))
    AssetsManager().set("Coins/blue.png", tint(default_coin, (100, 130, 255)))

    _load_color_changer_image("red")
    _load_color_changer_image("green")
    _load_color_changer_image("blue")

    return [
        Block(
            obstacles=[
                bird(0, 100),
                bat(200, 120),
                plane(400, 0),
            ],
            score_points=[
                coin(600, 400, "red"),
                coin(640, 400, "red"),
                coin(680, 400, "red"),
                coin(200, 540, "green"),
                coin(240, 540, "green"),
                coin(280, 540, "green"),
            ],
            color_changers=[
                color_changer(800, "red"),
            ],
            offset=SCREEN_WIDTH
        ),
        Block(
            obstacles=[
                bat(0, 100 + 300),
                bird(200, 120 + 300),
                bat(400, 100),
                bird(600, 100 + 300),
            ],
            score_points=[
                coin(40, 320, "blue"),
                coin(80, 320, "blue"),
                coin(120, 320, "blue"),
            ],
            color_changers=[],
            offset=SCREEN_WIDTH
        ),
        Block(
            obstacles=[
                plane(0, 0),
                plane(0, 200),
                plane(0, 400),
                plane(0, 600),
            ],
            score_points=[
                coin(200 + 300, 120, "green"),
                coin(200 + 340, 120, "green"),
                coin(200 + 380, 120, "green"),
                coin(200 + 420, 120, "green"),
                coin(200 + 460, 120, "green"),
                coin(200 + 300, 150, "blue"),
                coin(200 + 340, 150, "blue"),
                coin(200 + 380, 150, "blue"),
                coin(200 + 420, 150, "blue"),
                coin(200 + 460, 150, "blue"),
                coin(200 + 300, 180, "red"),
                coin(200 + 340, 180, "red"),
                coin(200 + 380, 180, "red"),
                coin(200 + 420, 180, "red"),
                coin(200 + 460, 180, "red"),
            ],
            color_changers=[
                color_changer(800, "blue"),
            ],
            offset=SCREEN_WIDTH
        ),
        Block(
            obstacles=[
                plane(0, -50),
                plane(0, 100),
                plane(0, 300),
                plane(0, 500),
            ],
            score_points=[
                coin(450, 120, "green"),
                coin(490, 120, "red"),
                coin(530, 120, "blue"),
            ],
            color_changers=[
                color_changer(800, "green"),
            ],
            offset=SCREEN_WIDTH
        ),
        Block(
            obstacles=[
                bird(100 + 0, 600),
                bird(100 + 40, 560),
                bird(100 + 80, 520),
                bird(100 + 120, 480),
                bird(100 + 160, 440),
            ],
            color_changers=[],
            offset=SCREEN_WIDTH,
            score_points=[
                coin(40, 560, "blue"),
                coin(80, 520, "blue"),
                coin(120, 480, "blue"),
                coin(160, 440, "blue"),
                coin(200, 400, "green"),
                coin(240, 360, "green"),
                coin(280, 320, "green"),
                coin(320, 280, "green"),
            ]
        ),
        Block(
            obstacles=[
                bat(0, 440 - 200),
                bat(40, 480 - 200),
                bat(80, 520 - 200),
                bat(120, 560 - 200),
                bat(160, 600 - 200),
            ],
            color_changers=[
                color_changer(800, "blue"),
            ],
            offset=SCREEN_WIDTH,
            score_points=[
                coin(40, 560, "green"),
                coin(80, 520, "green"),
                coin(120, 480, "green"),
                coin(160, 440, "green"),
                coin(200 + 200, 400, "red"),
                coin(200 + 240, 360, "red"),
                coin(200 + 280, 320, "red"),
                coin(200 + 320, 280, "red"),
            ]
        ),
        Block(
            obstacles=[
                bird(0, 100),
                bird(40, 140),
                bird(80, 180),
                bird(120, 220),
                bird(160, 260),
            ],
            color_changers=[],
            score_points=[
                coin(200, 400, "red"),
                coin(240, 400, "red"),
                coin(280, 400, "red"),
                coin(320, 400, "red"),
                coin(360, 400, "red"),
            ],
            offset=SCREEN_WIDTH
        )
    ]

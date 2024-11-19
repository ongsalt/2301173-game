from typing import Literal
from pygame import Rect
from kaoyum.block import Block
from kaoyum.obstacle import Obstacle
from kaoyum.scorepoint import Scorepoint
from kaoyum.color_change import ColorChange
from kaoyum.assets_manager import AssetsManager
from kaoyum.utils import tint

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

def color_changer(x: int, y: int, color: str) -> ColorChange:
    return ColorChange(
        x=x,
        width=32,
        height=32,
        color=color,
    )

def initialize_blocks():
    SCREEN_WIDTH = 800
    default_coin = AssetsManager().get("Coins/1.png")
    AssetsManager().set("Coins/red.png", tint(default_coin, (255, 0, 0)))
    AssetsManager().set("Coins/green.png", tint(default_coin, (0, 255, 0)))
    AssetsManager().set("Coins/blue.png", tint(default_coin, (0, 0, 255)))

    block1 = Block(
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
        color_changers=[],
        offset=SCREEN_WIDTH
    )

    return [block1]
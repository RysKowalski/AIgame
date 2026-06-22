from dataclasses import dataclass
from typing import Any

import pygame

from .GameObject import GameObject


@dataclass(frozen=True)
class ScriptSquareData:
    x: float
    y: float
    width: float
    height: float
    rotation: float
    backgroundColor: tuple[int, int, int]
    borderWidth: float
    borderColor: tuple[int, int, int]


class SquareObject(GameObject):
    """
    this.x
    this.y
    this.width
    this.height
    this.rotation
    this.red
    this.green
    this.blue
    this.border_width
    this.border_red
    this.border_green
    this.border_blue
    """

    name = "Square"
    id = 0
    script = """this.x = 0
    this.y = 0
    this.width = 100
    this.height = 100
    this.rotation = 0
    this.red = 255
    this.green = 255
    this.blue = 255
    this.border_width = 0
    this.border_red = 0
    this.border_green = 0
    this.border_blue = 0"""

    def __init__(
        self,
        screen: pygame.Surface,
    ) -> None:
        super().__init__(screen)
        self.get_data = lambda: {}

    def draw(self) -> None:
        data: dict[str, Any] = self.get_data()
        squareData: ScriptSquareData = ScriptSquareData(
            x=data.get("x", 0),
            y=data.get("y", 0),
            width=data.get("width", 100),
            height=data.get("height", 100),
            rotation=data.get("rotation", 0),
            backgroundColor=(
                data.get("red", 255),
                data.get("green", 255),
                data.get("blue", 255),
            ),
            borderWidth=data.get("border_width", 0),
            borderColor=(
                data.get("border_red", 0),
                data.get("border_green", 0),
                data.get("border_blue", 0),
            ),
        )

        surface: pygame.Surface = pygame.Surface(
            (squareData.width, squareData.height), pygame.SRCALPHA
        )

        rect: pygame.Rect = pygame.Rect(0, 0, squareData.width, squareData.height)

        pygame.draw.rect(surface, squareData.backgroundColor, rect)
        if squareData.borderWidth > 0:
            pygame.draw.rect(
                surface, squareData.borderColor, rect, int(squareData.borderWidth)
            )

        rotatedSurface: pygame.Surface = pygame.transform.rotate(
            surface, squareData.rotation
        )
        center: tuple[float, float] = (
            squareData.x + squareData.width / 2,
            squareData.y + squareData.height / 2,
        )

        rotatedRect: pygame.Rect = rotatedSurface.get_rect(center=center)

        self.screen.blit(rotatedSurface, rotatedRect)

    def contains_point(self, pos: tuple[int, int]) -> bool:
        data: dict[str, Any] = self.get_data()
        squareData: ScriptSquareData = ScriptSquareData(
            x=data.get("x", 0),
            y=data.get("y", 0),
            width=data.get("width", 100),
            height=data.get("height", 100),
            rotation=data.get("rotation", 0),
            backgroundColor=(
                data.get("red", 255),
                data.get("green", 255),
                data.get("blue", 255),
            ),
            borderWidth=data.get("border_width", 0),
            borderColor=(
                data.get("border_red", 0),
                data.get("border_green", 0),
                data.get("border_blue", 0),
            ),
        )

        surface: pygame.Surface = pygame.Surface(
            (squareData.width, squareData.height), pygame.SRCALPHA
        )

        rotatedSurface: pygame.Surface = pygame.transform.rotate(
            surface, squareData.rotation
        )

        center: tuple[float, float] = (
            squareData.x + squareData.width / 2,
            squareData.y + squareData.height / 2,
        )

        rotatedRect: pygame.Rect = rotatedSurface.get_rect(center=center)

        return rotatedRect.collidepoint(pos)

from dataclasses import dataclass

import pygame

from .GameObject import VizObject


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


class SquareObject(VizObject):
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
    script = """x = 0
    y = 0
    width = 100
    height = 100
    rotation = 0
    red = 255
    green = 255
    blue = 255
    border_width = 0
    border_red = 0
    border_green = 0
    border_blue = 0"""

    def __init__(
        self,
        screen: pygame.Surface,
    ) -> None:
        super().__init__(screen)
        self.get_data = lambda: {}

    def draw(self) -> None:
        squareData: ScriptSquareData = ScriptSquareData(
            x=self.data.get("x", 0),
            y=self.data.get("y", 0),
            width=self.data.get("width", 100),
            height=self.data.get("height", 100),
            rotation=self.data.get("rotation", 0),
            backgroundColor=(
                self.data.get("red", 255),
                self.data.get("green", 255),
                self.data.get("blue", 255),
            ),
            borderWidth=self.data.get("border_width", 0),
            borderColor=(
                self.data.get("border_red", 0),
                self.data.get("border_green", 0),
                self.data.get("border_blue", 0),
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
        squareData: ScriptSquareData = ScriptSquareData(
            x=self.data.get("x", 0),
            y=self.data.get("y", 0),
            width=self.data.get("width", 100),
            height=self.data.get("height", 100),
            rotation=self.data.get("rotation", 0),
            backgroundColor=(
                self.data.get("red", 255),
                self.data.get("green", 255),
                self.data.get("blue", 255),
            ),
            borderWidth=self.data.get("border_width", 0),
            borderColor=(
                self.data.get("border_red", 0),
                self.data.get("border_green", 0),
                self.data.get("border_blue", 0),
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

from collections.abc import Callable
from dataclasses import dataclass

import pygame
from pygame.event import Event

from .GameObject import InputObject


@dataclass(frozen=True)
class ScriptTickData:
    x: float
    y: float
    width: float
    height: float
    rotation: float
    backgroundColor: tuple[int, int, int]
    borderWidth: float
    borderColor: tuple[int, int, int]


class TickObject(InputObject):
    """
    x
    y
    width
    height
    rotation
    red
    green
    blue
    hover_red
    hover_green
    hover_blue
    border_width
    border_red
    border_green
    border_blue
    """

    name = "Input"
    id = 0
    data = {}

    def __init__(
        self,
        screen: pygame.Surface,
        tick: Callable[[list[float]], None],
        input_count: int,
    ) -> None:
        self.script = """x = 0
y = 0
width = 100
height = 100
rotation = 0
red = 255
green = 255
blue = 255
hover_red = 100
hover_green = 100
hover_blue = 100
border_width = 0
border_red = 0
border_green = 0
border_blue = 0"""

        super().__init__(screen)

        self.trigger_tick = tick
        self.input_count: int = input_count

        for i in range(input_count):
            self.script += f"\ninput{i} = 0"

    def draw(self) -> None:
        squareData: ScriptTickData = ScriptTickData(
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
        squareData: ScriptTickData = ScriptTickData(
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

    def process_event(self, event: Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.contains_point(event.pos):
                inputs: list[float] = []
                for i in range(self.input_count):
                    inputs.append(self.data.get(f"input{i}", 0.0))
                self.trigger_tick(inputs)

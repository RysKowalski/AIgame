from dataclasses import dataclass
from typing import Callable

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
    this.x
    this.y
    this.width
    this.height
    this.rotation
    this.red
    this.green
    this.blue
    this.hover_red
    this.hover_green
    this.hover_blue
    this.border_width
    this.border_red
    this.border_green
    this.border_blue
    """

    name = "Input"
    id = 0
    script = """
this.x = 0
this.y = 0
this.width = 100
this.height = 100
this.rotation = 0
this.red = 255
this.green = 255
this.blue = 255
this.hover_red = 100
this.hover_green = 100
this.hover_blue = 100
this.border_width = 0
this.border_red = 0
this.border_green = 0
this.border_blue = 0"""

    def __init__(self, screen: pygame.Surface, tick: Callable[[], None]) -> None:
        super().__init__(screen)
        self.get_data = lambda: {}
        self.trigger_tick = tick

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.contains_point(event.pos):
                    self.trigger_tick()

from collections.abc import Callable

import pygame
from pygame.event import Event

from .GameObject import InputObject


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
        width = self.data.get("width", 100)
        height = self.data.get("height", 100)
        borderWidth = self.data.get("border_width", 0)

        surface: pygame.Surface = pygame.Surface((width, height), pygame.SRCALPHA)

        rect: pygame.Rect = pygame.Rect(0, 0, width, height)

        pygame.draw.rect(
            surface,
            (
                int(self.data.get("red", 255)),
                int(self.data.get("green", 255)),
                int(self.data.get("blue", 255)),
            ),
            rect,
        )
        if borderWidth > 0:
            pygame.draw.rect(
                surface,
                (
                    int(self.data.get("border_red", 0)),
                    int(self.data.get("border_green", 0)),
                    int(self.data.get("border_blue", 0)),
                ),
                rect,
                int(borderWidth),
            )

        rotatedSurface: pygame.Surface = pygame.transform.rotate(
            surface, self.data.get("rotation", 0)
        )
        center: tuple[float, float] = (
            self.data.get("x", 0) + width / 2,
            self.data.get("y", 0) + height / 2,
        )

        rotatedRect: pygame.Rect = rotatedSurface.get_rect(center=center)

        self.screen.blit(rotatedSurface, rotatedRect)

    def contains_point(self, pos: tuple[int, int]) -> bool:
        width = self.data.get("width", 100)
        height = self.data.get("height", 100)

        surface: pygame.Surface = pygame.Surface((width, height), pygame.SRCALPHA)

        rotatedSurface: pygame.Surface = pygame.transform.rotate(
            surface, self.data.get("rotation", 0)
        )

        center: tuple[float, float] = (
            self.data.get("x", 0) + width / 2,
            self.data.get("y", 0) + height / 2,
        )

        rotatedRect: pygame.Rect = rotatedSurface.get_rect(center=center)

        return rotatedRect.collidepoint(pos)

    def process_event(self, events: list[Event]) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.contains_point(event.pos):
                    inputs: list[float] = []
                    for i in range(self.input_count):
                        inputs.append(self.data.get(f"input{i}", 0.0))
                    self.trigger_tick(inputs)

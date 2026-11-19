from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

import pygame
import pygame.freetype

if TYPE_CHECKING:
    from pygame.event import Event

from .GameObject import InputObject


class TimerTickObject(InputObject):
    """
    x
    y
    round_digits
    red
    green
    blue
    text_red
    text_green
    text_blue
    ticks
    """

    name = "timer tick"
    id = 0

    def __init__(
        self,
        screen: pygame.Surface,
        font: pygame.freetype.Font,
        tick: Callable[[list[float]], None],
        input_count: int,
    ) -> None:
        self.script = """x = 0
y = 0
round_digits = 2
red = 155
green = 155
blue = 155
text_red = 255
text_green = 255
text_blue = 255
ticks = 60
active = 0"""

        super().__init__(screen)
        self.font: pygame.freetype.Font = font
        self.rect: pygame.Rect = pygame.Rect(1, 1, 1, 1)
        self.data = {}

        self.trigger_tick = tick
        self.input_count: int = input_count

        self.remaining_ticks: int = 60

        for i in range(input_count):
            self.script += f"\ninput{i} = 0"

    def draw(self) -> None:
        active: bool = bool(self.data.get("active", 0))
        self.remaining_ticks -= active

        time_remaining: str = str(self.remaining_ticks) + "t"

        if self.remaining_ticks < 1:
            self.remaining_ticks = int(self.data.get("ticks", 60))
            inputs: list[float] = []
            for i in range(self.input_count):
                inputs.append(self.data.get(f"input{i}", 0.0))
            self.trigger_tick(inputs)

        self.font.render_to(
            self.screen,
            (self.data.get("x", 0), self.data.get("y", 0)),
            time_remaining,
            (
                int(self.data.get("text_red", 255)),
                int(self.data.get("text_green", 255)),
                int(self.data.get("text_blue", 255)),
            ),
            (
                int(self.data.get("red", 155)),
                int(self.data.get("green", 155)),
                int(self.data.get("blue", 155)),
            ),
        )

        fontRect: pygame.Rect = self.font.get_rect(time_remaining)
        self.rect.x = int(self.data.get("x", 0))
        self.rect.y = int(self.data.get("y", 0))
        self.rect.width = fontRect.width
        self.rect.height = fontRect.height

    def contains_point(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)

    def process_event(self, events: list[Event]) -> None:
        pass

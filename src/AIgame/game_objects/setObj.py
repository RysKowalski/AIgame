from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
import pygame.freetype

if TYPE_CHECKING:
    from AIgame.script_applyer.context import Context

from .GameObject import InputObject


class SetObject(InputObject):
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
    name
    value
    """

    name = "Set"
    script = """x = 0
y = 0
round_digits = 2
red = 155
green = 155
blue = 155
text_red = 255
text_green = 255
text_blue = 255
name = 0
value = 0"""

    def __init__(
        self, screen: pygame.Surface, font: pygame.freetype.Font, context: Context
    ) -> None:
        super().__init__(screen)
        self.font: pygame.freetype.Font = font
        self.rect: pygame.Rect = pygame.Rect(1, 1, 1, 1)
        self.context: Context = context

    def draw(self) -> None:
        rawValue: float = self.data.get("value", 0)
        roundDigits: int = int(self.data.get("round_digits", 2))

        value: str
        if roundDigits > 0:
            value = str(round(rawValue, roundDigits))
        else:
            value = str(round(rawValue))

        backgroundColor: tuple[int, int, int] = (
            int(self.data.get("red", 155)),
            int(self.data.get("green", 155)),
            int(self.data.get("blue", 155)),
        )

        textColor: tuple[int, int, int] = (
            int(self.data.get("text_red", 255)),
            int(self.data.get("text_green", 255)),
            int(self.data.get("text_blue", 255)),
        )

        name: str = str(int(self.data.get("name", 0)))
        self.context.user_variables[name] = rawValue

        self.font.render_to(
            self.screen,
            (self.data.get("x", 0), self.data.get("y", 0)),
            f"{name} = {value}",
            textColor,
            backgroundColor,
        )

        fontRect: pygame.Rect = self.font.get_rect(f"{name} = {value}")
        self.rect.x = int(self.data.get("x", 0))
        self.rect.y = int(self.data.get("y", 0))
        self.rect.width = fontRect.width
        self.rect.height = fontRect.height

    def contains_point(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)

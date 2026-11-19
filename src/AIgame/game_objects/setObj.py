from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


import pygame


if TYPE_CHECKING:
    from AIgame.script_applyer.context import Context
    import pygame.freetype

from .GameObject import InputObject


@dataclass(frozen=True)
class ScriptSetData:
    x: float
    y: float
    backgroundColor: tuple[int, int, int]
    textColor: tuple[int, int, int]
    value: str


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
    id = 0
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
        self, screen: pygame.Surface, font: "pygame.freetype.Font", context: Context
    ) -> None:
        super().__init__(screen)
        self.font: "pygame.freetype.Font" = font
        self.rect: pygame.Rect = pygame.Rect(1, 1, 1, 1)
        self.data = {}
        self.context: Context = context

    def draw(self) -> None:
        rawValue: float = self.data.get("value", 0)
        roundDigits: int = int(self.data.get("round_digits", 2))

        value: str
        if roundDigits > 0:
            value = str(round(rawValue, roundDigits))
        else:
            value = str(round(rawValue))

        textDisplayData: ScriptSetData = ScriptSetData(
            x=self.data.get("x", 0),
            y=self.data.get("y", 0),
            backgroundColor=(
                self.data.get("red", 155),
                self.data.get("green", 155),
                self.data.get("blue", 155),
            ),
            textColor=(
                self.data.get("text_red", 255),
                self.data.get("text_green", 255),
                self.data.get("text_blue", 255),
            ),
            value=value,
        )

        name: str = str(int(self.data.get("name", 0)))
        self.context.user_variables[name] = rawValue

        self.font.render_to(
            self.screen,
            (textDisplayData.x, textDisplayData.y),
            f"{name} = {textDisplayData.value}",
            textDisplayData.textColor,
            textDisplayData.backgroundColor,
        )

        fontRect: pygame.Rect = self.font.get_rect(f"{name} = {textDisplayData.value}")
        self.rect.x = int(textDisplayData.x)
        self.rect.y = int(textDisplayData.y)
        self.rect.width = fontRect.width
        self.rect.height = fontRect.height

    def contains_point(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)

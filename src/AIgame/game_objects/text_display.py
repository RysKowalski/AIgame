from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import pygame

if TYPE_CHECKING:
    import pygame.freetype

from .GameObject import GameObject


@dataclass(frozen=True)
class ScriptTextDisplayData:
    x: float
    y: float
    backgroundColor: tuple[int, int, int]
    textColor: tuple[int, int, int]
    value: str


class TextDisplayObject(GameObject):
    """
    this.x
    this.y
    this.value
    this.round_digits
    this.red
    this.green
    this.blue
    this.text_red
    this.text_green
    this.text_blue
    """

    name = "Text"
    id = 0
    script = """this.x = 0
this.y = 0
this.value = 0
this.round_digits = 2
this.red = 155
this.green = 155
this.blue = 155
this.text_red = 255
this.text_green = 255
this.text_blue = 255"""

    def __init__(
        self,
        screen: pygame.Surface,
        font: "pygame.freetype.Font",
    ) -> None:
        super().__init__(screen)
        self.font: "pygame.freetype.Font" = font
        self.rect: pygame.Rect = pygame.Rect(1, 1, 1, 1)
        self.get_data = lambda: {}

    def draw(self) -> None:
        rawValue: float = self.data.get("value", 0)
        roundDigits: int = int(self.data.get("round_digits", 2))

        value: str
        if roundDigits > 0:
            value = str(round(rawValue, roundDigits))
        else:
            value = str(round(rawValue))

        textDisplayData: ScriptTextDisplayData = ScriptTextDisplayData(
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

        self.font.render_to(
            self.screen,
            (textDisplayData.x, textDisplayData.y),
            textDisplayData.value,
            textDisplayData.textColor,
            textDisplayData.backgroundColor,
        )

        fontRect: pygame.Rect = self.font.get_rect(textDisplayData.value)
        self.rect.x = int(textDisplayData.x)
        self.rect.y = int(textDisplayData.y)
        self.rect.width = fontRect.width
        self.rect.height = fontRect.height

    def contains_point(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)

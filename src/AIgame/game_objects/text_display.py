import pygame
import pygame.freetype

from .GameObject import VizObject


class TextDisplayObject(VizObject):
    """
    x
    y
    value
    round_digits
    red
    green
    blue
    text_red
    text_green
    text_blue
    """

    name = "Text"
    id = 0
    script = """x = 0
y = 0
value = 0
round_digits = 2
red = 10
green = 10
blue = 10
text_red = 255
text_green = 255
text_blue = 255"""

    def __init__(
        self,
        screen: pygame.Surface,
        font: "pygame.freetype.Font",
    ) -> None:
        super().__init__(screen)
        self.font: pygame.freetype.Font = font
        self.rect: pygame.Rect = pygame.Rect(1, 1, 1, 1)
        self.data = {}

    def draw(self) -> None:
        rawValue: float = self.data.get("value", 0)
        roundDigits: int = int(self.data.get("round_digits", 2))

        value: str
        if roundDigits > 0:
            value = str(round(rawValue, roundDigits))
        else:
            value = str(round(rawValue))

        x = self.data.get("x", 0)
        y = self.data.get("y", 0)

        self.font.render_to(
            self.screen,
            (x, y),
            value,
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

        fontRect: pygame.Rect = self.font.get_rect(value)
        self.rect.x = int(x)
        self.rect.y = int(y)
        self.rect.width = fontRect.width
        self.rect.height = fontRect.height

    def contains_point(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)

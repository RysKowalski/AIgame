import pygame
import pygame.freetype

from .GameObject import VizObject


class HelpObject(VizObject):
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
    page
    """

    name = "Help"
    script = """x = 0
y = 0
round_digits = 2
red = 10
green = 10
blue = 10
text_red = 255
text_green = 255
text_blue = 255
page = 0"""

    def __init__(
        self,
        screen: pygame.Surface,
        font: "pygame.freetype.Font",
    ) -> None:
        super().__init__(screen)
        self.font: pygame.freetype.Font = font
        self.rect: pygame.Rect = pygame.Rect(1, 1, 1, 1)

    def draw(self) -> None:
        x = self.data.get("x", 0)
        y = self.data.get("y", 0)
        value = "help " + str(int(self.data.get("page", 0)))

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

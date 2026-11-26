import pygame
import pygame.freetype

from .GameObject import VizObject


class HelpObject(VizObject):
    """
    x
    y
    width
    padding
    gap
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
width = 300
padding = 10
gap = 0
red = 10
green = 10
blue = 10
text_red = 255
text_green = 255
text_blue = 255
page = 0"""

    pages: list[str] = [
        """
        help page
        0
        """,
        """
        help page
        1
        looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong
        1
        2
        3
        4
        5
        6
        7
        8
        9
        10
        """,
    ]

    def __init__(
        self,
        screen: pygame.Surface,
        font: "pygame.freetype.Font",
    ) -> None:
        super().__init__(screen)
        self.font: pygame.freetype.Font = font
        self.rect: pygame.Rect = pygame.Rect(1, 1, 1, 1)

    def draw(self) -> None:
        lines: list[str] = self.pages[int(self.data.get("page", 0))].splitlines()
        line_height: int = self.font.get_rect("").height

        x: int = int(self.data.get("x", 0))
        y: int = int(self.data.get("y", 0))
        padding: int = int(self.data.get("padding", 30))
        gap: int = int(self.data.get("gap", 10))
        width: int = int(self.data.get("width", 300))

        self.rect = pygame.Rect(
            x,
            y,
            width + padding * 2,
            int(line_height * len(lines) + gap * (len(lines) - 1) + padding * 2),
        )

        pygame.draw.rect(
            self.screen,
            (
                int(self.data.get("red", 255)),
                int(self.data.get("green", 255)),
                int(self.data.get("blue", 255)),
            ),
            self.rect,
        )

        color = (
            int(self.data.get("text_red", 255)),
            int(self.data.get("text_green", 255)),
            int(self.data.get("text_blue", 255)),
        )

        x += padding
        y += padding

        for line in lines:
            print(x)
            self.font.render_to(self.screen, (x, y), line, color)
            y += line_height + gap

    def contains_point(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)

import pygame
import pygame.freetype
from pygame.rect import Rect

from AIgame.script_applyer.context import Context

from .GameObject import VizObject


class VariablesObject(VizObject):
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
    """

    name = "Variables"
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
text_blue = 255"""

    def __init__(
        self, screen: pygame.Surface, font: "pygame.freetype.Font", context: Context
    ) -> None:
        super().__init__(screen)
        self.font: pygame.freetype.Font = font
        self.context: Context = context

        self.backgroundRect: Rect

    def draw(self) -> None:
        variable_count: int = (
            len(self.context.global_variables)
            + len(self.context.level_variables)
            + len(self.context.user_variables)
        )

        line_height: int = self.font.get_rect("").height

        x: int = int(self.data.get("x", 0))
        y: int = int(self.data.get("y", 0))
        padding: int = int(self.data.get("padding", 30))
        gap: int = int(self.data.get("gap", 10))
        width: int = int(self.data.get("width", 300))

        self.backgroundRect = Rect(
            x,
            y,
            width + padding * 2,
            int(
                line_height * variable_count + gap * (variable_count - 1) + padding * 2
            ),
        )

        pygame.draw.rect(
            self.screen,
            (
                int(self.data.get("red", 255)),
                int(self.data.get("green", 255)),
                int(self.data.get("blue", 255)),
            ),
            self.backgroundRect,
        )

        lines: list[str] = []
        for name, value in self.context.global_variables.items():
            lines.append(f"#{name} = {value}")
        for i, value in enumerate(self.context.level_variables):
            lines.append(f"${i} = {value}")
        for name, value in self.context.user_variables.items():
            lines.append(f"@{name} = {value}")

        color = (
            int(self.data.get("text_red", 255)),
            int(self.data.get("text_green", 255)),
            int(self.data.get("text_blue", 255)),
        )

        x += padding
        y += padding

        for line in lines:
            self.font.render_to(self.screen, (x, y), line, color)
            y += line_height + gap

    def contains_point(self, pos: tuple[int, int]) -> bool:
        return self.backgroundRect.collidepoint(pos)

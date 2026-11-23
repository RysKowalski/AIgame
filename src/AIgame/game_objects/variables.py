import pygame
import pygame.freetype
from pygame.rect import Rect

from AIgame.script_applyer.context import Context

from .GameObject import VizObject


class VariablesObject(VizObject):
    """
    x
    y
    red
    green
    blue
    text_red
    text_green
    text_blue
    """

    name = "Variables"
    id = 0
    script = """x = 0
y = 0
red = 155
green = 155
blue = 155
text_red = 255
text_green = 255
text_blue = 255"""

    def __init__(
        self, screen: pygame.Surface, font: "pygame.freetype.Font", context: Context
    ) -> None:
        super().__init__(screen)
        self.font: pygame.freetype.Font = font
        self.context: Context = context
        self.data = {}

        self.last_variables: set[str] = set()

        self.backgroundRect: Rect

    def generate_menu(self) -> None:
        if self.variables_changed():
            print("changed")

    def variables_changed(self) -> bool:
        variables: set[str] = (
            set(self.context.global_variables)
            | set(self.context.user_variables)
            | {"$" + str(len(self.context.level_variables))}
        )
        if self.last_variables == variables:
            return False

        self.last_variables = variables
        return True

    def draw(self) -> None:
        self.generate_menu()

    def contains_point(self, pos: tuple[int, int]) -> bool:
        return pos == (0, 0)

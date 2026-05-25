from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    import pygame.freetype
    from AIgame.script_engine import ScriptEngine

from AIgame.script_engine import ScriptTextDisplayData
from AIgame.game_objects import GameObject


class TextDisplayObject(GameObject):
    """
    this.x
    this.y
    this.value
    this.round
    this.red
    this.green
    this.blue
    this.text_red
    this.text_green
    this.text_blue
    """

    name = "Text"
    id = 0

    def __init__(
        self,
        script: str,
        screen: pygame.Surface,
        scriptEngine: "ScriptEngine",
        font: "pygame.freetype.Font",
    ) -> None:
        if script == "default":
            self.script: str = self.get_default_script()
        else:
            self.script: str = script
        self.screen = screen
        self.scriptEngine: "ScriptEngine" = scriptEngine
        self.font: "pygame.freetype.Font" = font
        self.rect: pygame.Rect = pygame.Rect(1, 1, 1, 1)
        self.get_data = lambda: self.scriptEngine.calculate_text_display(self.script)

    def draw(self) -> None:
        textDisplayData: ScriptTextDisplayData = self.get_data()
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

    def get_default_script(self) -> str:
        return """this.x = 0
this.y = 0
this.value = 0
this.round = 2
this.red = 155
this.green = 155
this.blue = 155
this.text_red = 255
this.text_green = 255
this.text_blue = 255"""

    def contains_point(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)

from typing import TYPE_CHECKING

import pygame

from script_engine import ScriptEngine, ScriptInputObjectData
from game_objects import GameObject
from widgets import TextDisplay, TextDisplaySettings


if TYPE_CHECKING:
    import pygame.freetype


class InputObject(GameObject):
    """
    this.input
    this.value
    this.x
    this.y
    this.round
    this.padding
    this.red
    this.green
    this.blue
    this.text_red
    this.text_green
    this.text_blue
    this.text_size
    this.border_width
    this.border_red
    this.border_green
    this.border_blue
    """

    name = "Input"

    def __init__(
        self,
        script: str,
        screen: pygame.Surface,
        scriptEngine: ScriptEngine,
        font: pygame.freetype.Font,
    ) -> None:
        if script == "default":
            self.script: str = self.get_default_script()
        else:
            self.script: str = script
        self.screen = screen
        self.scriptEngine: ScriptEngine = scriptEngine
        self.font: pygame.freetype.Font = font

    def _get_data(self) -> ScriptInputObjectData:
        return self.scriptEngine.calculate_input_object(self.script)

    def draw(self) -> None:
        data: ScriptInputObjectData = self._get_data()

        # fontrect: pygame.Rect = self.font.render(self.screen, (data.x, data.y), data.value, data.textColor)

    def get_default_script(self) -> str:
        return """this.input = -1
this.value = 0
this.x = 0
this.y = 0
this.round = 2
this.padding = 5
this.red = 0
this.green = 0
this.blue = 0
this.text_red = 255
this.text_green = 255
this.text_blue = 255
this.text_size = 20
this.border_width = 0
this.border_red = 255
this.border_green = 255
this.border_blue = 255"""

    def contains_point(self, pos: tuple[int, int]) -> bool:
        return True  # TODO:

from dataclasses import dataclass
from typing import Callable

import pygame
import pygame.freetype

from game_objects import GameObject


@dataclass
class EditSettings:
    backgroundColor: pygame.Color
    borderColor: pygame.Color
    editingBorderColor: pygame.Color
    borderWidth: int
    menuHorizontalPadding: int
    topPadding: int
    bottomPadding: int


class TextBox:
    def __init__(
        self,
        screen: pygame.Surface,
        font: pygame.freetype.Font,
        text: str,
        applyFunc: Callable[[str], None],
        textBoxs: list["TextBox"],
    ):
        self.screen: pygame.Surface = screen
        self.font: pygame.freetype.Font = font
        self.text: str = text
        self.apply: Callable[[str], None] = applyFunc
        self.textBoxes: list["TextBox"] = textBoxs
        self.focused: bool = False

    def focus(self) -> None:
        for textBox in self.textBoxes:
            textBox.apply(textBox.text)
            textBox.focused = False
        self.focused = True


class EditElementMenu:
    def __init__(
        self,
        screen: pygame.Surface,
        font: pygame.freetype.Font,
        settings: EditSettings,
        gameObject: GameObject,
    ) -> None:
        self.screen: pygame.Surface = screen
        self.font: pygame.freetype.Font = font
        self.settings: EditSettings = settings
        self.object: GameObject = gameObject

        self.visible: bool = False
        self.position: tuple[int, int] = (0, 0)

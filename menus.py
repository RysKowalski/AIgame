import pygame
import pygame.freetype
from game_objects import GameObject
from script_engine import ScriptEngine
from dataclasses import dataclass


@dataclass
class AddSettings:
    backgroundColor: pygame.Color
    entryColor: pygame.Color
    hoverEntryColor: pygame.Color
    entryPadding: int
    textPadding: int
    entrySpacing: int


class AddElementMenu:
    def __init__(
        self,
        screen: pygame.Surface,
        font: pygame.freetype.Font,
        scriptEngine: ScriptEngine,
        gameObjectList: list[GameObject],
        elements: dict[str, type[GameObject]],
        settings: AddSettings,
    ) -> None:
        self.screen: pygame.Surface = screen
        self.font: pygame.freetype.Font = font
        self.scriptEngine: ScriptEngine = scriptEngine
        self.gameObjectList: list[GameObject] = gameObjectList
        self.elements: dict[str, type[GameObject]] = elements
        self.visible: bool = False
        self.position: tuple[int, int] = (0, 0)
        self.texts: list[pygame.Rect]

    def show(self, position: tuple[int, int]) -> None:
        self.visible = True
        self.position = position

    def hide(self) -> None:
        self.visible = False

    def process_event(self, event: pygame.event.Event) -> None:
        if not self.visible:
            return

    def draw(self) -> None:
        if not self.visible:
            return
        pygame.draw.rect(self.screen, (30, 30, 30), self._calculate_size())

    def _calculate_size(self) -> pygame.Rect:
        fontRect: pygame.Rect = self.font.get_rect(self._get_longest_menu_entry())

        height: float = fontRect.height * len(self.elements) * 1.4
        width: int = fontRect.width
        return pygame.Rect(self.position[0], self.position[1], width, height)

    def _get_longest_menu_entry(self) -> str:
        return max(self.elements.keys(), key=len)

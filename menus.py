import pygame
import pygame.freetype
from game_objects import GameObject
from script_engine import ScriptEngine


class AddElementMenu:
    def __init__(
        self,
        screen: pygame.Surface,
        font: pygame.freetype.Font,
        scriptEngine: ScriptEngine,
        gameObjectList: list[GameObject],
        elements: dict[str, type[GameObject]],
    ) -> None:
        self.screen: pygame.Surface = screen
        self.font: pygame.freetype.Font = font
        self.scriptEngine: ScriptEngine = scriptEngine
        self.gameObjectList: list[GameObject] = gameObjectList
        self.elements: dict[str, type[GameObject]] = elements
        self.visible: bool = False

    def show(self) -> None:
        self.visible = True

    def hide(self) -> None:
        self.visible = False

    def process_event(self, event: pygame.event.Event) -> None:
        if not self.visible:
            return

    def draw(self) -> None:
        if not self.visible:
            return

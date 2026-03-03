import pygame
from game_objects import GameObject


class AddElementMenu:
    def __init__(
        self,
        screen: pygame.Surface,
        gameObjectList: list[GameObject],
        font: pygame.font.Font,
        elements: dict[str, GameObject],
    ) -> None:
        self.screen: pygame.Surface = screen
        self.gameObjectList: list[GameObject] = gameObjectList
        self.font: pygame.font.Font = font
        self.elements: dict[str, GameObject] = elements
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

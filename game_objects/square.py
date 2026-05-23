import pygame

from script_engine import ScriptSquareData, ScriptEngine
from .game_objects import GameObject


class SquareObject(GameObject):
    """
    this.x
    this.y
    this.width
    this.height
    this.rotation
    this.red
    this.green
    this.blue
    this.border_width
    this.border_red
    this.border_green
    this.border_blue
    """

    name = "Square"
    id = 0

    def __init__(
        self,
        script: str,
        screen: pygame.Surface,
        scriptEngine: ScriptEngine,
    ) -> None:
        super().__init__(script, screen, scriptEngine)
        self.get_data = lambda: self.scriptEngine.calculate_square(self.script)

    def draw(self) -> None:
        squareData: ScriptSquareData = self.get_data()

        surface: pygame.Surface = pygame.Surface(
            (squareData.width, squareData.height), pygame.SRCALPHA
        )

        rect: pygame.Rect = pygame.Rect(0, 0, squareData.width, squareData.height)

        pygame.draw.rect(surface, squareData.backgroundColor, rect)
        pygame.draw.rect(
            surface, squareData.borderColor, rect, int(squareData.borderWidth)
        )

        rotatedSurface: pygame.Surface = pygame.transform.rotate(
            surface, squareData.rotation
        )
        center: tuple[float, float] = (
            squareData.x + squareData.width / 2,
            squareData.y + squareData.height / 2,
        )

        rotatedRect: pygame.Rect = rotatedSurface.get_rect(center=center)

        self.screen.blit(rotatedSurface, rotatedRect)

    def get_default_script(self) -> str:
        return """this.x = 0
    this.y = 0
    this.width = 100
    this.height = 100
    this.rotation = 0
    this.red = 255
    this.green = 255
    this.blue = 255
    this.border_width = 5
    this.border_red = 0
    this.border_green = 0
    this.border_blue = 0"""

    def contains_point(self, pos: tuple[int, int]) -> bool:
        squareData: ScriptSquareData = self.get_data()

        surface: pygame.Surface = pygame.Surface(
            (squareData.width, squareData.height), pygame.SRCALPHA
        )

        rotatedSurface: pygame.Surface = pygame.transform.rotate(
            surface, squareData.rotation
        )

        center: tuple[float, float] = (
            squareData.x + squareData.width / 2,
            squareData.y + squareData.height / 2,
        )

        rotatedRect: pygame.Rect = rotatedSurface.get_rect(center=center)

        return rotatedRect.collidepoint(pos)

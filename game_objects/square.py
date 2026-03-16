import pygame
from script_engine import ScriptSquareData
from game_objects import GameObject


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

    def draw(self) -> None:
        squareData: ScriptSquareData = self._get_data()
        rect: pygame.Rect = pygame.Rect(
            int(squareData.x), int(squareData.y), squareData.width, squareData.height
        )
        pygame.draw.rect(self.screen, squareData.backgroundColor, rect)

    def _get_data(self) -> ScriptSquareData:
        return self.scriptEngine.calculate_square(self.script)

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

from __future__ import annotations
import pygame
from levels import Level1Tutorial
from script_engine import ScriptSquareData, ScriptEngine, ScriptTextDisplayData


class GameObject:
    id: str
    script: str
    screen: pygame.Surface
    scriptEngine: ScriptEngine

    def __init__(
        self, script: str, screen: pygame.Surface, scriptEngine: ScriptEngine
    ) -> None:
        self.script: str = script
        self.screen = screen
        self.scriptEngine: ScriptEngine = scriptEngine

    def draw(self) -> None: ...


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

    def draw(self) -> None:
        squareData: ScriptSquareData = self._get_data()
        rect: pygame.Rect = pygame.Rect(
            int(squareData.x), int(squareData.y), squareData.width, squareData.height
        )
        pygame.draw.rect(self.screen, squareData.backgroundColor, rect)

    def _get_data(self) -> ScriptSquareData:
        return self.scriptEngine.calculate_square(self.script)


class TextDisplayObject(GameObject):
    """
    this.x
    this.y
    this.value
    this.red
    this.green
    this.blue
    this.text_red
    this.text_green
    this.text_blue
    """

    def __init__(
        self,
        script: str,
        screen: pygame.Surface,
        scriptEngine: ScriptEngine,
        font: pygame.font.Font,
    ) -> None:
        self.script: str = script
        self.screen = screen
        self.scriptEngine: ScriptEngine = scriptEngine
        self.font: pygame.font.Font = font

    def draw(self) -> None:
        textDisplayData: ScriptTextDisplayData = self._get_data()
        textSurface: pygame.Surface = self.font.render(
            textDisplayData.value,
            False,
            textDisplayData.textColor,
            textDisplayData.backgroundColor,
        )

        self.screen.blit(textSurface, (textDisplayData.x, textDisplayData.y))

    def _get_data(self) -> ScriptTextDisplayData:
        return self.scriptEngine.calculate_text_display(self.script)


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((800, 600))
    level: Level1Tutorial = Level1Tutorial()
    scriptEngine: ScriptEngine = ScriptEngine(level)
    font: pygame.font.Font = pygame.font.SysFont("Comic Sans MS", 30)

    rectScript = """
        this.x = 50
        this.y = $0
        this.width = 15 + 15
        this.height = 12 + 18
        this.rotation = 3 / 2 - 1.5
        this.red = 100 + 100 + 55
        this.green = 100 + 55 + 100
        this.blue = 100 / 2
        this.border_width = 2 + 2
        this.border_red = 55 + 55
        this.border_green = 66 - 10
        this.border_blue = $0 / $1
    """
    textDisplayScript: str = """
        this.x = 100
        this.y = 200
        this.red = 255
        this.green = 0
        this.blue = 0
        this.text_red = 0
        this.text_green = 0
        this.text_blue = 0
        this.value = $0
    """
    rectElement: SquareObject = SquareObject(rectScript, screen, scriptEngine)
    textDisplayElement: TextDisplayObject = TextDisplayObject(
        textDisplayScript, screen, scriptEngine, font
    )
    level.variables[0] = 123

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        rectElement.draw()
        textDisplayElement.draw()
        level.tick((scriptEngine.calculate_expression("1"),))
        pygame.display.flip()

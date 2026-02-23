import pygame

from levels import Level1Tutorial
from script_engine import ScriptSquareData, ScriptEngine


class GameObject:
    id: str
    script: str
    screen: pygame.Surface
    scriptEngine: ScriptEngine

    def __init__(
        self, script: str, screen: pygame.Surface, scriptEngine: ScriptEngine
    ) -> None: ...

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

    def __init__(
        self,
        script: str,
        screen: pygame.Surface,
        scriptEngine: ScriptEngine,
    ) -> None:
        self.script: str = script
        self.screen = screen
        self.scriptEngine: ScriptEngine = scriptEngine

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
    """

    def __init__(
        self, script: str, screen: pygame.Surface, scriptEngine: ScriptEngine
    ) -> None:
        self.script: str = script
        self.screen = screen
        self.scriptEngine: ScriptEngine = scriptEngine


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    level: Level1Tutorial = Level1Tutorial()
    scriptEngine: ScriptEngine = ScriptEngine(level)
    script = """
        this.x = 50
        this.y = $1
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
    rectElement: SquareObject = SquareObject(script, screen, scriptEngine)

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        rectElement.draw()
        level.tick((-0.2,))
        pygame.display.flip()

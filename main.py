import pygame

pygame.init()
import pygame.freetype
import levels
from levels import GameLevel
from script_engine import ScriptEngine
import game_objects
import menus


def main() -> None:
    GAME_FONT: pygame.freetype.Font = pygame.freetype.Font("font.ttf", 24)
    WINDOW_SIZE: tuple[int, int] = (800, 600)
    FRAMERATE: float = 60

    level: GameLevel = levels.Level1Tutorial()
    scriptEngine: ScriptEngine = ScriptEngine(level)
    font: pygame.font.Font = pygame.freetype

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

    uiObjects: list[game_objects.GameObject] = []
    screen: pygame.Surface = initialize_pygame(WINDOW_SIZE)
    uiObjects.append(game_objects.SquareObject(rectScript, screen, scriptEngine))

    addElementMenu: menus.AddElementMenu = menus.AddElementMenu(
        screen, uiObjects, font, {"square": game_objects.SquareObject}
    )

    ticks: int = 0
    running: bool = True
    while running:
        ticks += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            addElementMenu.process_event(event)

        screen.fill((255, 255, 255))

        if ticks == 120:
            addElementMenu.show()
        for uiObject in uiObjects:
            uiObject.draw()

        addElementMenu.draw()
        level.tick((0.3,))

        pygame.display.flip()


def initialize_pygame(window_size: tuple[int, int]) -> pygame.Surface:
    screen: pygame.Surface = pygame.display.set_mode(window_size)
    return screen


if __name__ == "__main__":
    main()

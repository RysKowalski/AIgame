import pygame

pygame.init()
import pygame.freetype
import levels
from levels import GameLevel
from script_engine import ScriptEngine
import game_objects
import menus


def main() -> None:
    WINDOW_SIZE: tuple[int, int] = (800, 600)
    FRAMERATE: float = 60

    font: pygame.freetype.Font = pygame.freetype.Font("font.ttf", 24)
    menuFont: pygame.freetype.Font = pygame.freetype.Font("font.ttf", 50)
    level: GameLevel = levels.Level1Tutorial()
    scriptEngine: ScriptEngine = ScriptEngine(level)
    uiObjects: list[game_objects.GameObject] = []
    screen: pygame.Surface = initialize_pygame(WINDOW_SIZE)
    clock: pygame.time.Clock = pygame.time.Clock()

    menuSettings: menus.AddSettings = menus.AddSettings(
        backgroundColor=pygame.Color(18, 18, 18),  # #121212
        entryBackgroundColor=pygame.Color(18, 18, 18),  # #121212
        hoverEntryBackgroundColor=pygame.Color(50, 50, 50),
        borderColor=pygame.Color(211, 211, 211),  # #D3D3D3
        entryBorderColor=pygame.Color(211, 211, 211),  # #D3D3D3
        borderWidth=3,
        entryBorderWidth=3,
        entryPadding=30,
        textPadding=8,
        entrySpacing=0,
    )
    addElementMenu: menus.AddElementMenu = menus.AddElementMenu(
        screen,
        menuFont,
        uiObjects,
        {
            "square": lambda: game_objects.SquareObject(
                script="default", screen=screen, scriptEngine=scriptEngine
            ),
            "text": lambda: game_objects.TextDisplayObject(
                script="default", screen=screen, scriptEngine=scriptEngine, font=font
            ),
        },
        menuSettings,
    )

    ticks: int = 0
    running: bool = True
    while running:
        ticks += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    addElementMenu.show(event.pos)
            addElementMenu.process_event(event)

        screen.fill((0, 0, 0))

        for uiObject in uiObjects:
            uiObject.draw()

        addElementMenu.draw()
        level.tick((0.3,))

        clock.tick(FRAMERATE)
        pygame.display.flip()


def initialize_pygame(window_size: tuple[int, int]) -> pygame.Surface:
    screen: pygame.Surface = pygame.display.set_mode(window_size)
    return screen


if __name__ == "__main__":
    main()

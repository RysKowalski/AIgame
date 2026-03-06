from typing import Callable
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
    level: GameLevel = levels.Level1Tutorial()
    scriptEngine: ScriptEngine = ScriptEngine(level)
    uiObjects: list[game_objects.GameObject] = []
    screen: pygame.Surface = initialize_pygame(WINDOW_SIZE)
    clock: pygame.time.Clock = pygame.time.Clock()

    menuSettings: menus.AddSettings = menus.AddSettings(
        pygame.Color(100, 100, 100),
        pygame.Color(150, 150, 150),
        pygame.Color(200, 200, 200),
        10,
        3,
        2,
    )
    addElementMenu: menus.AddElementMenu = menus.AddElementMenu(
        screen,
        font,
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

        screen.fill((255, 255, 255))

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

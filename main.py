import pygame
import pygame.freetype
import levels
from levels import GameLevel
from script_engine import ScriptEngine
import game_objects


def main() -> None:
    GAME_FONT: pygame.freetype.Font = pygame.freetype.Font("font.ttf", 24)
    WINDOW_SIZE: tuple[int, int] = (800, 600)
    FRAMERATE: float = 60

    level: GameLevel = levels.Level1Tutorial()
    scriptEngine: ScriptEngine = ScriptEngine(level)

    uiObjects: list[game_objects.GameObject] = []
    screen: pygame.Surface = initialize_pygame(WINDOW_SIZE)

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for uiObject in uiObjects:
            uiObject.draw()


def initialize_pygame(window_size: tuple[int, int]) -> pygame.Surface:
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode(window_size)
    return screen

import pygame

pygame.init()

import menus
import pygame.freetype
import levels
from levels import GameLevel
from script_engine import ScriptEngine
import game_objects


class Fonts:
    addMenuFont: pygame.freetype.Font = pygame.freetype.Font("font.ttf", 50)
    editMenuFont: pygame.freetype.Font = pygame.freetype.Font("font.ttf", 22)
    uiTextDisplayFont: pygame.freetype.Font = pygame.freetype.Font("font.ttf", 24)


def main() -> None:
    WINDOW_SIZE: tuple[int, int] = (0, 0)
    FRAMERATE: float = 60

    level: GameLevel = levels.Level1Tutorial()
    scriptEngine: ScriptEngine = ScriptEngine(level)
    gameObjects: game_objects.GameObjectStore = game_objects.GameObjectStore()
    screen: pygame.Surface = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
    clock: pygame.time.Clock = pygame.time.Clock()

    menuSettings: menus.AddSettings = menus.AddSettings(
        backgroundColor=pygame.Color(18, 18, 18),  # #121212
        entryBackgroundColor=pygame.Color(18, 18, 18),  # #121212
        hoverEntryBackgroundColor=pygame.Color(50, 50, 50),  # #323232
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
        Fonts.addMenuFont,
        gameObjects,
        {
            "square": lambda: game_objects.SquareObject(
                script="default", screen=screen, scriptEngine=scriptEngine
            ),
            "text": lambda: game_objects.TextDisplayObject(
                script="default",
                screen=screen,
                scriptEngine=scriptEngine,
                font=Fonts.uiTextDisplayFont,
            ),
        },
        menuSettings,
    )

    editSettings: menus.EditSettings = menus.EditSettings(
        backgroundColor=pygame.Color(10, 10, 10),
        borderColor=pygame.Color(255, 255, 255),
        editingBorderColor=pygame.Color(255, 255, 255),
        borderWidth=3,
        menuHorizontalPadding=30,
        nameBottomGap=40,
        topPadding=30,
        bottomPadding=30,
        textPadding=8,
        nameSize=30,
    )
    editElementMenu: menus.EditElementMenu = menus.EditElementMenu(
        screen, Fonts.editMenuFont, editSettings, gameObjects
    )

    ticks: int = 0
    running: bool = True
    while running:
        ticks += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
                    ctrl_pressed: bool = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
                    if ctrl_pressed:
                        obj_id: int | None = gameObjects.get_on_pos(event.pos)
                        if obj_id is not None:
                            editElementMenu.show(obj_id, screen.get_rect().center)
                            continue

                if event.button == 2:
                    addElementMenu.show(event.pos)
            addElementMenu.process_event(event)
            editElementMenu.process_event(event)

        screen.fill((0, 0, 0))

        gameObjects.draw()

        addElementMenu.draw()
        editElementMenu.draw()
        level.tick((0.3,))

        clock.tick(FRAMERATE)
        pygame.display.flip()


if __name__ == "__main__":
    main()

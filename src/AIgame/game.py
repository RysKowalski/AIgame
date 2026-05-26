import pygame

from AIgame.menus import AddSettings, AddElementMenu, EditSettings, EditElementMenu
from AIgame.levels import LevelManager
from AIgame.game_objects_manager import GameObjectManager
from AIgame.resources import Fonts


def main() -> None:
    FRAMERATE: float = 60
    clock: pygame.time.Clock = pygame.time.Clock()
    screen: pygame.Surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    levelManager: LevelManager = LevelManager("tutorial1temp")

    gameObjects: GameObjectManager = GameObjectManager()

    menuSettings: AddSettings = AddSettings(
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

    addElementMenu: AddElementMenu = AddElementMenu(
        screen,
        gameObjects,
        menuSettings,
    )

    editSettings: EditSettings = EditSettings(
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
    editElementMenu: EditElementMenu = EditElementMenu(
        screen, editSettings, gameObjects
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
        levelManager.tick((0.3, 0.3))

        clock.tick(FRAMERATE)
        pygame.display.flip()


if __name__ == "__main__":
    main()

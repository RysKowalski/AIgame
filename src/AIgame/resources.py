import sys
from pathlib import Path

import pygame.freetype


class Fonts:
    @staticmethod
    def _resource_path(relative_path: str) -> str:
        base_path: str = getattr(sys, "_MEIPASS", Path(__file__).parent.as_posix())
        return str(Path(base_path) / relative_path)

    addMenuFont: pygame.freetype.Font = pygame.freetype.Font(
        _resource_path("font.ttf"), 50
    )
    editMenuFont: pygame.freetype.Font = pygame.freetype.Font(
        _resource_path("font.ttf"), 22
    )
    uiTextDisplayFont: pygame.freetype.Font = pygame.freetype.Font(
        _resource_path("font.ttf"), 24
    )

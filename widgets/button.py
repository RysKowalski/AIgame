from dataclasses import dataclass
from typing import Callable

import pygame
import pygame.freetype


@dataclass
class ButtonSettings:
    x: int
    y: int
    width: int
    height: int
    borderWidth: int
    fontSize: float
    backgroundColor: pygame.Color
    borderColor: pygame.Color
    textColor: pygame.Color


class Button:
    def __init__(
        self,
        screen: pygame.Surface,
        font: pygame.freetype.Font,
        text: str,
        settings: ButtonSettings,
        onClick: Callable[[], None],
    ) -> None:
        self.screen: pygame.Surface = screen
        self.font: pygame.freetype.Font = font
        self.text: str = text
        self.settings: ButtonSettings = settings
        self.onClick: Callable[[], None] = onClick
        self.rect: pygame.Rect
        self.surface: pygame.Surface

        self.recalculate_layout()

    def recalculate_layout(self) -> None:
        self.rect = self._create_rect()
        self.surface = self._create_surface()

    def _create_rect(self) -> pygame.Rect:
        return pygame.Rect(
            self.settings.x, self.settings.y, self.settings.width, self.settings.height
        )

    def _create_surface(self) -> pygame.Surface:
        surface: pygame.Surface = pygame.Surface(
            (self.settings.width, self.settings.height)
        )
        pygame.draw.rect(
            surface,
            self.settings.backgroundColor,
            pygame.Rect(0, 0, self.settings.width, self.settings.height),
        )

        pygame.draw.rect(
            surface,
            self.settings.borderColor,
            pygame.Rect(0, 0, self.settings.width, self.settings.height),
            width=self.settings.borderWidth,
        )

        fontRect: pygame.Rect = self.font.get_rect(
            self.text, size=self.settings.fontSize
        )
        fontRect.center = (int(self.settings.width / 2), int(self.settings.height / 2))

        self.font.render_to(
            surface,
            fontRect,
            self.text,
            fgcolor=self.settings.textColor,
            size=self.settings.fontSize,
        )

        return surface

    def draw(self) -> None:
        self.screen.blit(self.surface, self.rect)

    def process_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.onClick()

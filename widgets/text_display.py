from enum import Enum
from dataclasses import dataclass

import pygame
import pygame.freetype


class TextAlign(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


@dataclass
class TextDisplaySettings:
    padding: int
    borderWidth: int
    borderColor: pygame.Color
    backgroundColor: pygame.Color
    textColor: pygame.Color
    fontSize: float
    minWidth: int
    minHeight: int
    textAlign: TextAlign = TextAlign.LEFT


class TextDisplay:
    def __init__(
        self,
        screen: pygame.Surface,
        font: pygame.freetype.Font,
        position: tuple[float, float],
        text: str,
        settings: TextDisplaySettings,
    ) -> None:
        self.screen: pygame.Surface = screen
        self.font: pygame.freetype.Font = font
        self.text: str = text
        self.settings: TextDisplaySettings = settings
        self.rect: pygame.Rect = self._generate_rect(position)

    def _generate_rect(self, position: tuple[float, float]) -> pygame.Rect:
        rect: pygame.Rect = self.font.get_rect(self.text, size=self.settings.fontSize)

        rect.height = max(
            rect.height + self.settings.padding * 2,
            self.settings.minHeight,
        )
        rect.width = max(
            rect.width + self.settings.padding * 2,
            self.settings.minWidth,
        )

        rect.x, rect.y = (int(position[0]), int(position[1]))

        return rect

    def _compute_text_x(self, text_rect: pygame.Rect) -> int:
        inner_left: int = (
            self.rect.x + self.settings.padding + self.settings.borderWidth
        )
        inner_right: int = (
            self.rect.right - self.settings.padding - self.settings.borderWidth
        )
        inner_width: int = inner_right - inner_left

        if self.settings.textAlign == TextAlign.LEFT:
            return inner_left

        if self.settings.textAlign == TextAlign.CENTER:
            return inner_left + (inner_width - text_rect.width) // 2

        return inner_right - text_rect.width

    def draw(self) -> None:  # TODO: vibecoded
        pygame.draw.rect(self.screen, self.settings.backgroundColor, self.rect)

        pygame.draw.rect(
            self.screen,
            self.settings.borderColor,
            self.rect,
            self.settings.borderWidth,
        )

        text_rect: pygame.Rect = self.font.get_rect(
            self.text,
            size=self.settings.fontSize,
        )

        text_rect.x = self._compute_text_x(text_rect)
        text_rect.centery = self.rect.centery

        self.font.render_to(
            self.screen,
            text_rect.topleft,
            self.text,
            self.settings.textColor,
            size=self.settings.fontSize,
        )

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple, Type

import pygame
import pygame.freetype


@dataclass
class AddSettings:
    backgroundColor: pygame.Color
    entryColor: pygame.Color
    hoverEntryColor: pygame.Color
    entryPadding: int
    textPadding: int
    entrySpacing: int


class AddElementMenu:
    """Context menu for spawning GameObject elements."""

    def __init__(
        self,
        screen: pygame.Surface,
        font: pygame.freetype.Font,
        scriptEngine: "ScriptEngine",
        gameObjectList: List["GameObject"],
        elements: Dict[str, Type["GameObject"]],
        settings: AddSettings,
    ) -> None:
        self.screen: pygame.Surface = screen
        self.font: pygame.freetype.Font = font
        self.scriptEngine: "ScriptEngine" = scriptEngine
        self.gameObjectList: List["GameObject"] = gameObjectList
        self.elements: Dict[str, Type["GameObject"]] = elements
        self.settings: AddSettings = settings

        self.visible: bool = False
        self.position: Tuple[int, int] = (0, 0)

        self.entries: List[str] = list(elements.keys())
        self.text_surfaces: List[Tuple[pygame.Surface, pygame.Rect]] = [
            self.font.render(entry, fgcolor=(255, 255, 255)) for entry in self.entries
        ]

        self.entry_rects: List[pygame.Rect] = []
        self.hover_index: int | None = None

        self.menu_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)

        self._recalculate_layout()

    def _recalculate_layout(self) -> None:
        """Compute menu and entry geometry."""

        max_width: int = 0
        text_height: int = 0

        for surface, rect in self.text_surfaces:
            max_width = max(max_width, rect.width)
            text_height = max(text_height, rect.height)

        entry_width: int = (
            max_width + self.settings.textPadding * 2 + self.settings.entryPadding * 2
        )

        entry_height: int = text_height + self.settings.textPadding * 2

        total_height: int = (
            len(self.entries) * entry_height
            + (len(self.entries) - 1) * self.settings.entrySpacing
            + self.settings.entryPadding * 2
        )

        total_width: int = entry_width + self.settings.entryPadding * 2

        self.menu_rect.size = (total_width, total_height)

        self.entry_rects.clear()

        y: int = self.settings.entryPadding

        for _ in self.entries:
            rect = pygame.Rect(
                self.settings.entryPadding,
                y,
                entry_width,
                entry_height,
            )
            self.entry_rects.append(rect)
            y += entry_height + self.settings.entrySpacing

    def show(self, position: Tuple[int, int]) -> None:
        """Display the menu at the given screen position."""

        self.position = position
        self.menu_rect.topleft = position
        self.visible = True
        self.hover_index = None

    def hide(self) -> None:
        """Hide the menu."""

        self.visible = False
        self.hover_index = None

    def process_event(self, event: pygame.event.Event) -> None:
        """Handle pygame input events."""

        if not self.visible:
            return

        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            local_x: int = mx - self.menu_rect.x
            local_y: int = my - self.menu_rect.y

            self.hover_index = None

            for i, rect in enumerate(self.entry_rects):
                if rect.collidepoint(local_x, local_y):
                    self.hover_index = i
                    break

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hover_index is None:
                self.hide()
                return

            name: str = self.entries[self.hover_index]
            cls: Type["GameObject"] = self.elements[name]

            obj: "GameObject" = cls()
            self.gameObjectList.append(obj)

            self.hide()

    def draw(self) -> None:
        """Render the menu."""

        if not self.visible:
            return

        pygame.draw.rect(
            self.screen,
            self.settings.backgroundColor,
            self.menu_rect,
        )

        for i, rect in enumerate(self.entry_rects):
            draw_rect: pygame.Rect = rect.move(self.menu_rect.topleft)

            color: pygame.Color = (
                self.settings.hoverEntryColor
                if i == self.hover_index
                else self.settings.entryColor
            )

            pygame.draw.rect(self.screen, color, draw_rect)

            text_surface, text_rect = self.text_surfaces[i]

            text_pos = (
                draw_rect.x + self.settings.entryPadding + self.settings.textPadding,
                draw_rect.y + self.settings.textPadding,
            )

            self.screen.blit(text_surface, text_pos)

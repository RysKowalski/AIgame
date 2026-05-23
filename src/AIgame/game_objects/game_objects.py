from typing import Any, Callable, Protocol
import pygame
from AIgame.script_engine import ScriptEngine


class GameObject(Protocol):
    id: int
    name: str
    script: str
    screen: pygame.Surface
    scriptEngine: ScriptEngine
    get_data: Callable[[], Any]

    def __init__(
        self, script: str, screen: pygame.Surface, scriptEngine: ScriptEngine
    ) -> None:
        """if script == 'default' default script is set"""
        if script == "default":
            self.script: str = self.get_default_script()
        else:
            self.script: str = script
        self.screen = screen
        self.scriptEngine: ScriptEngine = scriptEngine

    def draw(self) -> None: ...

    def get_default_script(self) -> str: ...

    def contains_point(self, pos: tuple[int, int]) -> bool: ...

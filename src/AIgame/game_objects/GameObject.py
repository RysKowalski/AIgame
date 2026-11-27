from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame import Surface
    from pygame.event import Event


class GameObject(ABC):
    id: int
    name: str
    script: str
    screen: "Surface"
    data: dict[str, float | int]

    def __init__(self, screen: "Surface") -> None:
        self.screen = screen
        self.data = {}
        self.id = 0

    @abstractmethod
    def draw(self) -> None: ...

    @abstractmethod
    def contains_point(self, pos: tuple[int, int]) -> bool: ...


class InputObject(GameObject):
    @abstractmethod
    def process_event(self, events: list["Event"]) -> None: ...


class VizObject(GameObject): ...

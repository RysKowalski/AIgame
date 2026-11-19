from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from pygame.event import Event
    from pygame import Surface


class GameObject(Protocol):
    id: int
    name: str
    script: str
    screen: "Surface"
    data: dict[str, float | int]

    def __init__(self, screen: "Surface") -> None:
        self.screen = screen

    def draw(self) -> None: ...

    def contains_point(self, pos: tuple[int, int]) -> bool: ...


class InputObject(GameObject):
    def process_event(self, events: list["Event"]) -> None: ...


class VizObject(GameObject): ...

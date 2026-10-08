from typing import TYPE_CHECKING, Any, Callable, Protocol, runtime_checkable


if TYPE_CHECKING:
    from pygame.event import Event
    from pygame import Surface


class GameObject(Protocol):
    id: int
    name: str
    script: str
    screen: "Surface"
    get_data: Callable[[], Any]
    data: Any

    def __init__(self, screen: "Surface") -> None:
        self.screen = screen

    def draw(self) -> None: ...

    def run_script(self) -> None:
        self.data = self.get_data()

    def contains_point(self, pos: tuple[int, int]) -> bool: ...


@runtime_checkable
class InputObject(GameObject):
    def process_event(self, event: "Event") -> None: ...


@runtime_checkable
class VizObject(GameObject): ...

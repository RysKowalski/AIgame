from typing import TYPE_CHECKING, Any, Callable, Protocol

if TYPE_CHECKING:
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

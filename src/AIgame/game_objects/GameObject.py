from typing import TYPE_CHECKING, Any, Callable, Protocol, runtime_checkable

if TYPE_CHECKING:
    from pygame import Surface


@runtime_checkable
class GameObject(Protocol):
    id: int
    name: str
    script: str
    screen: "Surface"
    get_data: Callable[[], Any]

    def __init__(self, screen: "Surface") -> None:
        self.screen = screen

    def draw(self) -> None: ...

    def contains_point(self, pos: tuple[int, int]) -> bool: ...

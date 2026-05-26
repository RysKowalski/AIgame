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

    def __init__(self, script: str, screen: "Surface") -> None:
        """if script == 'default' default script is set"""
        if script == "default":
            self.script: str = self.get_default_script()
        else:
            self.script: str = script
        self.screen = screen

    def draw(self) -> None: ...

    def get_default_script(self) -> str: ...

    def contains_point(self, pos: tuple[int, int]) -> bool: ...

from pygame.event import Event

from .mouse import Mouse
from .widget import WidgetHandler

__version__ = "1.3.2"


def update(events: list[Event]):
    Mouse.updateMouseState()
    WidgetHandler.main(events)


def version():
    print(f"PygameWidgets v{__version__}")

from __future__ import annotations

import weakref
from abc import ABC, abstractmethod
from collections import OrderedDict
from collections.abc import Iterable, Iterator, MutableSet
from typing import Any

from pygame import Surface
from pygame.event import Event

from .mouse import Mouse


class OrderedSet[T](MutableSet[T]):
    def __init__(self, values: Iterable[T] = ()) -> None:
        self._od: OrderedDict[T, None] = OrderedDict.fromkeys(values)

    def __len__(self) -> int:
        return len(self._od)

    def __iter__(self) -> Iterator[T]:
        return iter(self._od)

    def __contains__(self, value: object) -> bool:
        return value in self._od

    def add(self, value: T) -> None:
        self._od[value] = None

    def discard(self, value: T) -> None:
        self._od.pop(value, None)

    def move_to_end(self, value: T) -> None:
        self._od.move_to_end(value)

    def move_to_start(self, value: T) -> None:
        self._od.move_to_end(value, last=False)

    def copy(self) -> OrderedSet[T]:
        return OrderedSet(self._od.keys())


class OrderedWeakset[T](weakref.WeakSet[T]):
    _remove: Any

    def __init__(self, values: Iterable[T] = ()) -> None:
        super().__init__()

        self.data: OrderedSet[weakref.ReferenceType[T]] = OrderedSet()

        for elem in values:
            self.add(elem)

    def move_to_end(self, item: T) -> None:
        self.data.move_to_end(weakref.ref(item, self._remove))

    def move_to_start(self, item: T) -> None:
        self.data.move_to_start(weakref.ref(item, self._remove))


class WidgetBase(ABC):
    def __init__(
        self,
        win: Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        isSubWidget: bool = False,
    ) -> None:
        self.win: Surface = win
        self._x: int = x
        self._y: int = y
        self._width: int = width
        self._height: int = height
        self._isSubWidget: bool = isSubWidget

        self._hidden: bool = False
        self._disabled: bool = False

        if not isSubWidget:
            WidgetHandler.addWidget(self)

    @abstractmethod
    def listen(self, events: list[Event]) -> None: ...

    @abstractmethod
    def draw(self) -> None: ...

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}"
            f"(x={self._x}, y={self._y}, "
            f"width={self._width}, height={self._height})"
        )

    def contains(self, x: int, y: int) -> bool:
        ox, oy = self.win.get_abs_offset()

        return (
            self._x < x - ox < self._x + self._width
            and self._y < y - oy < self._y + self._height
        )

    def hide(self) -> None:
        self._hidden = True

        if not self._isSubWidget:
            WidgetHandler.moveToBottom(self)

    def show(self) -> None:
        self._hidden = False

        if not self._isSubWidget:
            WidgetHandler.moveToTop(self)

    def disable(self) -> None:
        self._disabled = True

    def enable(self) -> None:
        self._disabled = False

    def isSubWidget(self) -> bool:
        return self._isSubWidget

    def moveToTop(self) -> None:
        WidgetHandler.moveToTop(self)

    def moveToBottom(self) -> None:
        WidgetHandler.moveToBottom(self)

    def moveX(self, x: int) -> None:
        self._x += x

    def moveY(self, y: int) -> None:
        self._y += y

    def get(self, attr: str) -> int | None:
        if attr == "x":
            return self._x

        if attr == "y":
            return self._y

        if attr == "width":
            return self._width

        if attr == "height":
            return self._height

        return None

    def getX(self) -> int:
        return self._x

    def getY(self) -> int:
        return self._y

    def getWidth(self) -> int:
        return self._width

    def getHeight(self) -> int:
        return self._height

    def isVisible(self) -> bool:
        return not self._hidden

    def isEnabled(self) -> bool:
        return not self._disabled

    def set(self, attr: str, value: int) -> None:
        if attr == "x":
            self._x = value

        elif attr == "y":
            self._y = value

        elif attr == "width":
            self._width = value

        elif attr == "height":
            self._height = value

    def setX(self, x: int) -> None:
        self._x = x

    def setY(self, y: int) -> None:
        self._y = y

    def setWidth(self, width: int) -> None:
        self._width = width

    def setHeight(self, height: int) -> None:
        self._height = height

    def setIsSubWidget(self, isSubWidget: bool) -> None:
        self._isSubWidget = isSubWidget

        if isSubWidget:
            WidgetHandler.removeWidget(self)
        else:
            WidgetHandler.addWidget(self)


class WidgetHandler:
    _widgets: OrderedWeakset[WidgetBase] = OrderedWeakset()

    @staticmethod
    def main(events: list[Event]) -> None:
        blocked = False

        widgets: list[WidgetBase] = list(WidgetHandler._widgets)

        for widget in reversed(widgets):
            if not blocked or not widget.contains(*Mouse.getMousePos()):
                widget.listen(events)

            if widget.contains(*Mouse.getMousePos()):
                blocked = True

        for widget in widgets:
            widget.draw()

    @staticmethod
    def addWidget(widget: WidgetBase) -> None:
        if widget not in WidgetHandler._widgets:
            WidgetHandler._widgets.add(widget)
            WidgetHandler.moveToTop(widget)

    @staticmethod
    def removeWidget(widget: WidgetBase) -> None:
        try:
            WidgetHandler._widgets.remove(widget)
        except ValueError:
            print(
                f"Error: Tried to remove {widget} when {widget} not in WidgetHandler."
            )

    @staticmethod
    def moveToTop(widget: WidgetBase) -> None:
        try:
            WidgetHandler._widgets.move_to_end(widget)
        except KeyError:
            print(
                f"Error: Tried to move {widget} "
                f"to top when {widget} not in WidgetHandler."
            )

    @staticmethod
    def moveToBottom(widget: WidgetBase) -> None:
        try:
            WidgetHandler._widgets.move_to_start(widget)
        except KeyError:
            print(
                f"Error: Tried to move {widget} "
                f"to bottom when {widget} not in WidgetHandler."
            )

    @staticmethod
    def getWidgets() -> OrderedWeakset[WidgetBase]:
        return WidgetHandler._widgets

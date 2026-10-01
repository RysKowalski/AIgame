from AIgame.game_objects import GameObject
from AIgame.game_objects_manager import GameObjectManager, ObjectDoesNotExistError
from tests.utils import (
    ExampleObject,
    get_example_object,
    example_surface,
)


def test_add_and_get() -> None:
    objectStore: GameObjectManager = GameObjectManager()
    exampleObject: GameObject = get_example_object()

    objectId: int = objectStore.add(exampleObject)
    outputObject: GameObject = objectStore.get(objectId)

    assert exampleObject is outputObject


def test_add_sets_game_object_id() -> None:
    objectStore: GameObjectManager = GameObjectManager()
    obj: ExampleObject = get_example_object()

    id: int = objectStore.add(obj)

    assert id == obj.id


def test_add_and_get_many() -> None:
    objectStore: GameObjectManager = GameObjectManager()
    addedObjects: dict[int, GameObject] = {}

    for _ in range(100):
        gameObject: GameObject = ExampleObject(example_surface())
        id: int = objectStore.add(gameObject)
        addedObjects[id] = gameObject

    for gameObjectId in addedObjects:
        assert objectStore.get(gameObjectId) is addedObjects[gameObjectId]


def test_get_nonexistent_raises_exception() -> None:
    objectStore: GameObjectManager = GameObjectManager()
    nonexistentId: int = -1
    failed: bool = True

    try:
        objectStore.get(nonexistentId)
    except ObjectDoesNotExistError:
        failed = False

    assert not failed


def test_delete_get_raises_exception() -> None:
    objectStore: GameObjectManager = GameObjectManager()
    exampleObject: GameObject = ExampleObject(example_surface())
    failed: bool = True

    id: int = objectStore.add(exampleObject)
    objectStore.delete(id)

    try:
        objectStore.get(id)
    except ObjectDoesNotExistError:
        failed = False

    assert not failed


def test_delete_nonexistent_raises_exception() -> None:
    objectStore: GameObjectManager = GameObjectManager()
    nonexistentId: int = -1
    failed: bool = True

    try:
        objectStore.delete(nonexistentId)
    except ObjectDoesNotExistError:
        failed = False

    assert not failed


def test_draw_correct_call() -> None:
    objectStore: GameObjectManager = GameObjectManager()
    gameObject: GameObject = get_example_object()
    objectStore.add(gameObject)

    objectStore.draw()

    assert gameObject.draw_call_count == 1


def test_draw_correct_call_many() -> None:
    objectStore: GameObjectManager = GameObjectManager()
    gameObjects: list[ExampleObject] = [get_example_object() for _ in range(100)]
    for gameObject in gameObjects:
        objectStore.add(gameObject)

    objectStore.draw()

    for gameObject in gameObjects:
        assert gameObject.draw_call_count == 1


def test_draw_no_game_objects() -> None:
    objectStore: GameObjectManager = GameObjectManager()

    objectStore.draw()


def test_get_on_pos_found() -> None:
    objectStore: GameObjectManager = GameObjectManager()
    gameObject: ExampleObject = get_example_object()
    gameObject.contains_point_returns = True
    id: int = objectStore.add(gameObject)

    containsID: int | None = objectStore.get_on_pos((0, 0))

    assert id == containsID


def test_get_on_pos_not_found() -> None:
    objectStore: GameObjectManager = GameObjectManager()
    gameObject: ExampleObject = get_example_object()
    gameObject.contains_point_returns = False
    objectStore.add(gameObject)

    id: int | None = objectStore.get_on_pos((0, 0))

    assert id is None


def test_get_on_pos_later_added_detected_first() -> None:
    objectStore: GameObjectManager = GameObjectManager()
    obj1: ExampleObject = get_example_object()
    obj1.returns_true()
    obj2: ExampleObject = get_example_object()
    obj2.returns_true()
    objectStore.add(obj1)
    objectStore.add(obj2)

    detectedID: int | None = objectStore.get_on_pos((0, 0))

    assert detectedID == obj2.id

from AIgame.game_objects import GameObject
from AIgame.game_objects_manager import GameObjectManager, ObjectDoesNotExistError
from AIgame.script_applyer import Context
from tests.utils import (
    ExampleObject,
    example_surface,
    get_example_object,
)


def test_add_and_get() -> None:
    objectStore: GameObjectManager = GameObjectManager(Context())
    obj: GameObject = get_example_object()

    objectStore.add(obj)
    outputObject: GameObject = objectStore.get(obj.id)

    assert obj is outputObject


def test_add_and_get_many() -> None:
    objectStore: GameObjectManager = GameObjectManager(Context())
    addedObjects: dict[int, GameObject] = {}

    for _ in range(100):
        gameObject: GameObject = ExampleObject(example_surface())
        objectStore.add(gameObject)
        addedObjects[gameObject.id] = gameObject

    for gameObjectId in addedObjects:
        assert objectStore.get(gameObjectId) is addedObjects[gameObjectId]


def test_get_nonexistent_raises_exception() -> None:
    objectStore: GameObjectManager = GameObjectManager(Context())
    nonexistentId: int = -1
    failed: bool = True

    try:
        objectStore.get(nonexistentId)
    except ObjectDoesNotExistError:
        failed = False

    assert not failed


def test_delete_get_raises_exception() -> None:
    objectStore: GameObjectManager = GameObjectManager(Context())
    exampleObject: GameObject = ExampleObject(example_surface())
    failed: bool = True

    objectStore.add(exampleObject)
    id = exampleObject.id
    print(exampleObject.id, objectStore._idCounter)
    objectStore.delete(id)

    try:
        objectStore.get(id)
    except ObjectDoesNotExistError:
        failed = False

    assert not failed


def test_delete_nonexistent_raises_exception() -> None:
    objectStore: GameObjectManager = GameObjectManager(Context())
    nonexistentId: int = -1
    failed: bool = True

    try:
        objectStore.delete(nonexistentId)
    except ObjectDoesNotExistError:
        failed = False

    assert not failed


def test_draw_correct_call() -> None:
    objectStore: GameObjectManager = GameObjectManager(Context())
    gameObject: GameObject = get_example_object()
    objectStore.add(gameObject)

    objectStore.draw()

    assert gameObject.draw_call_count == 1


def test_draw_correct_call_many() -> None:
    objectStore: GameObjectManager = GameObjectManager(Context())
    gameObjects: list[ExampleObject] = [get_example_object() for _ in range(100)]
    for gameObject in gameObjects:
        objectStore.add(gameObject)

    objectStore.draw()

    for gameObject in gameObjects:
        assert gameObject.draw_call_count == 1


def test_draw_no_game_objects() -> None:
    objectStore: GameObjectManager = GameObjectManager(Context())

    objectStore.draw()


def test_get_on_pos_found() -> None:
    objectStore: GameObjectManager = GameObjectManager(Context())
    gameObject: ExampleObject = get_example_object()
    gameObject.contains_point_returns = True
    objectStore.add(gameObject)

    containsID: int | None = objectStore.get_on_pos((0, 0))

    assert gameObject.id == containsID


def test_get_on_pos_not_found() -> None:
    objectStore: GameObjectManager = GameObjectManager(Context())
    gameObject: ExampleObject = get_example_object()
    gameObject.contains_point_returns = False
    objectStore.add(gameObject)

    id: int | None = objectStore.get_on_pos((0, 0))

    assert id is None


def test_get_on_pos_later_added_detected_first() -> None:
    objectStore: GameObjectManager = GameObjectManager(Context())
    obj1: ExampleObject = get_example_object()
    obj1.returns_true()
    obj2: ExampleObject = get_example_object()
    obj2.returns_true()
    objectStore.add(obj1)
    objectStore.add(obj2)

    detectedID: int | None = objectStore.get_on_pos((0, 0))

    assert detectedID == obj2.id

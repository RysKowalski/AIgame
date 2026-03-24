from game_objects import GameObjectStore, GameObject
from tests.utils import ExampleObject, test_script_engine, test_surface


def test_add_and_get() -> None:
    exampleObject: GameObject = ExampleObject(
        "default", test_surface(), test_script_engine()
    )
    objectStore: GameObjectStore = GameObjectStore()

    objectId: int = objectStore.add(exampleObject)
    outputObject: GameObject = objectStore.get(objectId)

    assert exampleObject is outputObject


def test_add_and_get_many() -> None:
    objectStore: GameObjectStore = GameObjectStore()
    addedObjects: dict[int, GameObject] = {}

    for _ in range(1000):
        gameObject: GameObject = ExampleObject(
            "default", test_surface(), test_script_engine()
        )
        id: int = objectStore.add(gameObject)
        addedObjects[id] = gameObject

    for gameObjectId in addedObjects:
        assert objectStore.get(gameObjectId) is addedObjects[gameObjectId]


# def test_get_nonexistent() -> None:
#     objectStore: GameObjectStore = GameObjectStore()
#     nonexistentId: int = 0
#
#     try:
#         objectStore.get(nonexistentId)
#         raise
#     except:
#         return


# def test_delete() -> None:
#     objectStore: GameObjectStore = GameObjectStore()
#     exampleObject: GameObject = ExampleObject("default", test_surface(), test_script_engine())
#
#     id: int = objectStore.add(exampleObject)
#     objectStore.delet

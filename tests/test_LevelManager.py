from AIgame.levels import GameLevel, LevelManager, LevelState, LevelData


class ExampleLevel(GameLevel):
    data = LevelData("test_level", 1, 100)

    def __init__(self) -> None:
        self.tickCount = 0
        self.lastInputs: tuple[float, ...] = ()

    def tick(self, state: LevelState, inputs: tuple[float, ...]) -> None:
        self.tickCount += 1
        self.lastInputs = inputs

    def check_and_set_end(self, state: LevelState) -> None:
        state.ended = state.reward > self.data.rewardTreshhold


class ExampleLevelLast(GameLevel):
    data = LevelData("test_level_last", 1, 100)

    def __init__(self) -> None:
        self.tickCount = 0
        self.lastInputs: tuple[float, ...] = ()

    def tick(self, state: LevelState, inputs: tuple[float, ...]) -> None:
        self.tickCount += 1
        self.lastInputs = inputs

    def check_and_set_end(self, state: LevelState) -> None:
        state.ended = state.reward > self.data.rewardTreshhold


testLevels: dict[str, type[GameLevel]] = {
    ExampleLevel.data.name: ExampleLevel,
    ExampleLevelLast.data.name: ExampleLevelLast,
}


def test_load_level() -> None:
    manager: LevelManager = LevelManager(ExampleLevel.data.name, testLevels)
    assert manager.level.data.name == ExampleLevel.data.name


def test_correct_level_state() -> None:
    manager: LevelManager = LevelManager(ExampleLevel.data.name, testLevels)
    assert manager.levelState == LevelState(0, 0, [0], False)


def test_tick_level() -> None:
    manager: LevelManager = LevelManager(ExampleLevel.data.name, testLevels)
    manager.level = ExampleLevel()

    manager.tick((0.0, 1.1))

    assert manager.level.tickCount == 1


def test_next_level() -> None:
    manager: LevelManager = LevelManager(ExampleLevel.data.name, testLevels)
    manager.levelState.ended = True
    initialLevel: GameLevel = manager.level

    manager.tick(())

    assert manager.level is not initialLevel


def test_next_level_wrap_to_start() -> None:
    manager: LevelManager = LevelManager(ExampleLevelLast.data.name, testLevels)
    manager.levelState.ended = True

    manager.tick(())

    assert isinstance(manager.level, ExampleLevel)

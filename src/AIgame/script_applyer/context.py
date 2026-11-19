from collections.abc import Callable


class Context:
    def __init__(self) -> None:
        self.global_variables: dict[str, float | str] = {
            "reward": 10,
            "total_reward": 100,
        }

        self.level_variables: list[float] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        self.functions: dict[str, Callable[[list[float]], float]] = {
            "min": lambda args: min(args),
            "max": lambda args: max(args),
            "avg": lambda args: sum(args) / len(args),
            "round": lambda args: round(args[0], int(args[1])),
        }

        self.user_variables: dict[str, float] = {}

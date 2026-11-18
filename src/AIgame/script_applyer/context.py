from collections.abc import Callable


class Context:
    global_variables: dict[str, float | str] = {  # noqa: RUF012
        "reward": 10,
        "total_reward": 100,
    }

    level_variables: list[float] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # noqa: RUF012

    functions: dict[str, Callable[[list[float]], float]] = {  # noqa: RUF012
        "min": lambda args: min(args),
        "max": lambda args: max(args),
        "avg": lambda args: sum(args) / len(args),
        "round": lambda args: round(args[0], int(args[1])),
    }

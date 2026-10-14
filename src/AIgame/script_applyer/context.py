from typing import Callable


class Context:
    global_variables: dict[str, float | str] = {
        "reward": 10,
        "total_reward": 100,
    }
    level_variables: list[float] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    functions: dict[str, Callable[..., float]] = {
        "min": min,
        "max": max,
        "avg": lambda args: sum(args) / len(args),
        "round": round,
    }

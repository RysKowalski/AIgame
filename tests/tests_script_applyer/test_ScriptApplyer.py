from AIgame.script_applyer.context import Context
from AIgame.script_applyer.script_applyer import ScriptApplyer

from ..utils import ExampleObject


def test_update_script() -> None:
    obj = ExampleObject()
    obj.script = """ a = 1
 b = 1 + 1
 c = 2 * 2
 d = 2 / 2
 e = 2 + 2 * 2
 f = $0 * $1
 g = #reward
 h = add($0, $1)
 i = minus(add($0, $1), minus($1, #reward))"""
    context = Context()
    context.functions = {
        "add": lambda args: args[0] + args[1],
        "minus": lambda args: args[0] - args[1],
    }
    context.global_variables = {"reward": 10}
    context.level_variables = [1, 2]
    sa = ScriptApplyer(context)

    sa.update_script([obj])

    assert obj.data == {
        "a": 1,
        "b": 2,
        "c": 4,
        "d": 1,
        "e": 6,
        "f": 2,
        "g": 10,
        "h": 3,
        "i": 11,
    }

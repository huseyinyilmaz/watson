from core.dsl.commons import decode
from core.dsl.semantic import parse


def getScript(s: str):
    expr = decode(s)
    return parse(expr)

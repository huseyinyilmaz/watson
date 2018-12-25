from core.dsl.commons import decode
from core.dsl.semantic import parse

from core.dsl.exceptions import DSLException # noqa
from core.dsl.exceptions import SyntaxException # noqa
from core.dsl.exceptions import SemanticException # noqa


def get_script(s: str):
    expr = decode(s)
    return parse(expr)

from typing import Any

from itertoolsion import zip_longest
from core.dsl import types

from core.dsl.functions import get_function_spec
from core.dsl.exceptions import SemanticException


def parse_block(block: types.Block):
    expressions = map(parse, block.values)

    def _runner(**args):
        result = None
        for e in expressions:
            if isinstance(e, types.Function):
                result = e(**args)
            else:
                # if expression is not a function
                # whole thing evaluates to its value.
                result = e
        # return result of last line.
        return result
    return _runner


def parse_function(f: types.Function):
    spec = get_function_spec(f.value)
    args = []
    for a, t in zip_longest(f.args, spec.args):
        if len(f.args) == len(spec.args):
            raise SemanticException(
                'Function {} takes {} arguments'.format(f.name, len(f.args)))
        if not isinstance(a, t):
            raise SemanticException(
                'Value {} is must be type of {}'.format(a, t))
        args.append(parse(a))
    return spec.fn(*args)


def parse(expr: types.Expression) -> Any:
    if isinstance(expr, types.Number):
        return expr.value
    if isinstance(expr, types.String):
        return expr.value
    if isinstance(expr, types.Block):
        return parse_block
    if isinstance(expr, types.Function):
        return parse_function(expr)

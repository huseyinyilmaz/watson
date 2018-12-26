from typing import Any

from itertools import zip_longest
from core.dsl import types

from core.dsl.functions import get_function_spec
from core.dsl.exceptions import SemanticException


def parse_block(block: types.Block):
    # Evaluate map result to list so we can do
    # type validation at script creation and not on run time.
    expressions = list(map(parse, block.values))

    def _runner(**kwargs):
        result = None
        for e, t in zip(expressions, block.values):
            if isinstance(t, types.Function):
                result = e(**kwargs)
            else:
                # if expression is not a function
                # whole thing evaluates to its value.
                result = e
        # return result of last line.
        return result
    return _runner


def parse_function(f: types.Function):
    spec = get_function_spec(f.name)
    if not spec:
        raise SemanticException(
            'Function with name "{}" does not exist.'.format(f.name))
    args = []
    for a, t in zip_longest(f.args, spec.argTypes):
        print(f, spec)
        if len(f.args) != len(spec.argTypes):
            raise SemanticException(
                'Function {} takes {} arguments but {} arguments are given'
                .format(f.name, len(spec.argTypes), len(f.args)))
        if not isinstance(a, t):
            raise SemanticException(
                'Value {} must be type of {}'.format(a.value, t.__name__))
        args.append(parse(a))
    return spec.fn(*args)


def parse(expr: types.Expression) -> Any:
    if isinstance(expr, types.Number):
        return expr.value
    if isinstance(expr, types.String):
        return expr.value
    if isinstance(expr, types.Block):
        return parse_block(expr)
    if isinstance(expr, types.Function):
        return parse_function(expr)

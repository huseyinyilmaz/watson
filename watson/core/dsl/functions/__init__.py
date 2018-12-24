from typing import Any
from typing import List
from typing import Tuple

from core.dsl import types

from core.dsl.functions.click import click
from core.dsl.functions.click import wait

clickSpec = types.FunctionSpec(
    name='click',
    args=(types.String, ),
    fn=click
)

waitSpec = types.FunctionSpec(
    name='wait',
    args=(types.Number, ),
    fn=wait
)


def get_function_spec(name: str) -> types.FunctionSpec:
    if name == 'click':
        return clickSpec
    elif name == 'wait':
        return waitSpec

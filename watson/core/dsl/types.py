from typing import Any
from typing import Callable
from typing import List
# from typing import Tuple
from dataclasses import dataclass


@dataclass(frozen=True)
class Expression:
    pass


@dataclass(frozen=True)
class String(Expression):
    value: str


@dataclass(frozen=True)
class Number(Expression):
    value: float


@dataclass(frozen=True)
class Function(Expression):
    name: str
    args: List[Expression]


@dataclass(frozen=True)
class Block(Expression):
    values: List[Expression]


@dataclass
class FunctionSpec:
    name: str
    argTypes: Any
    fn: Callable[..., Callable[..., Any]]

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Protocol

class _Decorator(Protocol):
    def __call__[**P, R](self, func: Callable[P, R]) -> Callable[P, R]: ...

class Type:
    pass

class Argument(Type):
    def __call__(self, *_: Argument) -> Type: ...

class Scalar(Argument):
    def __getitem__(self, val: slice | tuple[slice, ...]) -> Argument: ...

int64: Scalar
float64: Scalar

def jit(
    sig: Type, /, *, parallel: bool = ..., cache: bool = ..., nogil: bool = ...
) -> _Decorator: ...
def prange(start: int, stop: int | None = ...) -> Iterable[int]: ...

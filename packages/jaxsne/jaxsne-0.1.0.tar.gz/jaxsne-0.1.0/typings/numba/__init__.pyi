from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Protocol

from . import types
from .types import Signature, float64, int64

class _Decorator(Protocol):
    def __call__[**P, R](self, func: Callable[P, R]) -> Callable[P, R]: ...

def jit(
    sig: Signature, /, *, parallel: bool = ..., cache: bool = ..., nogil: bool = ...
) -> _Decorator: ...
def prange(start: int, stop: int | None = ...) -> Iterable[int]: ...

__all__ = ("types", "int64", "float64", "jit", "prange")

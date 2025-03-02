from collections.abc import Callable
from typing import TypeVar

from jax import Array

T = TypeVar("T")

def while_loop(cond: Callable[[T], Array], body: Callable[[T], T], init: T) -> T: ...
def cond(cond: Array | bool, left: Callable[[], T], right: Callable[[], T]) -> T: ...

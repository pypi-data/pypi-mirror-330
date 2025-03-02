from collections.abc import Callable, Mapping
from typing import Literal

import numpy as np
from jax import Array
from numpy.typing import NDArray

class OptimizeResult:
    @property
    def x(self) -> NDArray[np.float64]: ...
    @property
    def success(self) -> bool: ...
    @property
    def message(self) -> str: ...

def minimize(
    func: Callable[[Array], Array],
    init: Array,
    args: tuple[object, ...],
    jac: Callable[[Array], Array],
    method: Literal["CG", "trust-constr"],
    options: Mapping[str, object] | None = None,
) -> OptimizeResult: ...

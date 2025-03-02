from collections.abc import Callable
from typing import TypeAlias

import jax
from jax import Array
from jax import numpy as jnp

Measure: TypeAlias = Callable[[Array], Array]


@jax.jit
def gaussian(dists: Array) -> Array:
    """Unnormalized gaussian distribution.

    `exp(-x^2)`
    """
    return jnp.exp(-(dists**2))


@jax.jit
def laplace(dists: Array) -> Array:
    """Unnormalized laplace distribution.

    `exp(-|x|)`
    """
    return jnp.exp(-jnp.abs(dists))


@jax.jit
def cauchy(dists: Array) -> Array:
    """Unnormalized cauchy distribution.

    `1 / (1 + x^2)`
    """
    return 1 / (1 + dists**2)

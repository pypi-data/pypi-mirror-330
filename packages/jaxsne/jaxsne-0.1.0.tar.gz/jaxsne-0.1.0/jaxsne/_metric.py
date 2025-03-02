from collections.abc import Callable
from typing import TypeAlias

import jax
from jax import Array
from jax import numpy as jnp

Metric: TypeAlias = Callable[[Array, Array], Array]


@jax.jit
def euclidean(left: Array, right: Array) -> Array:
    """Compute the euclidian distance."""
    return jnp.linalg.norm(left - right, 2, -1)


@jax.jit
def cosine(left: Array, right: Array) -> Array:
    """Compute the cosine distance.

    Before computing the distance, the points are projected onto the l2-ball.
    It's normalized to be in [0, 1]
    """
    # first project onto the ball
    left_norm = left / jnp.linalg.norm(left, 2, -1)[..., None]
    right_norm = right / jnp.linalg.norm(right, 2, -1)[..., None]
    # then compute
    return 1 / 2 - (left_norm[..., None, :] @ right_norm[..., None])[..., 0, 0] / 2


@jax.jit
def poincare(left: Array, right: Array) -> Array:
    """Compute the hyperbolic distance.

    This metric is a two stage process. First, points are projected onto the
    poincare disk with `u = x / (1 + ||x||)`. Then the standard poincare distance is
    used on those points.

    If data already exists on the poincare-disk, then you need to project it
    onto the plane with `u = x / (1 - ||x||)` before using this metric on it.
    """
    # first project into the ball
    left_poinc = left / (1 + jnp.linalg.norm(left, 2, -1)[..., None])
    right_poinc = right / (1 + jnp.linalg.norm(right, 2, -1)[..., None])
    # compute delta
    diff = left_poinc - right_poinc
    left_sq = (left_poinc[..., None, :] @ left_poinc[..., None])[..., 0, 0]
    right_sq = (right_poinc[..., None, :] @ right_poinc[..., None])[..., 0, 0]
    diff_sq = (diff[..., None, :] @ diff[..., None])[..., 0, 0]
    delta = 2 * diff_sq / ((1 - left_sq) * (1 - right_sq))
    return jnp.arccosh(1 + delta)

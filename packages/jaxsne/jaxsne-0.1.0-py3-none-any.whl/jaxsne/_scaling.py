from functools import partial

import jax
from jax import Array, random
from jax import numpy as jnp
from scipy import optimize as spo

from . import _utils as utils
from .metric import Metric, euclidean


@partial(jax.jit, static_argnames=["metric", "num", "dim"])
def _fun(x: Array, ref: Array, metric: Metric, num: int, dim: int) -> Array:
    points = x.reshape(num, dim)
    xi, yi = jnp.triu_indices(num, 1)
    dists = metric(points[xi], points[yi])
    return jnp.mean((dists - ref) ** 2)


ZERO_KEY = random.key(0)


def scaling(  # noqa: PLR0913
    data: Array,
    n_components: int = 2,
    *,
    in_metric: Metric = euclidean,
    out_metric: Metric = euclidean,
    max_iter: int = 1024,
    key: Array = ZERO_KEY,
    gtol: float = 1e-6,
    xtol: float = 1e-6,
) -> Array:
    """Apply multidimensional scaling.

    Multidimensional scaling works by finding points in the reduced dimensional
    space while trying to keep the pairwise distances as close as possible.

    Parameters
    ----------
    data : (n, d)
        The input data, as n rows of d-dimensional points.
    n_components : The dimension of the space to project into.
    in_metric : The metric function for the original data space.
    out_metric : The metric function for the destination space.
    max_iter : The maximum number of iterations to use to find a solution.
    key : A key used for initialization of random projection if the number of
        input points is lower than the input dimension.
    gtol : Tolerance used for terminating optimization from gradient norm.
    xtol : Tolerance used for terminating optimization from trust region size.

    Returns
    -------
    result : (n, n_components)
        The reduced dimensional version of data.
    """
    num, _ = data.shape
    xi, yi = jnp.triu_indices(num, 1)
    ref = in_metric(data[xi], data[yi])

    init = utils.init(data, n_components, key)
    res = spo.minimize(
        _fun,  # type: ignore
        init.flatten(),
        (ref, out_metric, num, n_components),
        jac=jax.grad(_fun),  # type: ignore
        method="trust-constr",
        options={"maxiter": max_iter, "gtol": gtol, "xtol": xtol},
    )
    if not res.success:  # pragma: no cover
        raise RuntimeError(f"optimization failed with: {res.message}")
    return jnp.array(res.x.reshape(num, n_components))

from functools import partial

import jax
import numpy as np
from jax import Array, lax, random
from jax import numpy as jnp
from jax.scipy import special as jss
from scipy import optimize as spo

from . import _utils as utils
from .measure import Measure, cauchy, gaussian
from .metric import Metric, euclidean


@partial(jax.vmap, in_axes=[0, None, None, None])
def _fit_probs(dists: Array, target: float, measure: Measure, tol: float) -> Array:
    @jax.jit
    def ent(mult_dists: Array) -> Array:
        probs = measure(mult_dists)
        probs = probs / probs.sum()
        return jss.xlogy(probs, probs).sum()

    def _less() -> tuple[float, float]:
        upper = lax.while_loop(
            lambda upper: ent(dists * upper) < target,
            lambda upper: upper * 2.0,
            2.0,
        )
        return upper / 2.0, upper

    def _more() -> tuple[float, float]:
        lower = lax.while_loop(
            lambda lower: ent(dists * lower) > target,
            lambda lower: lower / 2.0,
            0.5,
        )
        return lower, lower * 2.0

    lower, upper = lax.cond(ent(dists) < target, _less, _more)
    mid = lower + (upper - lower) / 2.0
    val = ent(dists * mid)

    def _bisect_cond(dat: tuple[Array, float, float]) -> Array:
        val, _, _ = dat
        return jnp.abs(val - target) > tol

    def _bisect_body(dat: tuple[Array, float, float]) -> tuple[Array, float, float]:
        _, lower, upper = dat
        mid = lower + (upper - lower) / 2.0
        val = ent(dists * mid)
        return lax.cond(
            val > target,
            lambda: (val, lower, mid),
            lambda: (val, mid, upper),
        )

    _, lower, upper = lax.while_loop(_bisect_cond, _bisect_body, (val, lower, upper))
    mult = lower + (upper - lower) / 2
    pi = measure(dists * mult)
    return pi / pi.sum()


@partial(jax.jit, static_argnames=["metric", "measure", "num", "dim"])
def _fun(  # noqa: PLR0913
    x: Array,
    p: Array,
    scale: float,
    metric: Metric,
    measure: Measure,
    num: int,
    dim: int,
) -> Array:
    points = x.reshape(num, dim)
    xi, yi = jnp.triu_indices(num, 1)
    dists = metric(points[xi], points[yi]) * scale
    q = measure(dists)
    # we omit p.sum() since it's one
    return jnp.log(q.sum()) - p @ jnp.log(q)


ZERO_KEY = random.key(0)


def sne(  # noqa: PLR0913
    data: Array,
    n_components: int = 2,
    *,
    perplexity: float = 30,
    in_metric: Metric = euclidean,
    in_measure: Measure = gaussian,
    out_metric: Metric = euclidean,
    out_measure: Measure = cauchy,
    out_scale: float | None = None,
    max_iter: int = 10024,
    key: Array = ZERO_KEY,
    ptol: float = 1e-6,
    gtol: float = 1e-6,
    xtol: float = 1e-6,
) -> Array:
    """Reduce dimension using Stochastic Neighbor Embeddings.

    The default implementation of this performs exact tSNE, but alternate metric
    spaces and distributions can be passed in to perform other variants. Custom
    metric and distribution functions must be jax jit-able.

    Parameters
    ----------
    data : (n, d)
        The input data in "high dimensional" d space.
    n_components : The dimension of the space to reduce to.
    perplexity : This is effectively a smoothing parameter that should be
        adjusted to gain the insights desired. A recommended range is [20, 50]
    in_metric : The metric space of data.
        (t-SNE = euclidian, vMF-SNE = cosine)
    in_measure : The distribution to use over the input metric space.
        (t-SNE = gaussian, vMF-SNE = laplace)
    out_metric : The desired metric space of the output. See information in the
        metrics for you might want to scale these.
        (t-SNE = euclidian, vMF-SNE = cosine)
    out_measure : The distribution for matching the output metrics.
        (t-SNE = cauchy, vMF-SNE = laplace)
    out_scale : It can be beneficial to scale the output metric space to help
        with alignment.  This is especially import in more fixed spaces like
        cosine and poincare, and matters less for euclidian out_metric.
    max_iter : The maximum number of iterations used to optimize the result.
        This can be adjusted if the optimization is failing for that reason and
        you're willing to wait longer.
    key : The key (seed) used for random projection if necessary to initialize
        the result data. If you're in this regime and want to try different
        initializations you can pass `key=jax.random.key(seed)`
    ptol : Tolerance used for perplexity matching the input.
    gtol : Tolerance used for terminating optimization from gradient norm.
    xtol : Tolerance used for terminating optimization from trust region size.

    Returns
    -------
    result : (n, n_components)
        The resulting data projected into n_components dimensions.

    Remarks
    -------
    Due to the flexibility of this method, it's not as readily amenable to the
    improvements of the Barnes-Hut approximation. As a gneral rule it is also
    alsower than the scikit-learn's TSNE in exact mode, so only use this if want
    alternate metric spaces or distributions.
    """
    num, _ = data.shape
    if out_scale is None:
        out_scale = num / perplexity

    # compute all pairwise distances
    all_dists = in_metric(data[None], data[:, None])
    # this is a proxy for a starting multiplier
    all_dists = all_dists / jnp.mean(all_dists, 1)[:, None]
    all_dists = jnp.fill_diagonal(all_dists, jnp.inf, inplace=False)

    # find the optimal distribution for perplexity
    probs = _fit_probs(all_dists, -np.log(perplexity), in_measure, ptol)
    xi, yi = jnp.triu_indices(num, 1)
    ps = probs[xi, yi] + probs[yi, xi]
    ps = ps / ps.sum()

    init = utils.init(data, n_components, key)
    res = spo.minimize(
        _fun,  # type: ignore
        init.flatten(),
        (ps, out_scale, out_metric, out_measure, num, n_components),
        jac=jax.grad(_fun),  # type: ignore
        method="trust-constr",
        options={"maxiter": max_iter, "gtol": gtol, "xtol": xtol},
    )
    if not res.success:  # pragma: no cover
        raise RuntimeError(f"optimization failed with: {res.message}")
    return jnp.array(res.x.reshape(num, n_components))

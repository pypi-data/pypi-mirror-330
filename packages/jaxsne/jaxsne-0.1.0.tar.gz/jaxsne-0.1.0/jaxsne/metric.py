"""Metrics for jaxsne.

A metric function is simply a valid distance between points in a space. In order
for arbitrary metrics to work with this library, they have to satisfy a few
properties:

1. They must be proper [metrics](https://en.wikipedia.org/wiki/Metric_space),
   notably they must be zero for identical points, and satisfy positivity,
   symmetry, and the triangle inequality.
2. They must treat the last dimension as the dimension of the points.
3. They must be [jax jit-able](https://docs.jax.dev/en/latest/jit-compilation.html).
4. They must apply to points in R^d, if they actually apply to some subset of
   points, they should first project homeomorphically into a space of the same
   dimension.
"""

from ._metric import Metric, cosine, euclidean, poincare

__all__ = ("cosine", "euclidean", "poincare", "Metric")

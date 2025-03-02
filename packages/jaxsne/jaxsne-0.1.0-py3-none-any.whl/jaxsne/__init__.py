"""A jax library for doing dimensionality reduction.

jaxsne is a library for doing dimensionality reduction, with two main methods:
`scaling` for multi-dimensional scaling that tried to match distances directly
between spaces, and `sne` a generic form of t-SNE that instead matches the
distribution of distances,

This library uses jax, so users can define their own measures for `sne` or their
own metrics for both, making is robust to different needs. However this library
is intended to come with batteries included, so doing `scaling(data)` or
`sne(data)` will just work.

Remarks
-------
It's important to note that this implements exact SNE instead of using the
optimizations from Barnes-Hut. This means that it is much less performant than
the t-SNE provided by scikit-learn, and in general is also less optimized than
their exact version, so only use library if you want other metric spaces.
"""

from . import measure, metric
from ._scaling import scaling
from ._sne import sne

__all__ = (
    "measure",
    "metric",
    "scaling",
    "sne",
)

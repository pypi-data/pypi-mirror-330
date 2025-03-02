"""Measure for jaxsne.

A measure is a mapping from distances (non-negative) to masses. Since SNE
empirically normalizes all distirbutions, these don't need to be normalized, and
should also omit scaling of the distance, even if the standard measure would, as
that is also handled by SNE.

1. They must be proper [measures](https://en.wikipedia.org/wiki/Measure_(mathematics)),
   which just means they should be non-negative.
2. They will only be called for positive inputs.
3. They must be [jax jit-able](https://docs.jax.dev/en/latest/jit-compilation.html).
"""

from ._measure import Measure, cauchy, gaussian, laplace

__all__ = ("gaussian", "cauchy", "laplace", "Measure")

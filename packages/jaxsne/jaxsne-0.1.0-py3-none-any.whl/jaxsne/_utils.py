from jax import Array, random
from jax import numpy as jnp


def rproj(data: Array, n_components: int, key: Array) -> Array:
    """Perform random projection."""
    _, dim = data.shape
    proj = random.normal(key, (dim, n_components))
    return data @ proj


def pca(data: Array, n_components: int) -> Array:
    """Perform Principle Component Analysis."""
    normed = data - jnp.mean(data, 0)
    normed = normed / (normed.std(0) + 1e-6)
    vals, vecs = jnp.linalg.eig(normed.T @ normed)
    inds = jnp.argpartition(-vals.real, n_components)[:n_components]
    return normed @ vecs.real[:, inds]


def init(data: Array, n_components: int, key: Array) -> Array:
    """Initialize reduced dimensional data.

    If there are enough points, PCA is used, otherwise this falls back to random
    projection.
    """
    num, dim = data.shape
    if num < dim:
        return rproj(data, n_components, key)
    else:
        return pca(data, n_components)

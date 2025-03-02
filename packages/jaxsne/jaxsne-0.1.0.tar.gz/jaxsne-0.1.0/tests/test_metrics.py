"""Test that metric functions work as epxected."""

from jax import numpy as jnp
from jax import random

from jaxsne import metric


def test_euclidean_known() -> None:
    """Test known euclidian distances."""
    left = jnp.array([[3, 4], [3, 4]])
    right = jnp.array([[3, 4], [0, 0]])
    res = metric.euclidean(left, right)
    expected = jnp.array([0, 5])
    assert jnp.allclose(res, expected)


def test_euclidean_shape() -> None:
    """Test euclidean shapes match."""
    key = random.key(0)
    left_key, right_key = random.split(key)
    left = random.normal(left_key, (10, 4, 3))
    right = random.normal(right_key, (1, 4, 3))
    dists = metric.euclidean(left, right)
    assert dists.shape == (10, 4)


def test_cosine_known() -> None:
    """Test known cosine distances."""
    left = jnp.array([[1, 0], [1, 0], [1, 0]])
    right = jnp.array([[1, 0], [0, 1], [-1, 0]])
    res = metric.cosine(left, right)
    expected = jnp.array([0, 1 / 2, 1])
    assert jnp.allclose(res, expected)


def test_cosine_invariant() -> None:
    """Test that normalizing prior to cosine dist doesn't matter."""
    key = random.key(0)
    left_key, right_key = random.split(key)
    left = random.normal(left_key, (10, 4, 3))
    right = random.normal(right_key, (1, 4, 3))
    dists = metric.cosine(left, right)
    assert dists.shape == (10, 4)

    mult_dists = metric.cosine(left * 2, right / 3)
    assert jnp.allclose(dists, mult_dists)


def test_poincare_known() -> None:
    """Test some known poincare distances."""
    left = jnp.array([[0, 1], [0, 1]])  # [0, 1/2]
    right = jnp.array([[0, 0], [0, 1 / 3]])  # [0, 1/4]
    res = metric.poincare(left, right)
    expected = jnp.log(jnp.array([3, 9 / 5]))
    assert jnp.allclose(res, expected)


def test_poncare_shape() -> None:
    """Test poincare shapes match."""
    key = random.key(0)
    left_key, right_key = random.split(key)
    left = random.normal(left_key, (10, 4, 3))
    right = random.normal(right_key, (1, 4, 3))
    dists = metric.poincare(left, right)
    assert dists.shape == (10, 4)

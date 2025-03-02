"""Tests for scaling."""

import pytest
from jax import random

import jaxsne
from jaxsne import metric
from jaxsne.metric import Metric


def test_random_scaling() -> None:
    """Test default execution reduces dimension."""
    key = random.key(0)
    data = random.normal(key, (100, 5))
    res = jaxsne.scaling(data)
    assert res.shape == (100, 2)


def test_small_scaling() -> None:
    """Test default works even with a small number of points."""
    key = random.key(0)
    data = random.normal(key, (50, 70))
    res = jaxsne.scaling(data)
    assert res.shape == (50, 2)


@pytest.mark.parametrize(
    "out_dim,in_metric,out_metric",
    [
        # euclidean
        (2, metric.euclidean, metric.euclidean),
        # 3d euclidean
        (3, metric.euclidean, metric.euclidean),
        # cosine
        (3, metric.cosine, metric.cosine),
    ],
)
def test_scaling_custom(
    out_dim: int,
    in_metric: Metric,
    out_metric: Metric,
) -> None:
    """Test that customizations work."""
    key = random.key(0)
    data = random.normal(key, (64, 5))
    res = jaxsne.scaling(
        data,
        out_dim,
        in_metric=in_metric,
        out_metric=out_metric,
        max_iter=2048,
    )
    assert res.shape == (64, out_dim)

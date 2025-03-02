"""Tests for the sne function."""

import pytest
from jax import random

import jaxsne
from jaxsne import measure, metric
from jaxsne.measure import Measure
from jaxsne.metric import Metric


def test_random_sne() -> None:
    """Test default execution reduces dimension."""
    key = random.key(0)
    data = random.normal(key, (100, 5))
    res = jaxsne.sne(data)
    assert res.shape == (100, 2)


def test_small_sne() -> None:
    """Test default works even with a small number of points."""
    key = random.key(0)
    data = random.normal(key, (50, 70))
    res = jaxsne.sne(data)
    assert res.shape == (50, 2)


@pytest.mark.parametrize(
    "out_dim,in_metric,in_measure,out_metric,out_measure",
    [
        # tSNE
        (2, metric.euclidean, measure.gaussian, metric.euclidean, measure.cauchy),
        # 3d tSNE
        (3, metric.euclidean, measure.gaussian, metric.euclidean, measure.cauchy),
        # vMF-SNE
        (3, metric.cosine, measure.laplace, metric.cosine, measure.laplace),
        # poincare SNE
        (2, metric.cosine, measure.gaussian, metric.poincare, measure.cauchy),
    ],
)
def test_sne_custom(
    out_dim: int,
    in_metric: Metric,
    in_measure: Measure,
    out_metric: Metric,
    out_measure: Measure,
) -> None:
    """Test that customizations work."""
    key = random.key(0)
    data = random.normal(key, (64, 5))
    res = jaxsne.sne(
        data,
        out_dim,
        in_metric=in_metric,
        in_measure=in_measure,
        out_metric=out_metric,
        out_measure=out_measure,
        max_iter=2048,
    )
    assert res.shape == (64, out_dim)

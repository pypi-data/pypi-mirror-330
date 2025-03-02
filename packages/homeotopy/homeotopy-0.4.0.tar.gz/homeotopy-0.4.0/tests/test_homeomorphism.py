"""Tests for the homeomorphism builder."""

import numpy as np

import homeotopy


def test_composition() -> None:
    """Test composing transforms with homeomorphism."""
    rng = np.random.default_rng()
    homeo = homeotopy.homeomorphism(homeotopy.simplex(), homeotopy.sphere())

    simplex = rng.dirichlet(np.ones(4), (2, 5))
    sphere = homeo(simplex)
    assert np.allclose(np.linalg.norm(sphere, 2, -1), 1)

    inv = ~homeo
    actual = inv(sphere)
    assert np.allclose(simplex, actual)

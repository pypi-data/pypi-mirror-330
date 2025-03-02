import numpy as np

import homeotopy


def test_known() -> None:
    sphere = homeotopy.sphere()

    sphere_points = np.array([[1, 0, 0], [0, 1, 0], [1 / 2, 0, 3**0.5 / 2]], "f8")
    inf_ball_points = np.array([[1, 1], [np.tanh(1), 0], [0, np.tanh(3**0.5)]], "f8")
    assert np.allclose(sphere.to_inf_ball(sphere_points), inf_ball_points)
    assert np.allclose(sphere.from_inf_ball(inf_ball_points), sphere_points)


def test_random() -> None:
    rng = np.random.default_rng(0)
    sphere = homeotopy.sphere()

    inf_ball_points = rng.uniform(-1, 1, (3, 4, 5))
    sphere_points = sphere.from_inf_ball(inf_ball_points)
    assert np.allclose(sphere.to_inf_ball(sphere_points), inf_ball_points)
    assert np.allclose(np.linalg.norm(sphere_points, 2, -1), 1)

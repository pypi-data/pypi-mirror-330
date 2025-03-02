import numpy as np

import homeotopy


def test_known() -> None:
    plane = homeotopy.plane()

    plane_points = np.array(
        [[0, 0, 0], [np.inf, np.inf, -np.inf], [3, -5, 1 / 2]], "f8"
    )
    inf_ball_points = np.array([[0, 0, 0], [1, 1, -1], [3 / 4, -5 / 6, 1 / 3]], "f8")
    assert np.allclose(plane.to_inf_ball(plane_points), inf_ball_points)
    assert np.allclose(plane.from_inf_ball(inf_ball_points), plane_points)


def test_random() -> None:
    rng = np.random.default_rng(0)
    plane = homeotopy.plane()

    inf_ball_points = rng.uniform(-1, 1, (3, 4, 5))
    plane_points = plane.from_inf_ball(inf_ball_points)
    assert np.allclose(plane.to_inf_ball(plane_points), inf_ball_points)

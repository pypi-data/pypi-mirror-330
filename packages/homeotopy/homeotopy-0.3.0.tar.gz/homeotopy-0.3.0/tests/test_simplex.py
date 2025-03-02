import numpy as np

import homeotopy


def test_known() -> None:
    simplex = homeotopy.simplex()

    simplex_points = np.array(
        [[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 1 / 2, 1 / 2], [1 / 3, 1 / 3, 1 / 3]],
        "f8",
    )
    inf_ball_points = np.array(
        [[-1, -1 / 3**0.5], [1, -1 / 3**0.5], [0, 1], [1, 1 / 3**0.5], [0, 0]], "f8"
    )
    assert np.allclose(simplex.to_inf_ball(simplex_points), inf_ball_points)
    assert np.allclose(simplex.from_inf_ball(inf_ball_points), simplex_points)


def test_random() -> None:
    rng = np.random.default_rng(0)
    simplex = homeotopy.simplex()

    inf_ball_points = rng.uniform(-1, 1, (3, 4, 5))
    simplex_points = simplex.from_inf_ball(inf_ball_points)
    assert np.allclose(simplex.to_inf_ball(simplex_points), inf_ball_points)

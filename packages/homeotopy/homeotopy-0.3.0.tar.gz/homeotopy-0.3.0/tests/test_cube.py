import numpy as np

import homeotopy


def test_known() -> None:
    cube = homeotopy.cube()

    cube_points = np.array([[0, 0, 0], [1, 1, 1], [0.5, 0.5, 0.5]], "f8")
    inf_ball_points = np.array([[-1, -1, -1], [1, 1, 1], [0, 0, 0]], "f8")
    assert np.allclose(cube.to_inf_ball(cube_points), inf_ball_points)
    assert np.allclose(cube.from_inf_ball(inf_ball_points), cube_points)


def test_random() -> None:
    rng = np.random.default_rng(0)
    cube = homeotopy.cube()

    inf_ball_points = rng.uniform(-1, 1, (3, 4, 5))
    cube_points = cube.from_inf_ball(inf_ball_points)
    assert np.allclose(cube.to_inf_ball(cube_points), inf_ball_points)
    assert np.all(0 <= cube_points) and np.all(cube_points <= 1)

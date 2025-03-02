import numpy as np
import pytest

import homeotopy


def test_known() -> None:
    ball = homeotopy.ball()

    ball_points = np.array(
        [
            [0, 0, 0],
            [0, 0, 1],
            [0, 1 / 2**0.5, 1 / 2**0.5],
            [1 / 3**0.5, 1 / 3**0.5, -1 / 3**0.5],
            [1 / 2, -1 / 2, 1 / 2],
        ],
        "f8",
    )
    inf_ball_points = np.array(
        [
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 1],
            [1, 1, -1],
            [3**0.5 / 2, -(3**0.5) / 2, 3**0.5 / 2],
        ],
        "f8",
    )
    assert np.allclose(ball.to_inf_ball(ball_points), inf_ball_points)
    assert np.allclose(ball.from_inf_ball(inf_ball_points), ball_points)


@pytest.mark.parametrize("p", [0.5, 1, 2, 3])
def test_random(p: float) -> None:
    rng = np.random.default_rng(0)
    ball = homeotopy.ball(p=p)

    inf_ball_points = rng.uniform(-1, 1, (3, 4, 5))
    inf_norms = np.abs(inf_ball_points).max(-1)
    ball_points = ball.from_inf_ball(inf_ball_points)
    ball_norms = np.linalg.norm(ball_points, ball.p, -1)

    assert np.allclose(ball.to_inf_ball(ball_points), inf_ball_points)
    assert np.all(np.linalg.norm(ball_points, ball.p, -1) <= 1)
    assert np.allclose(inf_norms, ball_norms)

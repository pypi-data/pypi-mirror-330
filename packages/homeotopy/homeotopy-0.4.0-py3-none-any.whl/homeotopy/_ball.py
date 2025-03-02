import math
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from ._homeomorphism import Topology


@dataclass(frozen=True, slots=True)
class Ball(Topology):
    """The topology of the p-norm ball.

    This represents all points in R^n s.t. ||x||_p < 1, although it should also
    work fo the boundary.
    """

    p: float

    def __post_init__(self) -> None:
        if self.p <= 0:
            raise ValueError(f"p must be greater than or equal to 0: {self.p:g}")

    def to_inf_ball(self, points: NDArray[np.float64]) -> NDArray[np.float64]:
        if self.p == math.inf:
            return points
        else:
            tiny = np.finfo(points.dtype).smallest_normal
            source = np.linalg.norm(points, self.p, -1)
            target = np.abs(points).max(-1) + tiny
            return np.clip(points * (source / target)[..., None], -1, 1)  # type: ignore

    def from_inf_ball(self, points: NDArray[np.float64]) -> NDArray[np.float64]:
        if self.p == math.inf:
            return points
        else:
            tiny = np.finfo(points.dtype).smallest_normal
            source = np.abs(points).max(-1)
            target = np.linalg.norm(points, self.p, -1) + tiny
            return points * (source / target)[..., None]  # type: ignore


def ball(p: float = 2.0) -> Ball:
    """Create a topology of the interior of the p-norm unit ball."""
    return Ball(p)

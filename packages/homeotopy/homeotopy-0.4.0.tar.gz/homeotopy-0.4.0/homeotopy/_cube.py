from dataclasses import dataclass
from functools import cache

import numpy as np
from numpy.typing import NDArray

from ._homeomorphism import Topology


@dataclass(frozen=True, slots=True)
class Cube(Topology):
    """The topology of the unit hyper cube.

    This represents all points in R^n s.t 0 < x_i < 1, although the boundary
    should also work.
    """

    def to_inf_ball(self, points: NDArray[np.float64]) -> NDArray[np.float64]:
        return np.clip(points * 2 - 1, -1, 1)

    def from_inf_ball(self, points: NDArray[np.float64]) -> NDArray[np.float64]:
        return np.clip((points + 1) / 2, 0, 1)


@cache
def cube() -> Cube:
    """Create a topology of the unit cube."""
    return Cube()

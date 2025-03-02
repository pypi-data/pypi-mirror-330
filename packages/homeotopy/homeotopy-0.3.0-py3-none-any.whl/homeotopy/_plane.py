from dataclasses import dataclass
from functools import cache

import numpy as np
from numpy.typing import NDArray

from ._homeomorphism import Topology


@dataclass(frozen=True, slots=True)
class Plane(Topology):
    """The topology of the euclidian plane.

    This represents all points in R^n, but boundary points map to inf.

    Remarks
    -------
    While translations will keep all points valid, this will try to keep points
    at the "center" of the space mapped to (0, 0, ..., 0).
    """

    def to_inf_ball(self, points: NDArray[np.float64]) -> NDArray[np.float64]:
        info = np.finfo(points.dtype)
        # max and inf will both get promoted to 1
        clipped = np.clip(points, info.min, info.max)
        return clipped / (1 + np.abs(clipped))

    def from_inf_ball(self, points: NDArray[np.float64]) -> NDArray[np.float64]:
        clipped = np.clip(points, -1, 1)
        # this triggers at -1 and 1
        with np.errstate(divide="ignore"):
            return clipped / (1 - np.abs(clipped))


@cache
def plane() -> Plane:
    """Create a topology of the euclidian plane."""
    return Plane()

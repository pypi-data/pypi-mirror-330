from dataclasses import dataclass
from functools import cache

import numba as nb
import numpy as np
from numpy.typing import NDArray

from ._homeomorphism import Topology

# NOTE we use this to avoid divide by zero errors


@nb.jit(nb.float64[:, ::1](nb.int64), parallel=True, cache=True, nogil=True)
def basis(dim: int) -> NDArray[np.float64]:  # pragma: no cover # can't trace numba
    """Create a basis for rotating the simplex onto the origin of dim - 1."""
    res = np.empty((dim, dim))
    for i in nb.prange(0, dim - 1):
        num = i + 1
        frac = 1 / (num + 1)
        res[i, :num] = -((frac / num) ** 0.5)
        res[i, num] = (1 - frac) ** 0.5
        res[i, num + 1 :] = 0
    res[-1] = (1 / dim) ** 0.5
    return res


@dataclass(frozen=True, slots=True)
class Simplex(Topology):
    """The topology of the simplex.

    This represents all points in R^n s.t. 0 < x_i and Σx_i = 1.
    """

    def to_inf_ball(self, points: NDArray[np.float64]) -> NDArray[np.float64]:
        tiny = np.finfo(points.dtype).smallest_normal
        d = points.shape[-1]

        simp_direc = points - np.full(d, 1 / d)
        isimp_a = d * np.maximum(-simp_direc, simp_direc / (d - 1)).max(-1)

        cube_direc = simp_direc @ basis(d)[: d - 1].T
        icube_a = np.max(np.abs(cube_direc), -1) + tiny

        return np.clip(cube_direc * (isimp_a / icube_a)[..., None], -1, 1)  # type: ignore

    def from_inf_ball(self, points: NDArray[np.float64]) -> NDArray[np.float64]:
        tiny = np.finfo(points.dtype).smallest_normal
        d = points.shape[-1]

        icube_a = np.max(np.abs(points), -1)

        simp_direc = np.insert(points, d, 0, -1) @ basis(d + 1)
        isimp_a = (d + 1) * np.maximum(-simp_direc, simp_direc / d).max(-1) + tiny

        raw = simp_direc * (icube_a / isimp_a)[..., None] + np.full(d + 1, 1 / (d + 1))
        return np.clip(raw, 0, 1)  # type: ignore


@cache
def simplex() -> Simplex:
    """Create the topology of the simplex."""
    return Simplex()

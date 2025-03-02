from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


class Topology(ABC):
    """An abstract topological space.

    For this library to work, each Topologiy should define a homeomorphism from
    it to the inf-norm ball.

    Remarks
    -------
    `to_inf_ball` and `from_inf_ball` are not meant to be called in isolation,
    but rather used in combination with `homeomorphism`.
    """

    @abstractmethod
    def to_inf_ball(self, points: NDArray[np.float64]) -> NDArray[np.float64]:
        """Map a set of points in this topology to the inf-ball.

        Parameters
        ----------
        points : (..., d_in)
            A set of points in the input topological space

        Returns
        -------
        points : (..., d_out)
            A set of points in the inf-norm ball, e.g. -1 < x_i < 1 for points
            in the open topology, but points can be mapped to the border for
            border points in the source topology.
        """
        ...  # pragma: no cover

    @abstractmethod
    def from_inf_ball(self, points: NDArray[np.float64]) -> NDArray[np.float64]:
        """Map a set of points from the inf-ball to this topology.

        Parameters
        ----------
        points : (..., d_in)
            A set of points in the inf-norm ball, e.g. -1 < x_i < 1 for points
            in the open topology, but points on the boarder should be handled as
            well.

        Returns
        -------
        points : (..., d_out)
            A set of points in the topological space.
        """
        ...  # pragma: no cover


@dataclass(frozen=True, slots=True)
class Homeomorphism:
    """A homeomorphism from source to target.

    Homeomorphisms can be called on points in the source domain to map them to
    points in the target domain. They can also be `inverted` to create the
    inverse mapping.


    Example
    -------

        from homeotopy import homeomorphism, ball, simplex
        import numpy as np

        forward = homeomorphism(ball(1), simplex())
        backward = ~forward

        ball_points = ...
        simplex_points = forwad(ball_points)
        backward(simplex_points)

    """

    source: Topology
    target: Topology

    def __invert__(self) -> Homeomorphism:
        return Homeomorphism(self.target, self.source)

    def __call__(self, points: NDArray[np.float64]) -> NDArray[np.float64]:
        return self.target.from_inf_ball(self.source.to_inf_ball(points))


def homeomorphism(source: Topology, target: Topology) -> Homeomorphism:
    """Create a Homeomorphism from a source and a target topology."""
    return Homeomorphism(source, target)

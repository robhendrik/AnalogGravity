"""Spatial and temporal grid definitions for the rope simulation."""

from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True, slots=True)
class Grid:
    """Uniform one-dimensional grid.

    Parameters
    ----------
    x_min, x_max:
        Domain limits. Both end points are included.
    nx:
        Number of spatial grid points.
    dt:
        Time step. It can be left as ``None`` until a medium is known.
    """

    x_min: float
    x_max: float
    nx: int
    dt: float | None = None

    def __post_init__(self) -> None:
        if self.nx < 3:
            raise ValueError("nx must be at least 3")
        if not self.x_max > self.x_min:
            raise ValueError("x_max must be greater than x_min")
        if self.dt is not None and self.dt <= 0.0:
            raise ValueError("dt must be positive")

    @property
    def x(self) -> NDArray[np.float64]:
        """Coordinates of the grid points."""
        return np.linspace(self.x_min, self.x_max, self.nx, dtype=float)

    @property
    def dx(self) -> float:
        """Uniform grid spacing."""
        return (self.x_max - self.x_min) / (self.nx - 1)

    def with_dt(self, dt: float) -> "Grid":
        """Return a copy with a validated time step."""
        if dt <= 0.0:
            raise ValueError("dt must be positive")
        return replace(self, dt=float(dt))

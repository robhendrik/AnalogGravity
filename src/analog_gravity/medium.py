"""Static background medium for the moving-rope analogue."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from .grid import Grid


@dataclass(frozen=True, slots=True)
class Medium:
    """Constant intrinsic wave speed and prescribed background advection.

    The Round-1 model keeps ``c`` constant and treats ``v(x)`` as an
    externally prescribed effective advection field.
    """

    c: float
    v: NDArray[np.float64]

    def __post_init__(self) -> None:
        if self.c <= 0.0:
            raise ValueError("c must be positive")
        values = np.asarray(self.v, dtype=float)
        if values.ndim != 1:
            raise ValueError("v must be a one-dimensional array")
        if values.size < 3:
            raise ValueError("v must contain at least three grid values")
        if not np.all(np.isfinite(values)):
            raise ValueError("v must contain only finite values")
        object.__setattr__(self, "v", values)

    @classmethod
    def uniform(cls, grid: Grid, *, c: float, v_const: float = 0.0) -> "Medium":
        """Construct a spatially uniform medium."""
        return cls(c=float(c), v=np.full(grid.nx, float(v_const), dtype=float))

    @classmethod
    def white_hole_ramp(
        cls,
        grid: Grid,
        *,
        c: float,
        v0: float,
        v1: float,
        x0: float,
        width: float,
    ) -> "Medium":
        """Construct the white-hole tanh flow profile from the simulation spec.

        ``v0`` and ``v1`` are positive speed magnitudes. The actual flow is
        leftward, hence negative.
        """
        if v0 < 0.0 or v1 <= 0.0:
            raise ValueError("v0 must be >= 0 and v1 must be > 0")
        if width <= 0.0:
            raise ValueError("width must be positive")
        x = grid.x
        v = -(v0 + 0.5 * v1 * (1.0 + np.tanh((x - x0) / width)))
        return cls(c=float(c), v=v)

    def recommended_dt(self, grid: Grid, *, cfl: float = 0.5) -> float:
        """Return a conservative CFL time step based on ``max(|v| + c)``."""
        if not 0.0 < cfl <= 1.0:
            raise ValueError("cfl must lie in (0, 1]")
        max_characteristic_speed = float(np.max(np.abs(self.v) + self.c))
        return cfl * grid.dx / max_characteristic_speed

    def dv_dx(self, grid: Grid) -> NDArray[np.float64]:
        """Numerical derivative of the prescribed background flow."""
        if grid.nx != self.v.size:
            raise ValueError("grid and medium sizes do not match")
        return np.gradient(self.v, grid.dx, edge_order=2)

    def numerical_horizon_position(self, grid: Grid) -> float:
        """Locate the first crossing of ``|v| = c`` by linear interpolation."""
        if grid.nx != self.v.size:
            raise ValueError("grid and medium sizes do not match")
        f = np.abs(self.v) - self.c
        exact = np.flatnonzero(np.isclose(f, 0.0, atol=1e-14, rtol=0.0))
        if exact.size:
            return float(grid.x[exact[0]])

        crossings = np.flatnonzero(f[:-1] * f[1:] < 0.0)
        if crossings.size == 0:
            raise ValueError("the medium contains no |v| = c horizon")
        i = int(crossings[0])
        x1, x2 = grid.x[i], grid.x[i + 1]
        f1, f2 = f[i], f[i + 1]
        return float(x1 - f1 * (x2 - x1) / (f2 - f1))


def analytic_white_hole_horizon(
    *, c: float, v0: float, v1: float, x0: float, width: float
) -> float:
    """Analytic horizon position for the tanh white-hole profile.

    Solves ``v0 + v1/2 * (1 + tanh((x-x0)/width)) = c``.
    """
    if c <= 0.0 or v0 < 0.0 or v1 <= 0.0 or width <= 0.0:
        raise ValueError("invalid ramp parameters")
    q = 2.0 * (c - v0) / v1 - 1.0
    if not -1.0 < q < 1.0:
        raise ValueError("parameters do not place a horizon inside the tanh transition")
    return float(x0 + width * np.arctanh(q))

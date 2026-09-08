"""Initial-condition helpers."""

from __future__ import annotations

from typing import Literal

import numpy as np
from numpy.typing import NDArray

from .grid import Grid
from .medium import Medium

Branch = Literal["against_flow", "with_flow"]


def _first_derivative(values: NDArray[np.float64], dx: float) -> NDArray[np.float64]:
    return np.gradient(values, dx, edge_order=2)


def make_wavepacket(
    grid: Grid,
    medium: Medium,
    *,
    x_center: float,
    width: float,
    k0: float,
    branch: Branch = "against_flow",
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Create a Gaussian carrier packet and a branch-consistent initial velocity.

    For the incident/against-flow branch, the local nondispersive relation is
    ``omega = (v + c) k``.  To leading WKB order a right-moving profile obeys
    ``y_t = -(v + c) y_x``.  The other branch uses ``v - c``.

    The relation is exact for uniform ``v`` and serves as the intended WKB
    initialization for a slowly varying ramp.
    """
    if medium.v.size != grid.nx:
        raise ValueError("grid and medium sizes do not match")
    if width <= 0.0:
        raise ValueError("width must be positive")
    if k0 < 0.0:
        raise ValueError("k0 must be non-negative")
    if branch not in ("against_flow", "with_flow"):
        raise ValueError(f"unknown branch: {branch}")

    xi = grid.x - x_center
    envelope = np.exp(-0.5 * (xi / width) ** 2)
    y0 = envelope * np.cos(k0 * xi)
    y_x = _first_derivative(y0, grid.dx)

    intrinsic_sign = 1.0 if branch == "against_flow" else -1.0
    local_phase_speed = medium.v + intrinsic_sign * medium.c
    ydot0 = -local_phase_speed * y_x
    return y0, ydot0

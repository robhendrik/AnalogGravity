"""Diagnostics for wave-packet propagation."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray
from scipy.signal import hilbert

from .grid import Grid
from .medium import Medium
from .wavepacket import Branch


def packet_center(
    x: NDArray[np.float64],
    y: NDArray[np.float64],
) -> float:
    """Estimate the center of a localized oscillatory wave packet.

    The real field ``y`` contains carrier oscillations, so using ``y**2``
    directly causes a small carrier-phase-dependent shift in the measured
    center.  We instead construct the analytic signal with a Hilbert
    transform and use its squared envelope as the weight.

    Parameters
    ----------
    x:
        Spatial coordinates.
    y:
        Real-valued wave field.

    Returns
    -------
    float
        Envelope-weighted packet center.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if x.ndim != 1 or y.ndim != 1:
        raise ValueError("x and y must be one-dimensional")
    if x.shape != y.shape:
        raise ValueError("x and y must have the same shape")

    envelope = np.abs(hilbert(y))
    weight = envelope**2
    total_weight = float(np.sum(weight))

    if total_weight <= 0.0:
        raise ValueError("wave field has zero total envelope weight")

    return float(np.sum(x * weight) / total_weight)


def track_packet_centers(
    grid: Grid,
    history: Sequence[NDArray[np.float64]],
) -> NDArray[np.float64]:
    """Measure the packet center for every stored simulation snapshot."""
    if len(history) == 0:
        raise ValueError("history must contain at least one snapshot")

    centers = [
        packet_center(grid.x, np.asarray(snapshot, dtype=float))
        for snapshot in history
    ]
    return np.asarray(centers, dtype=float)


def measure_group_velocity(
    times: NDArray[np.float64],
    centers: NDArray[np.float64],
) -> float:
    """Measure packet group velocity from a linear fit to center vs. time.

    This diagnostic is intended for Step 2, where the medium is uniform and
    the packet trajectory should therefore be linear.

    Parameters
    ----------
    times:
        Snapshot times.
    centers:
        Packet-center positions corresponding to ``times``.

    Returns
    -------
    float
        Best-fit slope ``dx/dt``.
    """
    times = np.asarray(times, dtype=float)
    centers = np.asarray(centers, dtype=float)

    if times.ndim != 1 or centers.ndim != 1:
        raise ValueError("times and centers must be one-dimensional")
    if times.shape != centers.shape:
        raise ValueError("times and centers must have the same shape")
    if times.size < 2:
        raise ValueError("at least two samples are required")
    if np.any(np.diff(times) <= 0.0):
        raise ValueError("times must be strictly increasing")

    slope, _ = np.polyfit(times, centers, deg=1)
    return float(slope)


def expected_group_velocity(
    medium: Medium,
    *,
    branch: Branch,
) -> float:
    """Return the analytic group velocity for a uniform medium.

    For the nondispersive Round-1 dispersion relation

        omega = (v + c) k
        omega = (v - c) k,

    the corresponding group velocities are

        v_g = v + c
        v_g = v - c.

    Parameters
    ----------
    medium:
        Medium whose velocity must be spatially uniform.
    branch:
        ``"against_flow"`` for the ``v + c`` branch or ``"with_flow"``
        for the ``v - c`` branch.
    """
    if not np.allclose(medium.v, medium.v[0]):
        raise ValueError("expected_group_velocity requires uniform flow")

    v_const = float(medium.v[0])

    if branch == "against_flow":
        return v_const + medium.c
    if branch == "with_flow":
        return v_const - medium.c

    raise ValueError(f"unknown branch: {branch}")
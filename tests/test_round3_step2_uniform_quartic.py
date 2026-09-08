"""Round 3 Step 2 regression test: uniform dispersive propagation."""

from __future__ import annotations

import numpy as np
import pytest
from scipy.signal import hilbert

from analog_gravity import Grid, Medium
from analog_gravity.quartic import group_velocity_lab
from analog_gravity.simulation_quartic import QuarticSimulation


def _packet_center(
    x: np.ndarray,
    y: np.ndarray,
) -> float:
    envelope = np.abs(hilbert(y))
    weights = envelope**2
    return float(np.sum(x * weights) / np.sum(weights))


def test_uniform_quartic_packet_matches_group_velocity() -> None:
    """Measured packet velocity must match stabilized dispersion."""
    c = 1.0
    k_d = 6.0
    gamma = 0.30
    v = -0.25
    k0 = 1.5

    # Deliberately moderate dx: enough to resolve k0 very well while keeping
    # the explicit sextic solver affordable.
    grid = Grid(
        x_min=-30.0,
        x_max=30.0,
        nx=1201,
    )

    medium = Medium.uniform(
        grid,
        c=c,
        v_const=v,
    )

    x0 = -10.0
    width = 4.0

    y0 = (
        np.exp(
            -0.5 * ((grid.x - x0) / width) ** 2
        )
        * np.cos(
            k0 * (grid.x - x0)
        )
    )

    sim = QuarticSimulation.from_branch_initial_condition(
        grid,
        medium,
        c=c,
        k_d=k_d,
        gamma=gamma,
        y0=y0,
        branch=+1,
        safety=0.50,
    )

    center0 = _packet_center(
        grid.x,
        sim.state.y,
    )

    t_end = 3.0
    n_steps = round(
        t_end / sim.dt
    )

    sim.run(
        n_steps=n_steps
    )

    center1 = _packet_center(
        grid.x,
        sim.state.y,
    )

    measured_vg = (
        center1 - center0
    ) / sim.state.t

    expected_vg = float(
        group_velocity_lab(
            k0,
            v=v,
            c=c,
            k_d=k_d,
            gamma=gamma,
            branch=+1,
        )
    )

    assert measured_vg == pytest.approx(
        expected_vg,
        rel=0.02,
    )

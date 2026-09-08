"""Regression tests for Round 2, Step 3: uniform lattice propagation."""

from __future__ import annotations

import numpy as np
import pytest
from scipy.signal import hilbert

from analog_gravity import Grid, Medium
from analog_gravity.lattice import group_velocity_lab
from analog_gravity.simulation_dispersive import DispersiveSimulation


def _packet_center(x: np.ndarray, y: np.ndarray) -> float:
    """Envelope-squared center of a localized carrier wave."""
    envelope = np.abs(hilbert(y))
    weights = envelope**2
    return float(np.sum(x * weights) / np.sum(weights))


def test_uniform_lattice_packet_moves_at_dispersive_group_velocity() -> None:
    """Measured packet velocity must match v + c cos(k a / 2)."""
    c = 1.0
    a = 0.25
    v = -0.35

    grid = Grid(x_min=-30.0, x_max=30.0, nx=4801)
    medium = Medium.uniform(grid, c=c, v_const=v)

    x0 = -10.0
    width = 3.0
    k0 = 4.0

    y0 = (
        np.exp(-0.5 * ((grid.x - x0) / width) ** 2)
        * np.cos(k0 * (grid.x - x0))
    )

    sim = DispersiveSimulation.from_branch_initial_condition(
        grid,
        medium,
        c=c,
        lattice_spacing=a,
        y0=y0,
        branch=+1,
        cfl=0.25,
    )

    center0 = _packet_center(grid.x, sim.state.y)

    t_end = 5.0
    sim.run(n_steps=round(t_end / sim.dt))

    center1 = _packet_center(grid.x, sim.state.y)
    measured_vg = (center1 - center0) / sim.state.t

    expected_vg = float(
        group_velocity_lab(
            k0,
            v=v,
            c=c,
            lattice_spacing=a,
            branch=+1,
        )
    )

    assert measured_vg == pytest.approx(
        expected_vg,
        rel=0.02,
    )


def test_uniform_lattice_result_is_insensitive_to_numerical_dx() -> None:
    """Physical group velocity must not be set by the computational mesh."""
    c = 1.0
    a = 0.25
    v = -0.35

    x0 = -10.0
    width = 3.0
    k0 = 4.0
    t_end = 3.0

    measured: list[float] = []

    for nx in (2401, 4801):
        grid = Grid(x_min=-30.0, x_max=30.0, nx=nx)
        medium = Medium.uniform(grid, c=c, v_const=v)

        y0 = (
            np.exp(-0.5 * ((grid.x - x0) / width) ** 2)
            * np.cos(k0 * (grid.x - x0))
        )

        sim = DispersiveSimulation.from_branch_initial_condition(
            grid,
            medium,
            c=c,
            lattice_spacing=a,
            y0=y0,
            branch=+1,
            cfl=0.25,
        )

        center0 = _packet_center(grid.x, sim.state.y)
        sim.run(n_steps=round(t_end / sim.dt))
        center1 = _packet_center(grid.x, sim.state.y)

        measured.append(
            (center1 - center0) / sim.state.t
        )

    assert measured[0] == pytest.approx(
        measured[1],
        rel=0.01,
    )

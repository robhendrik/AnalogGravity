import numpy as np
import pytest

from analog_gravity import (
    Grid,
    Medium,
    Simulation,
    make_wavepacket,
)


def _centroid(
    x: np.ndarray,
    y: np.ndarray,
) -> float:
    """Simple energy-weighted packet position."""
    weight = y * y

    return float(
        np.sum(x * weight)
        / np.sum(weight)
    )


def test_zero_field_stays_zero_on_white_hole_ramp() -> None:
    """A ramp must not spontaneously generate numerical noise."""

    grid0 = Grid(
        -20.0,
        20.0,
        1201,
    )

    medium = Medium.white_hole_ramp(
        grid0,
        c=1.0,
        v0=0.25,
        v1=1.0,
        x0=2.0,
        width=3.0,
    )

    grid = grid0.with_dt(
        medium.recommended_dt(
            grid0,
            cfl=0.30,
        )
    )

    zero = np.zeros(
        grid.nx,
    )

    sim = Simulation.from_initial_conditions(
        grid,
        medium,
        zero,
        zero,
    )

    sim.run(
        n_steps=2000,
    )

    assert np.all(
        np.isfinite(
            sim.state.y_curr
        )
    )

    assert np.max(
        np.abs(
            sim.state.y_curr
        )
    ) == pytest.approx(
        0.0,
        abs=1e-14,
    )


def test_uniform_supersonic_against_flow_branch_is_stable() -> None:
    """The solver must also be stable when |v| > c."""

    grid0 = Grid(
        -20.0,
        20.0,
        1601,
    )

    medium = Medium.uniform(
        grid0,
        c=1.0,
        v_const=-1.2,
    )

    grid = grid0.with_dt(
        medium.recommended_dt(
            grid0,
            cfl=0.30,
        )
    )

    y0, ydot0 = make_wavepacket(
        grid,
        medium,
        x_center=5.0,
        width=1.2,
        k0=4.0,
        branch="against_flow",
    )

    sim = Simulation.from_initial_conditions(
        grid,
        medium,
        y0,
        ydot0,
    )

    initial_center = _centroid(
        grid.x,
        y0,
    )

    target_time = 3.0

    sim.run(
        n_steps=round(
            target_time
            / grid.dt
        )
    )

    final_center = _centroid(
        grid.x,
        sim.state.y_curr,
    )

    measured_velocity = (
        final_center
        - initial_center
    ) / sim.state.t

    # v + c = -1.2 + 1.0 = -0.2
    expected_velocity = -0.2

    assert np.all(
        np.isfinite(
            sim.state.y_curr
        )
    )

    assert np.max(
        np.abs(
            sim.state.y_curr
        )
    ) < (
        1.1
        * np.max(np.abs(y0))
    )

    assert measured_velocity == pytest.approx(
        expected_velocity,
        abs=0.03,
    )


def test_ramp_does_not_create_remote_supersonic_growth() -> None:
    """No artificial field should explode far ahead of the packet."""

    grid0 = Grid(
        -25.0,
        25.0,
        2001,
    )

    medium = Medium.white_hole_ramp(
        grid0,
        c=1.0,
        v0=0.25,
        v1=1.0,
        x0=2.0,
        width=3.0,
    )

    grid = grid0.with_dt(
        medium.recommended_dt(
            grid0,
            cfl=0.30,
        )
    )

    y0, ydot0 = make_wavepacket(
        grid,
        medium,
        x_center=-12.0,
        width=1.5,
        k0=5.0,
        branch="against_flow",
    )

    sim = Simulation.from_initial_conditions(
        grid,
        medium,
        y0,
        ydot0,
    )

    # At t=4 the physical packet is still far from x > 8.
    sim.run(
        n_steps=round(
            4.0
            / grid.dt
        )
    )

    remote_region = (
        grid.x > 8.0
    )

    assert np.all(
        np.isfinite(
            sim.state.y_curr
        )
    )

    assert np.max(
        np.abs(
            sim.state.y_curr[
                remote_region
            ]
        )
    ) < 1e-6
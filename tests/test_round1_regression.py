"""Physics regression tests for Round 1.

These tests protect the main nondispersive results demonstrated by the
moving-rope analogue-horizon simulations.

They are deliberately more physics-oriented than the lower-level unit tests.
"""

from __future__ import annotations

import numpy as np
import pytest

from analog_gravity import (
    Grid,
    Medium,
    Simulation,
    analytic_white_hole_horizon,
    make_wavepacket,
    packet_center,
)


# ============================================================
# Shared physical parameters
# ============================================================

C = 1.0

V0 = 0.25
V1 = 1.00
X0 = 2.0
W = 3.0


def _analytic_dv_dx(
    x: float,
    *,
    v1: float,
    x0: float,
    width: float,
) -> float:
    """Derivative of the tanh white-hole velocity profile."""
    z = (x - x0) / width

    sech_squared = 1.0 / np.cosh(z) ** 2

    return (
        -v1
        / (2.0 * width)
        * sech_squared
    )


def test_horizon_satisfies_v_plus_c_equals_zero() -> None:
    """The analytic horizon must coincide with v(x) + c = 0."""
    grid = Grid(
        x_min=-20.0,
        x_max=20.0,
        nx=4001,
    )

    medium = Medium.white_hole_ramp(
        grid,
        c=C,
        v0=V0,
        v1=V1,
        x0=X0,
        width=W,
    )

    x_h = analytic_white_hole_horizon(
        c=C,
        v0=V0,
        v1=V1,
        x0=X0,
        width=W,
    )

    v_h = np.interp(
        x_h,
        grid.x,
        medium.v,
    )

    assert v_h + C == pytest.approx(
        0.0,
        abs=2e-5,
    )


@pytest.mark.parametrize(
    ("width", "expected_kappa"),
    [
        (1.0, 0.375),
        (1.5, 0.250),
        (2.0, 0.1875),
        (3.0, 0.125),
        (4.0, 0.09375),
        (6.0, 0.0625),
    ],
)
def test_surface_gravity_matches_analytic_result(
    width: float,
    expected_kappa: float,
) -> None:
    """Numerical surface gravity must agree with the tanh profile."""
    grid = Grid(
        x_min=-20.0,
        x_max=20.0,
        nx=16001,
    )

    medium = Medium.white_hole_ramp(
        grid,
        c=C,
        v0=V0,
        v1=V1,
        x0=X0,
        width=width,
    )

    x_h = analytic_white_hole_horizon(
        c=C,
        v0=V0,
        v1=V1,
        x0=X0,
        width=width,
    )

    dv_dx = np.gradient(
        medium.v,
        grid.dx,
        edge_order=2,
    )

    numerical_kappa = abs(
        np.interp(
            x_h,
            grid.x,
            dv_dx,
        )
    )

    analytic_kappa = abs(
        _analytic_dv_dx(
            x_h,
            v1=V1,
            x0=X0,
            width=width,
        )
    )

    assert analytic_kappa == pytest.approx(
        expected_kappa,
        rel=1e-12,
    )

    assert numerical_kappa == pytest.approx(
        analytic_kappa,
        rel=2e-4,
    )


def test_surface_gravity_scales_inverse_with_width() -> None:
    """For fixed v0 and v1, kappa * width must remain constant."""
    widths = np.asarray(
        [
            1.0,
            1.5,
            2.0,
            3.0,
            4.0,
            6.0,
        ]
    )

    kappas = []

    for width in widths:
        x_h = analytic_white_hole_horizon(
            c=C,
            v0=V0,
            v1=V1,
            x0=X0,
            width=width,
        )

        kappa = abs(
            _analytic_dv_dx(
                x_h,
                v1=V1,
                x0=X0,
                width=width,
            )
        )

        kappas.append(kappa)

    kappas = np.asarray(kappas)

    products = (
        widths * kappas
    )

    assert np.allclose(
        products,
        products[0],
        rtol=1e-12,
        atol=1e-12,
    )

    # For the present profile parameters:
    #
    #     kappa = 0.375 / w
    #
    assert products[0] == pytest.approx(
        0.375,
        rel=1e-12,
    )


def test_incident_branch_blueshifts_toward_horizon() -> None:
    """Analytic incident-branch k must increase toward the horizon."""
    grid = Grid(
        x_min=-20.0,
        x_max=20.0,
        nx=4001,
    )

    medium = Medium.white_hole_ramp(
        grid,
        c=C,
        v0=V0,
        v1=V1,
        x0=X0,
        width=W,
    )

    x_h = analytic_white_hole_horizon(
        c=C,
        v0=V0,
        v1=V1,
        x0=X0,
        width=W,
    )

    x_launch = -12.0
    k0 = 5.0

    v_launch = np.interp(
        x_launch,
        grid.x,
        medium.v,
    )

    omega0 = (
        v_launch + C
    ) * k0

    sample_x = np.asarray(
        [
            -10.0,
            -5.0,
            0.0,
            1.0,
            2.0,
        ]
    )

    assert np.all(
        sample_x < x_h
    )

    v_sample = np.interp(
        sample_x,
        grid.x,
        medium.v,
    )

    k_sample = (
        omega0
        / (v_sample + C)
    )

    assert np.all(
        np.diff(k_sample) > 0.0
    )

    assert k_sample[-1] > k_sample[0]


def test_incident_branch_comoving_frequency_equals_c_k() -> None:
    """The incident branch must satisfy omega' = omega - vk = c k."""
    grid = Grid(
        x_min=-20.0,
        x_max=20.0,
        nx=4001,
    )

    medium = Medium.white_hole_ramp(
        grid,
        c=C,
        v0=V0,
        v1=V1,
        x0=X0,
        width=W,
    )

    x_launch = -12.0
    k0 = 5.0

    v_launch = np.interp(
        x_launch,
        grid.x,
        medium.v,
    )

    omega0 = (
        v_launch + C
    ) * k0

    sample_x = np.asarray(
        [
            -10.0,
            -5.0,
            0.0,
            1.0,
            2.0,
        ]
    )

    v_sample = np.interp(
        sample_x,
        grid.x,
        medium.v,
    )

    k_sample = (
        omega0
        / (v_sample + C)
    )

    omega_prime = (
        omega0
        - v_sample * k_sample
    )

    assert np.allclose(
        omega_prime,
        C * k_sample,
        rtol=1e-12,
        atol=1e-12,
    )


def test_characteristic_solver_remains_stable_on_full_ramp() -> None:
    """A packet must not trigger remote numerical growth on the ramp."""
    grid0 = Grid(
        x_min=-25.0,
        x_max=25.0,
        nx=1601,
    )

    medium = Medium.white_hole_ramp(
        grid0,
        c=C,
        v0=V0,
        v1=V1,
        x0=X0,
        width=W,
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

    target_time = 4.0

    sim.run(
        n_steps=round(
            target_time / grid.dt
        )
    )

    assert np.all(
        np.isfinite(
            sim.state.y_curr
        )
    )

    center = packet_center(
        grid.x,
        sim.state.y_curr,
    )

    # The packet should still be on the subsonic left side.
    assert center < -8.0

    # No remote instability should have appeared in the supersonic region.
    remote = grid.x > 8.0

    assert np.max(
        np.abs(
            sim.state.y_curr[remote]
        )
    ) < 1e-5
"""Tests for the Round-2 physical lattice dispersion."""

from __future__ import annotations

import numpy as np
import pytest

from analog_gravity.lattice import (
    brillouin_edge,
    dispersion_residual,
    find_modes,
    group_velocity_comoving,
    group_velocity_lab,
    omega_comoving,
    omega_lab,
)


def test_brillouin_edge_is_pi_over_a() -> None:
    """The first Brillouin zone ends at |k| = pi/a."""
    a = 0.25

    assert brillouin_edge(a) == pytest.approx(
        np.pi / a
    )


@pytest.mark.parametrize(
    "branch",
    [+1, -1],
)
def test_long_wavelength_limit_recovers_continuum(
    branch: int,
) -> None:
    """For |ka| << 1, omega' approaches branch * c * k."""
    c = 1.3
    a = 0.2
    k = np.asarray(
        [
            -0.05,
            -0.02,
            0.02,
            0.05,
        ]
    )

    omega_prime = omega_comoving(
        k,
        c=c,
        lattice_spacing=a,
        branch=branch,
    )

    expected = branch * c * k

    assert np.allclose(
        omega_prime,
        expected,
        rtol=5e-6,
        atol=1e-12,
    )


@pytest.mark.parametrize(
    "branch",
    [+1, -1],
)
def test_group_velocity_is_derivative_of_omega_comoving(
    branch: int,
) -> None:
    """Analytic group velocity must match a finite-difference derivative."""
    c = 1.0
    a = 0.3
    k = 2.1
    dk = 1e-6

    numerical_derivative = (
        omega_comoving(
            k + dk,
            c=c,
            lattice_spacing=a,
            branch=branch,
        )
        - omega_comoving(
            k - dk,
            c=c,
            lattice_spacing=a,
            branch=branch,
        )
    ) / (2.0 * dk)

    analytic = group_velocity_comoving(
        k,
        c=c,
        lattice_spacing=a,
        branch=branch,
    )

    assert float(analytic) == pytest.approx(
        float(numerical_derivative),
        rel=1e-9,
        abs=1e-10,
    )


def test_lab_frequency_is_doppler_shifted_comoving_frequency() -> None:
    """omega = v k + omega' must hold exactly."""
    c = 1.0
    a = 0.25
    v = -0.4
    k = np.asarray(
        [
            -4.0,
            -1.0,
            1.0,
            4.0,
        ]
    )

    omega_prime = omega_comoving(
        k,
        c=c,
        lattice_spacing=a,
        branch=+1,
    )

    omega = omega_lab(
        k,
        v=v,
        c=c,
        lattice_spacing=a,
        branch=+1,
    )

    assert np.allclose(
        omega,
        v * k + omega_prime,
        rtol=0.0,
        atol=1e-14,
    )


def test_lab_group_velocity_is_v_plus_comoving_group_velocity() -> None:
    """The background velocity simply adds to d omega'/dk."""
    c = 1.0
    a = 0.25
    v = -0.35
    k = 3.0

    expected = (
        v
        + group_velocity_comoving(
            k,
            c=c,
            lattice_spacing=a,
            branch=+1,
        )
    )

    actual = group_velocity_lab(
        k,
        v=v,
        c=c,
        lattice_spacing=a,
        branch=+1,
    )

    assert float(actual) == pytest.approx(
        float(expected)
    )


def test_lattice_group_velocity_vanishes_at_brillouin_edge() -> None:
    """Intrinsic group velocity is zero at k = +/- pi/a."""
    c = 1.0
    a = 0.25
    k_edge = brillouin_edge(a)

    vg_plus = group_velocity_comoving(
        k_edge,
        c=c,
        lattice_spacing=a,
        branch=+1,
    )

    vg_minus = group_velocity_comoving(
        -k_edge,
        c=c,
        lattice_spacing=a,
        branch=+1,
    )

    assert float(vg_plus) == pytest.approx(
        0.0,
        abs=1e-14,
    )

    assert float(vg_minus) == pytest.approx(
        0.0,
        abs=1e-14,
    )


def test_branch_solution_satisfies_squared_dispersion_relation() -> None:
    """Both signed branches must satisfy the squared physical relation."""
    c = 1.0
    a = 0.25
    v = -0.6
    k = np.linspace(
        -0.9 * np.pi / a,
        0.9 * np.pi / a,
        101,
    )

    for branch in (+1, -1):
        omega = omega_lab(
            k,
            v=v,
            c=c,
            lattice_spacing=a,
            branch=branch,
        )

        residual = dispersion_residual(
            k,
            omega=omega,
            v=v,
            c=c,
            lattice_spacing=a,
        )

        assert np.allclose(
            residual,
            0.0,
            atol=1e-11,
        )


def test_find_modes_returns_real_roots_that_satisfy_fixed_omega() -> None:
    """Every returned mode must lie on its branch at the requested omega."""
    c = 1.0
    a = 0.25
    v = -0.8
    omega0 = 1.0

    modes = find_modes(
        omega0,
        v=v,
        c=c,
        lattice_spacing=a,
    )

    assert len(modes) >= 1

    for mode in modes:
        reconstructed = omega_lab(
            mode.k,
            v=v,
            c=c,
            lattice_spacing=a,
            branch=mode.branch,
        )

        assert float(reconstructed) == pytest.approx(
            omega0,
            abs=1e-9,
        )

        assert mode.omega_prime == pytest.approx(
            omega0 - v * mode.k,
            abs=1e-12,
        )


def test_invalid_branch_is_rejected() -> None:
    """Only the two signed acoustic branches are allowed."""
    with pytest.raises(
        ValueError,
        match="branch",
    ):
        omega_comoving(
            1.0,
            c=1.0,
            lattice_spacing=0.25,
            branch=0,
        )

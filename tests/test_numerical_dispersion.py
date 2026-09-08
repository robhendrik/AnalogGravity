"""Tests for the intentional numerical-dispersion experiment.

These tests characterize the dispersion introduced by the second-order
upwind stencil used by the characteristic solver.

This is numerical lattice physics, not physical rope dispersion.
"""

from __future__ import annotations

import numpy as np
import pytest


def numerical_k_eff(
    k: np.ndarray | float,
    dx: float,
) -> np.ndarray:
    """Real propagation part of the second-order upwind derivative."""
    theta = np.asarray(k) * dx

    return (
        4.0 * np.sin(theta)
        - np.sin(2.0 * theta)
    ) / (2.0 * dx)


def numerical_group_velocity_factor(
    k: np.ndarray | float,
    dx: float,
) -> np.ndarray:
    """Return vg_num / vg_continuum for the upwind spatial stencil."""
    theta = np.asarray(k) * dx

    return (
        2.0 * np.cos(theta)
        - np.cos(2.0 * theta)
    )


def test_numerical_dispersion_recovers_continuum_at_small_k() -> None:
    """Long wavelengths must converge to the continuum dispersion."""
    dx = 0.02

    k = np.asarray(
        [
            0.1,
            0.2,
            0.5,
        ]
    )

    k_eff = numerical_k_eff(
        k,
        dx,
    )

    relative_error = np.abs(
        (k_eff - k) / k
    )

    # The second-order upwind modified wavenumber satisfies
    #
    #     k_eff = k + (1/3) k^3 dx^2 + O(dx^4),
    #
    # so the relative error is O((k dx)^2).
    expected_leading_error = (
        (k * dx) ** 2 / 3.0
    )

    assert np.allclose(
        relative_error,
        expected_leading_error,
        rtol=5e-3,
        atol=1e-10,
    )


def test_numerical_group_velocity_recovers_continuum() -> None:
    """Long-wavelength group velocity follows the expected small-k limit."""
    dx = 0.02
    k = 0.5

    theta = k * dx

    ratio = numerical_group_velocity_factor(
        k,
        dx,
    )

    # For the second-order upwind stencil,
    #
    #     vg_num / vg_cont
    #       = 2 cos(theta) - cos(2 theta)
    #
    # and for small theta,
    #
    #     = 1 + theta^2 - (7/12) theta^4 + O(theta^6).
    #
    expected = (
        1.0
        + theta**2
        - (7.0 / 12.0) * theta**4
    )

    assert ratio == pytest.approx(
        expected,
        rel=1e-10,
    )


def test_numerical_group_velocity_has_lattice_turning_point() -> None:
    """The stencil must develop an artificial zero group velocity."""
    # Solve analytically:
    #
    #   2 cos(theta) - cos(2 theta) = 0
    #
    # giving
    #
    #   cos(theta) = (1 - sqrt(3)) / 2.
    #
    theta_turn = np.arccos(
        (1.0 - np.sqrt(3.0)) / 2.0
    )

    points_per_wavelength = (
        2.0 * np.pi
        / theta_turn
    )

    assert theta_turn == pytest.approx(
        1.94553,
        rel=1e-4,
    )

    assert points_per_wavelength == pytest.approx(
        3.23,
        rel=0.01,
    )

    ratio = (
        2.0 * np.cos(theta_turn)
        - np.cos(2.0 * theta_turn)
    )

    assert ratio == pytest.approx(
        0.0,
        abs=1e-12,
    )


def test_group_velocity_reverses_beyond_lattice_turning_point() -> None:
    """Shorter numerical wavelengths acquire the wrong propagation direction."""
    theta = 2.2

    ratio = (
        2.0 * np.cos(theta)
        - np.cos(2.0 * theta)
    )

    assert ratio < 0.0
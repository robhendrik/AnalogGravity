"""Controlled stabilized subluminal dispersion for Round 3.

The intrinsic dispersion is

    Omega^2(k) = c^2 k^2 [
        1 - (k/k_d)^2 + gamma (k/k_d)^4
    ].

For gamma > 1/4, Omega^2 is positive for every real k.
"""

from __future__ import annotations

import numpy as np


def dispersion_polynomial(
    k: np.ndarray | float,
    *,
    k_d: float,
    gamma: float,
) -> np.ndarray:
    """Return 1 - q^2 + gamma q^4 with q=k/k_d."""
    if k_d <= 0.0:
        raise ValueError("k_d must be positive")
    if gamma <= 0.25:
        raise ValueError("gamma must be > 0.25 for all-k stability")

    q = np.asarray(k, dtype=float) / k_d
    return 1.0 - q**2 + gamma * q**4


def omega_comoving(
    k: np.ndarray | float,
    *,
    c: float,
    k_d: float,
    gamma: float,
    branch: int = +1,
) -> np.ndarray:
    """Return signed comoving frequency omega'(k)."""
    if c <= 0.0:
        raise ValueError("c must be positive")
    if branch not in (-1, +1):
        raise ValueError("branch must be +1 or -1")

    k_array = np.asarray(k, dtype=float)
    poly = dispersion_polynomial(
        k_array,
        k_d=k_d,
        gamma=gamma,
    )

    return branch * c * k_array * np.sqrt(poly)


def omega_squared(
    k: np.ndarray | float,
    *,
    c: float,
    k_d: float,
    gamma: float,
) -> np.ndarray:
    """Return the positive intrinsic Omega^2(k)."""
    k_array = np.asarray(k, dtype=float)
    poly = dispersion_polynomial(
        k_array,
        k_d=k_d,
        gamma=gamma,
    )
    return c**2 * k_array**2 * poly


def omega_lab(
    k: np.ndarray | float,
    *,
    v: float,
    c: float,
    k_d: float,
    gamma: float,
    branch: int = +1,
) -> np.ndarray:
    """Return lab frequency omega = v k + omega'."""
    k_array = np.asarray(k, dtype=float)
    return v * k_array + omega_comoving(
        k_array,
        c=c,
        k_d=k_d,
        gamma=gamma,
        branch=branch,
    )


def group_velocity_lab(
    k: np.ndarray | float,
    *,
    v: float,
    c: float,
    k_d: float,
    gamma: float,
    branch: int = +1,
) -> np.ndarray:
    """Return d omega / d k in the lab frame."""
    if branch not in (-1, +1):
        raise ValueError("branch must be +1 or -1")

    k_array = np.asarray(k, dtype=float)
    q = k_array / k_d
    poly = dispersion_polynomial(
        k_array,
        k_d=k_d,
        gamma=gamma,
    )

    numerator = 1.0 - 2.0 * q**2 + 3.0 * gamma * q**4

    return (
        v
        + branch
        * c
        * numerator
        / np.sqrt(poly)
    )

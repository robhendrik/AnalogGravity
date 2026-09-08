"""Dispersion relations for the Round-2 physical lattice model.

The physical lattice spacing ``a`` is a model parameter and must not be
confused with the numerical grid spacing ``dx``.

For the nearest-neighbour lattice used in Round 2,

    (omega - v k)^2
        = (4 c^2 / a^2) sin^2(k a / 2).

The two signed acoustic continuations are written

    omega' = omega - v k
           = s (2 c / a) sin(k a / 2),

with ``s = +1`` or ``-1``.

Near k = 0 these reduce to

    omega' ~= s c k,

so ``branch=+1`` is the continuation with positive slope +c through k=0,
and ``branch=-1`` has slope -c.

Note that ``branch`` is therefore a branch label, not a statement that
omega' is positive everywhere. The sign of ``omega_prime`` should be used
when classifying positive- and negative-comoving-frequency modes.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import brentq


@dataclass(frozen=True)
class LatticeMode:
    """One real-k solution at fixed lab-frame frequency."""

    k: float
    branch: int
    omega_prime: float
    group_velocity: float


def _validate_branch(branch: int) -> None:
    """Validate a lattice branch label."""
    if branch not in (-1, +1):
        raise ValueError("branch must be +1 or -1")


def brillouin_edge(lattice_spacing: float) -> float:
    """Return the positive edge pi/a of the first Brillouin zone."""
    if lattice_spacing <= 0.0:
        raise ValueError("lattice_spacing must be positive")

    return np.pi / lattice_spacing


def omega_comoving(
    k: np.ndarray | float,
    *,
    c: float,
    lattice_spacing: float,
    branch: int = +1,
) -> np.ndarray:
    """Return the signed comoving frequency omega' for one lattice branch."""
    _validate_branch(branch)

    if c <= 0.0:
        raise ValueError("c must be positive")

    if lattice_spacing <= 0.0:
        raise ValueError("lattice_spacing must be positive")

    k_array = np.asarray(k, dtype=float)
    a = lattice_spacing

    return (
        branch
        * (2.0 * c / a)
        * np.sin(0.5 * k_array * a)
    )


def omega_lab(
    k: np.ndarray | float,
    *,
    v: float,
    c: float,
    lattice_spacing: float,
    branch: int = +1,
) -> np.ndarray:
    """Return lab-frame frequency omega = v k + omega'."""
    k_array = np.asarray(k, dtype=float)

    return (
        v * k_array
        + omega_comoving(
            k_array,
            c=c,
            lattice_spacing=lattice_spacing,
            branch=branch,
        )
    )


def group_velocity_comoving(
    k: np.ndarray | float,
    *,
    c: float,
    lattice_spacing: float,
    branch: int = +1,
) -> np.ndarray:
    """Return d omega' / d k for one lattice branch."""
    _validate_branch(branch)

    if c <= 0.0:
        raise ValueError("c must be positive")

    if lattice_spacing <= 0.0:
        raise ValueError("lattice_spacing must be positive")

    k_array = np.asarray(k, dtype=float)
    a = lattice_spacing

    return (
        branch
        * c
        * np.cos(0.5 * k_array * a)
    )


def group_velocity_lab(
    k: np.ndarray | float,
    *,
    v: float,
    c: float,
    lattice_spacing: float,
    branch: int = +1,
) -> np.ndarray:
    """Return lab-frame group velocity d omega / d k."""
    return (
        v
        + group_velocity_comoving(
            k,
            c=c,
            lattice_spacing=lattice_spacing,
            branch=branch,
        )
    )


def dispersion_residual(
    k: np.ndarray | float,
    *,
    omega: float,
    v: float,
    c: float,
    lattice_spacing: float,
) -> np.ndarray:
    """Return the squared lattice-dispersion residual.

    A physical root satisfies residual = 0:

        (omega - v k)^2
        - (4 c^2 / a^2) sin^2(k a / 2) = 0.
    """
    k_array = np.asarray(k, dtype=float)
    a = lattice_spacing

    return (
        (omega - v * k_array) ** 2
        - (
            (2.0 * c / a)
            * np.sin(0.5 * k_array * a)
        ) ** 2
    )


def find_modes(
    omega: float,
    *,
    v: float,
    c: float,
    lattice_spacing: float,
    samples: int = 20001,
    root_tolerance: float = 1e-10,
) -> list[LatticeMode]:
    """Find all real modes in the first Brillouin zone for fixed omega.

    Roots are found separately on the two signed acoustic branches. Each
    returned mode includes its comoving frequency and lab-frame group velocity.
    """
    if samples < 101:
        raise ValueError("samples must be at least 101")

    k_edge = brillouin_edge(lattice_spacing)

    k_grid = np.linspace(
        -k_edge,
        +k_edge,
        samples,
    )

    modes: list[LatticeMode] = []

    for branch in (+1, -1):

        def f(k_value: float) -> float:
            return float(
                omega_lab(
                    k_value,
                    v=v,
                    c=c,
                    lattice_spacing=lattice_spacing,
                    branch=branch,
                )
                - omega
            )

        values = np.asarray(
            [
                f(k_value)
                for k_value in k_grid
            ]
        )

        roots: list[float] = []

        for index in range(
            len(k_grid) - 1
        ):
            k_left = k_grid[index]
            k_right = k_grid[index + 1]

            f_left = values[index]
            f_right = values[index + 1]

            if abs(f_left) <= root_tolerance:
                roots.append(
                    float(k_left)
                )

            if f_left * f_right < 0.0:
                roots.append(
                    float(
                        brentq(
                            f,
                            k_left,
                            k_right,
                        )
                    )
                )

        if abs(values[-1]) <= root_tolerance:
            roots.append(
                float(k_grid[-1])
            )

        roots.sort()

        unique_roots: list[float] = []

        for root in roots:
            if (
                not unique_roots
                or abs(
                    root
                    - unique_roots[-1]
                ) > 100.0 * root_tolerance
            ):
                unique_roots.append(root)

        for root in unique_roots:
            omega_prime = float(
                omega
                - v * root
            )

            vg = float(
                group_velocity_lab(
                    root,
                    v=v,
                    c=c,
                    lattice_spacing=lattice_spacing,
                    branch=branch,
                )
            )

            modes.append(
                LatticeMode(
                    k=root,
                    branch=branch,
                    omega_prime=omega_prime,
                    group_velocity=vg,
                )
            )

    modes.sort(
        key=lambda mode: mode.k
    )

    return modes
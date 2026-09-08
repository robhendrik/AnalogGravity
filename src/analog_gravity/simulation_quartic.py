"""Pseudo-spectral time-domain solver for Round-3 dispersion.

The variables are

    y(x,t)
    p(x,t) = (partial_t + v partial_x) y.

They obey

    y_t = p - v y_x
    p_t = -v p_x - Omega^2(-i partial_x) y,

with

    Omega^2(k)
        = c^2 k^2 [
            1 - (k/k_d)^2 + gamma (k/k_d)^4
        ].

This module is deliberately separate from the validated Round-1 solver and
the exploratory Round-2 lattice solver.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .grid import Grid
from .medium import Medium
from .quartic import omega_comoving, omega_squared


@dataclass
class QuarticState:
    """State of the stabilized-dispersion simulation."""

    t: float
    y: np.ndarray
    p: np.ndarray


class QuarticSimulation:
    """RK4 pseudo-spectral evolution for stabilized dispersion."""

    def __init__(
        self,
        grid: Grid,
        medium: Medium,
        *,
        c: float,
        k_d: float,
        gamma: float,
        dt: float,
        y0: np.ndarray,
        p0: np.ndarray,
    ) -> None:
        if c <= 0.0:
            raise ValueError("c must be positive")
        if k_d <= 0.0:
            raise ValueError("k_d must be positive")
        if gamma <= 0.25:
            raise ValueError("gamma must be > 0.25")
        if dt <= 0.0:
            raise ValueError("dt must be positive")

        y0 = np.asarray(y0, dtype=float)
        p0 = np.asarray(p0, dtype=float)

        if y0.shape != grid.x.shape:
            raise ValueError("y0 must have shape grid.x.shape")
        if p0.shape != grid.x.shape:
            raise ValueError("p0 must have shape grid.x.shape")

        self.grid = grid
        self.medium = medium
        self.c = float(c)
        self.k_d = float(k_d)
        self.gamma = float(gamma)
        self.dt = float(dt)

        self._k = 2.0 * np.pi * np.fft.fftfreq(
            grid.nx,
            d=grid.dx,
        )

        self._omega_squared = omega_squared(
            self._k,
            c=self.c,
            k_d=self.k_d,
            gamma=self.gamma,
        )

        self.state = QuarticState(
            t=0.0,
            y=y0.copy(),
            p=p0.copy(),
        )

    @classmethod
    def from_branch_initial_condition(
        cls,
        grid: Grid,
        medium: Medium,
        *,
        c: float,
        k_d: float,
        gamma: float,
        y0: np.ndarray,
        branch: int = +1,
        dt: float | None = None,
        safety: float = 0.35,
    ) -> "QuarticSimulation":
        """Construct an approximately pure signed intrinsic branch."""
        if branch not in (-1, +1):
            raise ValueError("branch must be +1 or -1")

        if dt is None:
            dt = cls.recommended_dt(
                grid,
                medium,
                c=c,
                k_d=k_d,
                gamma=gamma,
                safety=safety,
            )

        k = 2.0 * np.pi * np.fft.fftfreq(
            grid.nx,
            d=grid.dx,
        )

        y_hat = np.fft.fft(
            np.asarray(y0, dtype=float)
        )

        omega_prime = omega_comoving(
            k,
            c=c,
            k_d=k_d,
            gamma=gamma,
            branch=branch,
        )

        p_hat = -1j * omega_prime * y_hat
        p0 = np.fft.ifft(p_hat).real

        return cls(
            grid,
            medium,
            c=c,
            k_d=k_d,
            gamma=gamma,
            dt=dt,
            y0=np.asarray(y0, dtype=float),
            p0=p0,
        )

    @staticmethod
    def recommended_dt(
        grid: Grid,
        medium: Medium,
        *,
        c: float,
        k_d: float,
        gamma: float,
        safety: float = 0.35,
    ) -> float:
        """Return a conservative RK4 timestep from the largest grid mode.

        The sextic high-k stabilizer makes the PDE stiff because Omega grows
        approximately as |k|^3.  For explicit RK4 we therefore estimate the
        largest angular frequency present on the numerical mesh and require

            dt * omega_max << RK4 imaginary-axis stability limit.

        ``safety`` is deliberately conservative.
        """
        if safety <= 0.0:
            raise ValueError("safety must be positive")

        k = 2.0 * np.pi * np.fft.fftfreq(
            grid.nx,
            d=grid.dx,
        )

        omega_intrinsic = np.sqrt(
            omega_squared(
                k,
                c=c,
                k_d=k_d,
                gamma=gamma,
            )
        )

        omega_advective = (
            np.max(np.abs(medium.v))
            * np.abs(k)
        )

        omega_max = float(
            np.max(
                omega_intrinsic
                + omega_advective
            )
        )

        if omega_max <= 0.0:
            raise ValueError("could not determine positive omega_max")

        return safety / omega_max

    def _dx(
        self,
        field: np.ndarray,
    ) -> np.ndarray:
        field_hat = np.fft.fft(field)
        return np.fft.ifft(
            1j * self._k * field_hat
        ).real

    def _omega_squared_operator(
        self,
        field: np.ndarray,
    ) -> np.ndarray:
        field_hat = np.fft.fft(field)
        return np.fft.ifft(
            self._omega_squared * field_hat
        ).real

    def _rhs(
        self,
        y: np.ndarray,
        p: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        y_x = self._dx(y)
        p_x = self._dx(p)

        y_t = p - self.medium.v * y_x
        p_t = (
            -self.medium.v * p_x
            - self._omega_squared_operator(y)
        )

        return y_t, p_t

    def step(self) -> None:
        """Advance by one classical RK4 step."""
        y = self.state.y
        p = self.state.p
        dt = self.dt

        k1_y, k1_p = self._rhs(y, p)
        k2_y, k2_p = self._rhs(
            y + 0.5 * dt * k1_y,
            p + 0.5 * dt * k1_p,
        )
        k3_y, k3_p = self._rhs(
            y + 0.5 * dt * k2_y,
            p + 0.5 * dt * k2_p,
        )
        k4_y, k4_p = self._rhs(
            y + dt * k3_y,
            p + dt * k3_p,
        )

        y_new = (
            y
            + dt
            * (
                k1_y
                + 2.0 * k2_y
                + 2.0 * k3_y
                + k4_y
            )
            / 6.0
        )

        p_new = (
            p
            + dt
            * (
                k1_p
                + 2.0 * k2_p
                + 2.0 * k3_p
                + k4_p
            )
            / 6.0
        )

        self.state = QuarticState(
            t=self.state.t + dt,
            y=y_new,
            p=p_new,
        )

    def run(
        self,
        *,
        n_steps: int,
    ) -> None:
        """Advance by n_steps."""
        if n_steps < 0:
            raise ValueError("n_steps must be non-negative")

        for _ in range(n_steps):
            self.step()

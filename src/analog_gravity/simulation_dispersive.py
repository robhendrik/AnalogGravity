"""Pseudo-spectral solver for the Round-2 lattice-inspired dispersion.

This module is separate from ``simulation.py`` so the validated Round-1
continuum solver remains untouched.

The dynamical variables are

    y(x,t)
    p(x,t) = (partial_t + v partial_x) y.

They obey

    y_t = p - v y_x
    p_t = -v p_x - Omega^2(-i partial_x) y,

with physical lattice dispersion

    Omega^2(k)
        = (4 c^2 / a^2) sin^2(k a / 2).

The physical lattice spacing ``a`` is independent of the numerical mesh
spacing ``dx``.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .grid import Grid
from .medium import Medium


@dataclass
class DispersiveState:
    """State of the Round-2 dispersive solver."""

    t: float
    y: np.ndarray
    p: np.ndarray


class DispersiveSimulation:
    """RK4 pseudo-spectral evolution with physical lattice dispersion."""

    def __init__(
        self,
        grid: Grid,
        medium: Medium,
        *,
        c: float,
        lattice_spacing: float,
        dt: float,
        y0: np.ndarray,
        p0: np.ndarray,
        enforce_brillouin_zone: bool = True,
    ) -> None:
        if c <= 0.0:
            raise ValueError("c must be positive")
        if lattice_spacing <= 0.0:
            raise ValueError("lattice_spacing must be positive")
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
        self.lattice_spacing = float(lattice_spacing)
        self.dt = float(dt)
        self.enforce_brillouin_zone = bool(enforce_brillouin_zone)

        self._k = 2.0 * np.pi * np.fft.fftfreq(grid.nx, d=grid.dx)
        self._k_edge = np.pi / self.lattice_spacing
        self._physical_band = np.abs(self._k) <= self._k_edge

        self._omega_squared = (
            (2.0 * self.c / self.lattice_spacing)
            * np.sin(0.5 * self._k * self.lattice_spacing)
        ) ** 2

        if self.enforce_brillouin_zone:
            y0 = self._project(y0)
            p0 = self._project(p0)

        self.state = DispersiveState(
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
        lattice_spacing: float,
        y0: np.ndarray,
        branch: int = +1,
        dt: float | None = None,
        cfl: float = 0.25,
        enforce_brillouin_zone: bool = True,
    ) -> "DispersiveSimulation":
        """Create a pure signed-acoustic-branch initial condition."""
        if branch not in (-1, +1):
            raise ValueError("branch must be +1 or -1")

        if dt is None:
            dt = cls.recommended_dt(
                grid,
                medium,
                c=c,
                lattice_spacing=lattice_spacing,
                cfl=cfl,
            )

        k = 2.0 * np.pi * np.fft.fftfreq(grid.nx, d=grid.dx)

        omega_prime = (
            branch
            * (2.0 * c / lattice_spacing)
            * np.sin(0.5 * k * lattice_spacing)
        )

        physical_band = np.abs(k) <= np.pi / lattice_spacing

        y_hat = np.fft.fft(np.asarray(y0, dtype=float))

        if enforce_brillouin_zone:
            y_hat = np.where(physical_band, y_hat, 0.0)

        p_hat = -1j * omega_prime * y_hat

        if enforce_brillouin_zone:
            p_hat = np.where(physical_band, p_hat, 0.0)

        y_filtered = np.fft.ifft(y_hat).real
        p0 = np.fft.ifft(p_hat).real

        return cls(
            grid,
            medium,
            c=c,
            lattice_spacing=lattice_spacing,
            dt=dt,
            y0=y_filtered,
            p0=p0,
            enforce_brillouin_zone=enforce_brillouin_zone,
        )

    @staticmethod
    def recommended_dt(
        grid: Grid,
        medium: Medium,
        *,
        c: float,
        lattice_spacing: float,
        cfl: float = 0.25,
    ) -> float:
        """Return a conservative RK4 timestep."""
        if cfl <= 0.0:
            raise ValueError("cfl must be positive")

        max_speed = float(np.max(np.abs(medium.v)) + c)
        return cfl * grid.dx / max_speed

    def _project(self, field: np.ndarray) -> np.ndarray:
        """Project a real field onto the first physical Brillouin zone."""
        field_hat = np.fft.fft(field)
        field_hat = np.where(self._physical_band, field_hat, 0.0)
        return np.fft.ifft(field_hat).real

    def _dx(self, field: np.ndarray) -> np.ndarray:
        """Periodic spectral first derivative."""
        field_hat = np.fft.fft(field)

        if self.enforce_brillouin_zone:
            field_hat = np.where(self._physical_band, field_hat, 0.0)

        derivative_hat = 1j * self._k * field_hat
        return np.fft.ifft(derivative_hat).real

    def _omega_squared_operator(self, field: np.ndarray) -> np.ndarray:
        """Apply the physical lattice Omega^2 operator."""
        field_hat = np.fft.fft(field)

        if self.enforce_brillouin_zone:
            field_hat = np.where(self._physical_band, field_hat, 0.0)

        result_hat = self._omega_squared * field_hat

        if self.enforce_brillouin_zone:
            result_hat = np.where(self._physical_band, result_hat, 0.0)

        return np.fft.ifft(result_hat).real

    def _rhs(
        self,
        y: np.ndarray,
        p: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Return y_t and p_t."""
        y_x = self._dx(y)
        p_x = self._dx(p)
        omega_squared_y = self._omega_squared_operator(y)

        y_t = p - self.medium.v * y_x
        p_t = -self.medium.v * p_x - omega_squared_y

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

        y_new = y + dt * (
            k1_y + 2.0 * k2_y + 2.0 * k3_y + k4_y
        ) / 6.0
        p_new = p + dt * (
            k1_p + 2.0 * k2_p + 2.0 * k3_p + k4_p
        ) / 6.0

        if self.enforce_brillouin_zone:
            y_new = self._project(y_new)
            p_new = self._project(p_new)

        self.state = DispersiveState(
            t=self.state.t + dt,
            y=y_new,
            p=p_new,
        )

    def run(self, *, n_steps: int) -> None:
        """Advance by ``n_steps``."""
        if n_steps < 0:
            raise ValueError("n_steps must be non-negative")

        for _ in range(n_steps):
            self.step()

"""Stable characteristic evolution of the nondispersive moving-rope equation."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray

from .grid import Grid
from .medium import Medium
from .state import WaveState


def _gradient(
    values: NDArray[np.float64],
    dx: float,
) -> NDArray[np.float64]:
    """Return a second-order numerical first derivative."""
    return np.gradient(values, dx, edge_order=2)


def _upwind_derivative(
    values: NDArray[np.float64],
    speed: NDArray[np.float64],
    dx: float,
) -> NDArray[np.float64]:
    """Second-order upwind derivative.

    The upwind direction is chosen independently at every grid point from
    the sign of the local characteristic speed.

    Zero-valued exterior ghost cells are used. Validation wave packets should
    remain well away from the physical boundaries.
    """
    f = np.asarray(values, dtype=float)
    a = np.asarray(speed, dtype=float)

    if f.shape != a.shape:
        raise ValueError("values and speed must have the same shape")

    fm1 = np.empty_like(f)
    fm2 = np.empty_like(f)

    fp1 = np.empty_like(f)
    fp2 = np.empty_like(f)

    # Left-shifted values.
    fm1[0] = 0.0
    fm1[1:] = f[:-1]

    fm2[:2] = 0.0
    fm2[2:] = f[:-2]

    # Right-shifted values.
    fp1[-1] = 0.0
    fp1[:-1] = f[1:]

    fp2[-2:] = 0.0
    fp2[:-2] = f[2:]

    backward = (
        3.0 * f
        - 4.0 * fm1
        + fm2
    ) / (2.0 * dx)

    forward = (
        -3.0 * f
        + 4.0 * fp1
        - fp2
    ) / (2.0 * dx)

    return np.where(
        a >= 0.0,
        backward,
        forward,
    )


@dataclass(slots=True)
class Simulation:
    """Characteristic solver for the nondispersive moving-rope equation.

    The governing equation is

        (d/dt + v d/dx)^2 y = c^2 y_xx.

    Define

        q = y_x
        p = y_t + v y_x

    and characteristic fields

        r_plus  = p + c q
        r_minus = p - c q.

    Their equations are

        r_plus_t + (v-c) r_plus_x
            = -(v'/2) (r_plus-r_minus)

        r_minus_t + (v+c) r_minus_x
            = +(v'/2) (r_plus-r_minus).

    Thus the two characteristic speeds are exactly

        v-c
        v+c.

    Spatial advection is treated with second-order upwinding and time
    evolution with third-order SSP Runge-Kutta.

    The public Simulation API remains the same as in the earlier leapfrog
    implementation.
    """

    grid: Grid
    medium: Medium
    state: WaveState
    store_every: int = 1

    history: list[NDArray[np.float64]] = field(
        default_factory=list
    )
    history_times: list[float] = field(
        default_factory=list
    )

    _r_plus: NDArray[np.float64] = field(
        init=False,
        repr=False,
    )
    _r_minus: NDArray[np.float64] = field(
        init=False,
        repr=False,
    )
    _dv_dx: NDArray[np.float64] = field(
        init=False,
        repr=False,
    )

    _steps: int = field(
        default=0,
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        if self.grid.dt is None:
            raise ValueError(
                "grid.dt must be set before constructing Simulation"
            )

        if self.medium.v.size != self.grid.nx:
            raise ValueError(
                "grid and medium sizes do not match"
            )

        if self.state.y_curr.size != self.grid.nx:
            raise ValueError(
                "grid and state sizes do not match"
            )

        if self.store_every < 1:
            raise ValueError(
                "store_every must be >= 1"
            )

        self._r_plus = np.zeros(
            self.grid.nx,
            dtype=float,
        )

        self._r_minus = np.zeros(
            self.grid.nx,
            dtype=float,
        )

        self._dv_dx = self.medium.dv_dx(
            self.grid
        )

        self.history.append(
            self.state.y_curr.copy()
        )

        self.history_times.append(
            float(self.state.t)
        )

    @classmethod
    def from_initial_conditions(
        cls,
        grid: Grid,
        medium: Medium,
        y0: NDArray[np.float64],
        ydot0: NDArray[np.float64],
        *,
        store_every: int = 1,
    ) -> "Simulation":
        """Construct a simulation from displacement and velocity.

        The initial characteristic fields are obtained from

            q = y_x
            p = ydot + v q.
        """
        if grid.dt is None:
            raise ValueError(
                "grid.dt must be set before initialization"
            )

        y0 = np.asarray(
            y0,
            dtype=float,
        ).copy()

        ydot0 = np.asarray(
            ydot0,
            dtype=float,
        ).copy()

        if y0.shape != (grid.nx,):
            raise ValueError(
                "initial-condition arrays must have shape (grid.nx,)"
            )

        if ydot0.shape != (grid.nx,):
            raise ValueError(
                "initial-condition arrays must have shape (grid.nx,)"
            )

        if not np.all(np.isfinite(y0)):
            raise ValueError(
                "initial conditions must contain only finite values"
            )

        if not np.all(np.isfinite(ydot0)):
            raise ValueError(
                "initial conditions must contain only finite values"
            )

        # Fixed field values at the domain edges.
        y0[[0, -1]] = 0.0
        ydot0[[0, -1]] = 0.0

        q0 = _gradient(
            y0,
            grid.dx,
        )

        p0 = (
            ydot0
            + medium.v * q0
        )

        r_plus0 = (
            p0
            + medium.c * q0
        )

        r_minus0 = (
            p0
            - medium.c * q0
        )

        # y_prev is retained for compatibility with WaveState and the
        # existing public API. The characteristic solver does not use it
        # for the numerical update.
        y_prev = (
            y0
            - grid.dt * ydot0
        )

        y_prev[[0, -1]] = 0.0

        state = WaveState(
            y_curr=y0,
            y_prev=y_prev,
            t=0.0,
        )

        simulation = cls(
            grid=grid,
            medium=medium,
            state=state,
            store_every=store_every,
        )

        simulation._r_plus = r_plus0
        simulation._r_minus = r_minus0

        return simulation

    def _rhs(
        self,
        y: NDArray[np.float64],
        r_plus: NDArray[np.float64],
        r_minus: NDArray[np.float64],
    ) -> tuple[
        NDArray[np.float64],
        NDArray[np.float64],
        NDArray[np.float64],
    ]:
        """Evaluate the semi-discrete evolution equations."""
        c = self.medium.c
        v = self.medium.v
        vp = self._dv_dx

        speed_plus = v - c
        speed_minus = v + c

        dr_plus_dx = _upwind_derivative(
            r_plus,
            speed_plus,
            self.grid.dx,
        )

        dr_minus_dx = _upwind_derivative(
            r_minus,
            speed_minus,
            self.grid.dx,
        )

        coupling = (
            0.5
            * vp
            * (r_plus - r_minus)
        )

        r_plus_t = (
            -speed_plus * dr_plus_dx
            - coupling
        )

        r_minus_t = (
            -speed_minus * dr_minus_dx
            + coupling
        )

        # Recover p and q.
        p = 0.5 * (
            r_plus
            + r_minus
        )

        q = (
            r_plus
            - r_minus
        ) / (2.0 * c)

        # Since p = y_t + v q:
        y_t = (
            p
            - v * q
        )

        y_t[[0, -1]] = 0.0

        return (
            y_t,
            r_plus_t,
            r_minus_t,
        )

    def _enforce_boundaries(
        self,
        y: NDArray[np.float64],
        r_plus: NDArray[np.float64],
        r_minus: NDArray[np.float64],
    ) -> tuple[
        NDArray[np.float64],
        NDArray[np.float64],
        NDArray[np.float64],
    ]:
        """Apply simple zero-inflow characteristic boundary conditions."""
        y = y.copy()
        r_plus = r_plus.copy()
        r_minus = r_minus.copy()

        y[[0, -1]] = 0.0

        speed_plus = (
            self.medium.v
            - self.medium.c
        )

        speed_minus = (
            self.medium.v
            + self.medium.c
        )

        # At x_min, positive velocity means information enters the domain.
        if speed_plus[0] > 0.0:
            r_plus[0] = 0.0

        if speed_minus[0] > 0.0:
            r_minus[0] = 0.0

        # At x_max, negative velocity means information enters the domain.
        if speed_plus[-1] < 0.0:
            r_plus[-1] = 0.0

        if speed_minus[-1] < 0.0:
            r_minus[-1] = 0.0

        return (
            y,
            r_plus,
            r_minus,
        )

    def step(self) -> WaveState:
        """Advance the solution by one SSP-RK3 time step."""
        dt = self.grid.dt

        assert dt is not None

        y0 = self.state.y_curr
        rp0 = self._r_plus
        rm0 = self._r_minus

        # --------------------------------------------------------
        # RK stage 1
        # --------------------------------------------------------

        y_t, rp_t, rm_t = self._rhs(
            y0,
            rp0,
            rm0,
        )

        y1 = y0 + dt * y_t
        rp1 = rp0 + dt * rp_t
        rm1 = rm0 + dt * rm_t

        y1, rp1, rm1 = self._enforce_boundaries(
            y1,
            rp1,
            rm1,
        )

        # --------------------------------------------------------
        # RK stage 2
        # --------------------------------------------------------

        y_t, rp_t, rm_t = self._rhs(
            y1,
            rp1,
            rm1,
        )

        y2 = (
            0.75 * y0
            + 0.25 * (
                y1
                + dt * y_t
            )
        )

        rp2 = (
            0.75 * rp0
            + 0.25 * (
                rp1
                + dt * rp_t
            )
        )

        rm2 = (
            0.75 * rm0
            + 0.25 * (
                rm1
                + dt * rm_t
            )
        )

        y2, rp2, rm2 = self._enforce_boundaries(
            y2,
            rp2,
            rm2,
        )

        # --------------------------------------------------------
        # RK stage 3
        # --------------------------------------------------------

        y_t, rp_t, rm_t = self._rhs(
            y2,
            rp2,
            rm2,
        )

        y_next = (
            (1.0 / 3.0) * y0
            + (2.0 / 3.0) * (
                y2
                + dt * y_t
            )
        )

        rp_next = (
            (1.0 / 3.0) * rp0
            + (2.0 / 3.0) * (
                rp2
                + dt * rp_t
            )
        )

        rm_next = (
            (1.0 / 3.0) * rm0
            + (2.0 / 3.0) * (
                rm2
                + dt * rm_t
            )
        )

        y_next, rp_next, rm_next = self._enforce_boundaries(
            y_next,
            rp_next,
            rm_next,
        )

        # --------------------------------------------------------
        # Commit state
        # --------------------------------------------------------

        self.state.y_prev = (
            self.state.y_curr.copy()
        )

        self.state.y_curr = y_next
        self.state.t += dt

        self._r_plus = rp_next
        self._r_minus = rm_next

        self._steps += 1

        if (
            self._steps
            % self.store_every
            == 0
        ):
            self.history.append(
                y_next.copy()
            )

            self.history_times.append(
                float(self.state.t)
            )

        return self.state

    def run(
        self,
        *,
        n_steps: int,
    ) -> WaveState:
        """Advance the simulation by ``n_steps``."""
        if n_steps < 0:
            raise ValueError(
                "n_steps must be non-negative"
            )

        for _ in range(n_steps):
            self.step()

        return self.state

    @property
    def history_array(
        self,
    ) -> NDArray[np.float64]:
        """Return stored snapshots as ``(n_snapshots, nx)``."""
        return np.asarray(
            self.history,
            dtype=float,
        )
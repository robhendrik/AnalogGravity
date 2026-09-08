import numpy as np
import pytest

from analog_gravity import Grid, Medium, Simulation


def _gaussian_and_derivative(x: np.ndarray, center: float, sigma: float):
    y = np.exp(-0.5 * ((x - center) / sigma) ** 2)
    y_x = -(x - center) / sigma**2 * y
    return y, y_x


def _centroid(x: np.ndarray, y: np.ndarray) -> float:
    weight = y * y
    return float(np.sum(x * weight) / np.sum(weight))


def test_step1_zero_initial_velocity_splits_symmetrically_at_plus_minus_c() -> None:
    grid0 = Grid(-12.0, 12.0, 1201)
    medium = Medium.uniform(grid0, c=1.0, v_const=0.0)
    grid = grid0.with_dt(medium.recommended_dt(grid0, cfl=0.45))
    y0, _ = _gaussian_and_derivative(grid.x, center=0.0, sigma=0.55)
    sim = Simulation.from_initial_conditions(grid, medium, y0, np.zeros_like(y0))

    target_t = 2.0
    n_steps = round(target_t / grid.dt)
    sim.run(n_steps=n_steps)
    t = sim.state.t
    y = sim.state.y_curr

    left = grid.x < 0.0
    right = grid.x > 0.0
    x_left = grid.x[left][np.argmax(np.abs(y[left]))]
    x_right = grid.x[right][np.argmax(np.abs(y[right]))]

    assert x_left == pytest.approx(-medium.c * t, abs=4.0 * grid.dx)
    assert x_right == pytest.approx(+medium.c * t, abs=4.0 * grid.dx)
    assert np.max(np.abs(y[left])) == pytest.approx(np.max(np.abs(y[right])), rel=3e-3)


def test_step2_uniform_flow_packet_moves_at_v_plus_c() -> None:
    grid0 = Grid(-20.0, 20.0, 2001)
    medium = Medium.uniform(grid0, c=1.0, v_const=-0.3)
    grid = grid0.with_dt(medium.recommended_dt(grid0, cfl=0.35))

    x0 = -7.0
    sigma = 0.8
    y0, y_x = _gaussian_and_derivative(grid.x, center=x0, sigma=sigma)
    expected_speed = -0.3 + 1.0
    ydot0 = -expected_speed * y_x

    sim = Simulation.from_initial_conditions(grid, medium, y0, ydot0)
    initial_centroid = _centroid(grid.x, sim.state.y_curr)
    target_t = 2.5
    sim.run(n_steps=round(target_t / grid.dt))
    final_centroid = _centroid(grid.x, sim.state.y_curr)

    measured_speed = (final_centroid - initial_centroid) / sim.state.t
    assert measured_speed == pytest.approx(expected_speed, abs=0.02)


def test_no_flow_solution_remains_bounded_before_boundaries_are_reached() -> None:
    grid0 = Grid(-10.0, 10.0, 801)
    medium = Medium.uniform(grid0, c=1.0, v_const=0.0)
    grid = grid0.with_dt(medium.recommended_dt(grid0, cfl=0.5))
    y0, _ = _gaussian_and_derivative(grid.x, center=0.0, sigma=0.7)
    sim = Simulation.from_initial_conditions(grid, medium, y0, np.zeros_like(y0))
    sim.run(n_steps=200)
    assert np.max(np.abs(sim.state.y_curr)) <= 1.02 * np.max(np.abs(y0))

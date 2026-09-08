import numpy as np
import pytest

from analog_gravity import Grid, Medium, analytic_white_hole_horizon


def test_white_hole_ramp_has_expected_asymptotes() -> None:
    grid = Grid(-20.0, 20.0, 4001)
    medium = Medium.white_hole_ramp(
        grid, c=1.0, v0=0.4, v1=1.0, x0=1.5, width=1.0
    )
    assert medium.v[0] == pytest.approx(-0.4, abs=1e-12)
    assert medium.v[-1] == pytest.approx(-1.4, abs=1e-12)


def test_numerical_horizon_matches_analytic_tanh_root() -> None:
    grid = Grid(-8.0, 8.0, 8001)
    params = dict(c=1.0, v0=0.4, v1=1.0, x0=0.7, width=1.3)
    medium = Medium.white_hole_ramp(grid, **params)
    x_num = medium.numerical_horizon_position(grid)
    x_exact = analytic_white_hole_horizon(**params)
    assert x_num == pytest.approx(x_exact, abs=2.0 * grid.dx)


def test_horizon_requires_subsonic_to_supersonic_transition() -> None:
    with pytest.raises(ValueError):
        analytic_white_hole_horizon(c=1.0, v0=0.2, v1=0.3, x0=0.0, width=1.0)

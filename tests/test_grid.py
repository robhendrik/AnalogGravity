import numpy as np
import pytest

from analog_gravity import Grid, Medium


def test_grid_includes_endpoints_and_has_expected_spacing() -> None:
    grid = Grid(-2.0, 3.0, 101)
    assert grid.x[0] == pytest.approx(-2.0)
    assert grid.x[-1] == pytest.approx(3.0)
    assert grid.dx == pytest.approx(0.05)
    assert np.allclose(np.diff(grid.x), grid.dx)


def test_recommended_dt_uses_fastest_characteristic_speed() -> None:
    grid = Grid(0.0, 10.0, 101)
    medium = Medium.uniform(grid, c=2.0, v_const=-0.5)
    dt = medium.recommended_dt(grid, cfl=0.4)
    assert dt == pytest.approx(0.4 * grid.dx / 2.5)

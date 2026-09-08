import numpy as np
import pytest

from analog_gravity import (
    Grid,
    Medium,
    expected_group_velocity,
    measure_group_velocity,
    packet_center,
)


def test_packet_center_finds_center_of_gaussian_carrier() -> None:
    grid = Grid(-20.0, 20.0, 2001)

    expected_center = 3.25
    width = 1.2
    k0 = 6.0

    xi = grid.x - expected_center
    y = np.exp(-0.5 * (xi / width) ** 2) * np.cos(k0 * xi)

    measured_center = packet_center(grid.x, y)

    assert measured_center == pytest.approx(expected_center, abs=0.02)


def test_measure_group_velocity_from_linear_trajectory() -> None:
    times = np.linspace(0.0, 4.0, 21)
    expected_velocity = 0.73
    centers = -2.0 + expected_velocity * times

    measured_velocity = measure_group_velocity(times, centers)

    assert measured_velocity == pytest.approx(expected_velocity)


def test_expected_group_velocity_against_flow_branch() -> None:
    grid = Grid(-10.0, 10.0, 101)
    medium = Medium.uniform(grid, c=1.0, v_const=-0.3)

    velocity = expected_group_velocity(
        medium,
        branch="against_flow",
    )

    assert velocity == pytest.approx(0.7)


def test_expected_group_velocity_with_flow_branch() -> None:
    grid = Grid(-10.0, 10.0, 101)
    medium = Medium.uniform(grid, c=1.0, v_const=-0.3)

    velocity = expected_group_velocity(
        medium,
        branch="with_flow",
    )

    assert velocity == pytest.approx(-1.3)


def test_expected_group_velocity_rejects_nonuniform_medium() -> None:
    grid = Grid(-10.0, 10.0, 101)

    medium = Medium(
        c=1.0,
        v=np.linspace(-0.2, -0.4, grid.nx),
    )

    with pytest.raises(ValueError, match="uniform flow"):
        expected_group_velocity(
            medium,
            branch="against_flow",
        )
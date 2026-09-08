import numpy as np
import pytest

from analog_gravity import (
    Grid,
    Medium,
    Simulation,
    expected_group_velocity,
    make_wavepacket,
    measure_group_velocity,
    track_packet_centers,
)


@pytest.mark.parametrize(
    ("v_const", "branch"),
    [
        (-0.30, "against_flow"),
        (+0.20, "against_flow"),
        (-0.20, "with_flow"),
    ],
)
def test_uniform_flow_packet_has_expected_group_velocity(
    v_const: float,
    branch: str,
) -> None:
    """Step 2: packet velocity must equal the analytic characteristic speed."""

    grid0 = Grid(
        x_min=-30.0,
        x_max=30.0,
        nx=2401,
    )

    medium = Medium.uniform(
        grid0,
        c=1.0,
        v_const=v_const,
    )

    grid = grid0.with_dt(
        medium.recommended_dt(
            grid0,
            cfl=0.35,
        )
    )

    y0, ydot0 = make_wavepacket(
        grid,
        medium,
        x_center=-8.0 if branch == "against_flow" else 8.0,
        width=1.4,
        k0=5.0,
        branch=branch,
    )

    sim = Simulation.from_initial_conditions(
        grid,
        medium,
        y0,
        ydot0,
        store_every=20,
    )

    target_time = 3.0
    n_steps = round(target_time / grid.dt)

    sim.run(n_steps=n_steps)

    centers = track_packet_centers(
        grid,
        sim.history,
    )

    measured_velocity = measure_group_velocity(
        np.asarray(sim.history_times),
        centers,
    )

    analytic_velocity = expected_group_velocity(
        medium,
        branch=branch,
    )

    assert measured_velocity == pytest.approx(
        analytic_velocity,
        abs=0.025,
    )


def test_step2_against_flow_packet_moves_right_in_leftward_subsonic_flow() -> None:
    """The white-hole incident branch must still move right while |v| < c."""

    grid0 = Grid(-25.0, 25.0, 2001)

    medium = Medium.uniform(
        grid0,
        c=1.0,
        v_const=-0.4,
    )

    grid = grid0.with_dt(
        medium.recommended_dt(
            grid0,
            cfl=0.35,
        )
    )

    y0, ydot0 = make_wavepacket(
        grid,
        medium,
        x_center=-7.0,
        width=1.2,
        k0=5.0,
        branch="against_flow",
    )

    sim = Simulation.from_initial_conditions(
        grid,
        medium,
        y0,
        ydot0,
        store_every=20,
    )

    sim.run(
        n_steps=round(2.5 / grid.dt),
    )

    centers = track_packet_centers(
        grid,
        sim.history,
    )

    assert centers[-1] > centers[0]
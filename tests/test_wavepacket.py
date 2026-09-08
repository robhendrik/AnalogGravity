import numpy as np

from analog_gravity import Grid, Medium, make_wavepacket


def test_uniform_medium_wavepacket_obeys_selected_branch_relation() -> None:
    base_grid = Grid(-20.0, 20.0, 4001)
    medium = Medium.uniform(base_grid, c=1.2, v_const=-0.25)
    y0, ydot0 = make_wavepacket(
        base_grid,
        medium,
        x_center=-4.0,
        width=2.0,
        k0=3.0,
        branch="against_flow",
    )
    y_x = np.gradient(y0, base_grid.dx, edge_order=2)
    expected = -(medium.v + medium.c) * y_x
    # Ignore exponentially small tails where relative finite-difference error is noisy.
    mask = np.abs(y0) > 1e-5
    assert np.allclose(ydot0[mask], expected[mask], atol=1e-12, rtol=1e-12)

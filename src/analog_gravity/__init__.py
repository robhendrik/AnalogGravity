"""Numerical experiments for the moving-rope analogue horizon."""

from .diagnostics import (
    expected_group_velocity,
    measure_group_velocity,
    packet_center,
    track_packet_centers,
)
from .grid import Grid
from .medium import Medium, analytic_white_hole_horizon
from .simulation import Simulation
from .state import WaveState
from .wavepacket import Branch, make_wavepacket

__all__ = [
    "Branch",
    "Grid",
    "Medium",
    "Simulation",
    "WaveState",
    "analytic_white_hole_horizon",
    "expected_group_velocity",
    "make_wavepacket",
    "measure_group_velocity",
    "packet_center",
    "track_packet_centers",
]
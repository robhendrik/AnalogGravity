"""
figure_1_black_white_hole_horizons.py

Figure 1 — Black-hole and white-hole horizons.

Stylized river analogy:
- Left: black-hole analogue.
- Right: time-reversed white-hole analogue.
- Same spatial flow-speed profile, opposite flow direction.
- Horizon where the flow speed reaches the wave speed.
- Waves and flow are schematic rather than quantitatively exact.

Outputs:
    Figure_1.png
    Figure_1.pdf
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
import os
os.chdir("post2_horizons")


# =============================================================================
# Output
# =============================================================================

OUT_DIR = Path.cwd()
OUT_PNG = OUT_DIR / "Figure_1.png"
OUT_PDF = OUT_DIR / "Figure_1.pdf"

DPI = 220


# =============================================================================
# Style
# =============================================================================

plt.rcParams.update(
    {
        "font.size": 12,
        "axes.titlesize": 15,
        "axes.labelsize": 12,
        "figure.titlesize": 17,
        "font.family": "DejaVu Sans",
    }
)


# =============================================================================
# Geometry
# =============================================================================

XMIN, XMAX = 0.0, 10.0
YMIN, YMAX = -1.6, 1.6

HORIZON_X = 5.8

# Flow speed profile:
# slow on the left, fast on the right
x = np.linspace(XMIN, XMAX, 800)

V_SLOW = 0.35
V_FAST = 1.35
V_WAVE = 1.0
RAMP_WIDTH = 0.9

flow_speed = (
    V_SLOW
    + (V_FAST - V_SLOW)
    * 0.5
    * (1.0 + np.tanh((x - HORIZON_X) / RAMP_WIDTH))
)


# =============================================================================
# Drawing helpers
# =============================================================================

def draw_river(ax):
    """Draw the river background and horizon regions."""
    ax.set_xlim(XMIN, XMAX)
    ax.set_ylim(YMIN, YMAX)
    ax.set_aspect("auto")

    # Water strip
    ax.add_patch(
        Rectangle(
            (XMIN, -1.15),
            XMAX - XMIN,
            2.30,
            facecolor="#dcecf3",
            edgecolor="none",
            zorder=0,
        )
    )

    # Fast-flow region
    ax.axvspan(
        HORIZON_X,
        XMAX,
        color="#9ec9d9",
        alpha=0.32,
        zorder=0,
    )

    # Horizon
    ax.axvline(
        HORIZON_X,
        color="0.20",
        linestyle="--",
        linewidth=1.5,
        zorder=5,
    )

    ax.text(
        HORIZON_X+0.49,
        1.30,
        "horizon",
        ha="center",
        va="bottom",
        fontsize=11,
    )

    # Labels for flow regime
    ax.text(
        2.1,
        -1.38,
        "slow flow",
        ha="center",
        va="center",
        color="0.30",
    )

    ax.text(
        8.0,
        -1.38,
        "fast flow",
        ha="center",
        va="center",
        color="0.30",
    )

    # Clean axes
    ax.set_xticks([])
    ax.set_yticks([])

    for spine in ax.spines.values():
        spine.set_visible(False)


def draw_flow_arrows(ax, direction=+1):
    """
    Draw flow arrows.

    direction = +1 : flow right
    direction = -1 : flow left
    """
    xs = np.linspace(1.0, 9.0, 9)

    for xx in xs:
        speed = np.interp(xx, x, flow_speed)

        # Arrow length grows with flow speed
        length = 0.48 + 0.52 * speed

        x0 = xx - 0.5 * direction * length
        x1 = xx + 0.5 * direction * length

        arrow = FancyArrowPatch(
            (x0, 0.68),
            (x1, 0.68),
            arrowstyle="-|>",
            mutation_scale=13,
            linewidth=1.5,
            color="#356b88",
            zorder=3,
        )
        ax.add_patch(arrow)

    ax.text(
        1.0 if direction > 0 else 9.0,
        0.98,
        "flow",
        ha="left" if direction > 0 else "right",
        va="center",
        color="#356b88",
        fontsize=11,
        weight="bold",
    )


def draw_wave_packet(
    ax,
    center,
    width,
    wavelength,
    y0=-0.30,
    amplitude=0.25,
    direction=+1,
    color="#173b5e",
    alpha=1.0,
):
    """
    Draw a localized sinusoidal wave packet.

    direction indicates intended propagation direction.
    """
    xx = np.linspace(center - 2.5 * width, center + 2.5 * width, 700)

    envelope = np.exp(-((xx - center) / width) ** 2)

    phase = 2.0 * np.pi * (xx - center) / wavelength

    yy = y0 + amplitude * envelope * np.sin(phase)

    ax.plot(
        xx,
        yy,
        color=color,
        linewidth=2.2,
        alpha=alpha,
        zorder=4,
    )

    # Propagation arrow above packet
    arrow_length = 1.0

    if direction > 0:
        start = (center - 0.5, y0 + 0.48)
        end = (center - 0.5 + arrow_length, y0 + 0.48)
    else:
        start = (center + 0.5, y0 + 0.48)
        end = (center + 0.5 - arrow_length, y0 + 0.48)

    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=1.8,
            color=color,
            zorder=5,
        )
    )


def draw_blocking_marker(ax, x0, y0=-0.30):
    """Small visual cue that the incoming packet cannot continue."""
    ax.plot(
        [x0 - 0.08, x0 + 0.08],
        [y0 - 0.38, y0 + 0.38],
        color="0.25",
        linewidth=2.0,
        zorder=6,
    )


# =============================================================================
# Figure
# =============================================================================

fig, axes = plt.subplots(
    1,
    2,
    figsize=(14, 5.2),
    constrained_layout=True,
)

ax_bh, ax_wh = axes


# -----------------------------------------------------------------------------
# Left panel — black hole
# -----------------------------------------------------------------------------

draw_river(ax_bh)
draw_flow_arrows(ax_bh, direction=+1)

# Wave inside fast-flow region trying to go upstream
draw_wave_packet(
    ax_bh,
    center=7.6,
    width=0.95,
    wavelength=0.72,
    y0=-0.28,
    amplitude=0.24,
    direction=-1,
)

# Net dragging direction
# ax_bh.add_patch(
#     FancyArrowPatch(
#         (7.3, -0.95),
#         (8.5, -0.95),
#         arrowstyle="-|>",
#         mutation_scale=15,
#         linewidth=1.8,
#         color="#9a4d35",
#         zorder=5,
#     )
# )

# ax_bh.text(
#     7.9,
#     -0.82,
#     "dragged with flow",
#     ha="center",
#     va="bottom",
#     fontsize=10,
#     color="#9a4d35",
# )

ax_bh.text(
    7.6,
    0.08,
    "Outgoing wave blocked at horizon",
    ha="center",
    va="bottom",
    fontsize=10,
    color="#173b5e",
)

ax_bh.set_title("Black-Hole Horizon", pad=18)


# -----------------------------------------------------------------------------
# Right panel — white hole
# -----------------------------------------------------------------------------

draw_river(ax_wh)
draw_flow_arrows(ax_wh, direction=-1)

# Incoming wave from left
draw_wave_packet(
    ax_wh,
    center=4.25,
    width=1.15,
    wavelength=0.95,
    y0=-0.28,
    amplitude=0.24,
    direction=+1,
)

# draw_blocking_marker(
#     ax_wh,
#     HORIZON_X - 0.05,
#     y0=-0.28,
# )

ax_wh.text(
    3.85,
    0.08,
    "Incoming wave blocked at horizon",
    ha="center",
    va="bottom",
    fontsize=10,
    color="#173b5e",
)

# ax_wh.text(
#     HORIZON_X - 0.10,
#     -0.92,
#     "cannot cross",
#     ha="right",
#     va="center",
#     fontsize=10,
#     color="#9a4d35",
# )

ax_wh.set_title("White-Hole Horizon", pad=18)


# -----------------------------------------------------------------------------
# Time-reversal indication
# -----------------------------------------------------------------------------

# fig.text(
#     0.5,
#     0.96,
#     "Reverse The Flow, Reverse The Horizon",
#     ha="center",
#     va="top",
#     fontsize=17,
#     weight="bold",
# )

# fig.text(
#     0.5,
#     0.895,
#     "same flow-speed profile • opposite direction",
#     ha="center",
#     va="top",
#     fontsize=11,
#     color="0.35",
# )


# =============================================================================
# Save
# =============================================================================

fig.savefig(
    OUT_PNG,
    dpi=DPI,
    bbox_inches="tight",
    facecolor="white",
)

fig.savefig(
    OUT_PDF,
    bbox_inches="tight",
    facecolor="white",
)

print(f"Saved: {OUT_PNG}")
print(f"Saved: {OUT_PDF}")

plt.show()
#!/usr/bin/env python3
"""
generate_figure_1_local_experiment.py

Figure 1 — A local experiment reveals motion through the water.

Bob uses only:
    - his own clock, to drive a wave generator at one fixed frequency
    - a local wavelength measurement

The figure compares:
    1. Bob co-moving with the water
    2. Bob moving relative to the water

For finite-depth surface gravity waves:

    Omega(k)^2 = g k tanh(k h)

For positive k, the intrinsic branch is:

    Omega(k) = sqrt(g k tanh(k h))

If Bob moves with velocity v relative to the water, he measures:

    omega_B(k) = Omega(k) - v k

At the same measured drive frequency omega_drive, the two dispersion
curves are crossed at different wavenumbers k, hence different wavelengths:

    lambda = 2 pi / k

Output:
    Figure_1.png

The file is saved in the same directory as this script.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


# =============================================================================
# Paths
# =============================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = SCRIPT_DIR / "Figure_1.png"


# =============================================================================
# Physical parameters
# =============================================================================

G = 9.81          # m/s^2
H = 0.20          # water depth [m]

# Long-wavelength shallow-water speed
C0 = np.sqrt(G * H)

# Bob's velocity relative to the water
V_REST = 0.0
V_MOVING = 0.25 * C0

# Fixed drive frequency measured by Bob
OMEGA_DRIVE = 5.0   # rad/s


# =============================================================================
# Plot range
# =============================================================================

K_MIN = 0.0
K_MAX = 14.0
N_K = 5000

k = np.linspace(K_MIN, K_MAX, N_K)


# =============================================================================
# Visual style — same language as post 2
# =============================================================================

BG = "#090b10"
FG = "#eef2f7"
MUTED = "#9aa6b2"
GRID = "#27303a"

BLUE = "#57a6ff"
RED = "#ff6b70"
WHITE = "#ffffff"

FIGSIZE = (7.4, 6.4)
DPI = 190

TITLE_SIZE = 20
AXIS_LABEL_SIZE = 20
TICK_SIZE = 14
LEGEND_SIZE = 13
ANNOTATION_SIZE = 13
MARKER_SIZE = 95


def configure_style() -> None:
    """Set the dark publication style used in post 2."""
    mpl.rcParams.update(
        {
            "figure.facecolor": BG,
            "axes.facecolor": BG,
            "savefig.facecolor": BG,
            "text.color": FG,
            "axes.labelcolor": FG,
            "axes.edgecolor": MUTED,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "font.size": TICK_SIZE,
            "axes.labelsize": AXIS_LABEL_SIZE,
            "xtick.labelsize": TICK_SIZE,
            "ytick.labelsize": TICK_SIZE,
            "legend.fontsize": LEGEND_SIZE,
        }
    )


# =============================================================================
# Dispersion relation
# =============================================================================

def omega_water(k_value: np.ndarray) -> np.ndarray:
    """
    Positive-k finite-depth surface-gravity-wave dispersion:

        Omega(k) = sqrt(g k tanh(k h))
    """
    return np.sqrt(G * k_value * np.tanh(k_value * H))


def omega_measured(k_value: np.ndarray, velocity: float) -> np.ndarray:
    """
    Dispersion measured by Bob:

        omega_B(k) = Omega(k) - v k
    """
    return omega_water(k_value) - velocity * k_value


def find_crossing(
    k_value: np.ndarray,
    omega_value: np.ndarray,
    omega_target: float,
) -> float:
    """
    Find the first positive-k crossing with omega_target
    using linear interpolation.
    """
    residual = omega_value - omega_target

    idx = np.where(residual[:-1] * residual[1:] < 0.0)[0]

    if len(idx) == 0:
        raise RuntimeError(
            f"No crossing found for omega = {omega_target:.3f} rad/s."
        )

    j = idx[0]

    k0, k1 = k_value[j], k_value[j + 1]
    r0, r1 = residual[j], residual[j + 1]

    return k0 - r0 * (k1 - k0) / (r1 - r0)


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    configure_style()

    # Measured dispersion curves
    omega_rest = omega_measured(k, V_REST)
    omega_moving = omega_measured(k, V_MOVING)

    # Find the two wavelengths produced by the same drive frequency
    k_rest = find_crossing(
        k,
        omega_rest,
        OMEGA_DRIVE,
    )

    k_moving = find_crossing(
        k,
        omega_moving,
        OMEGA_DRIVE,
    )

    lambda_rest = 2.0 * np.pi / k_rest
    lambda_moving = 2.0 * np.pi / k_moving

    phase_speed_rest = OMEGA_DRIVE / k_rest
    phase_speed_moving = OMEGA_DRIVE / k_moving

    # -------------------------------------------------------------------------
    # Figure
    # -------------------------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=FIGSIZE,
    )

    # Dispersion curves
    ax.plot(
        k,
        omega_rest,
        color=BLUE,
        lw=3.2,
        label="co-moving with water",
        zorder=2,
    )

    ax.plot(
        k,
        omega_moving,
        color=RED,
        lw=3.2,
        label="moving relative to water",
        zorder=2,
    )

    # Fixed drive frequency
    ax.axhline(
        OMEGA_DRIVE,
        color=WHITE,
        lw=1.7,
        alpha=0.88,
        zorder=1,
    )

    ax.text(
        K_MAX * 0.97,
        OMEGA_DRIVE + 0.18,
        rf"same drive frequency  $\omega_B={OMEGA_DRIVE:.0f}$",
        ha="right",
        va="bottom",
        fontsize=ANNOTATION_SIZE,
        color=FG,
    )

    # Intersection markers
    ax.scatter(
        [k_rest],
        [OMEGA_DRIVE],
        s=MARKER_SIZE,
        color=BLUE,
        edgecolors=BG,
        linewidths=1.5,
        zorder=5,
    )

    ax.scatter(
        [k_moving],
        [OMEGA_DRIVE],
        s=MARKER_SIZE,
        color=RED,
        edgecolors=BG,
        linewidths=1.5,
        zorder=5,
    )

    # Vertical guides down to the k axis
    ax.vlines(
        k_rest,
        0.0,
        OMEGA_DRIVE,
        colors=BLUE,
        linestyles="--",
        linewidth=1.3,
        alpha=0.75,
        zorder=1,
    )

    ax.vlines(
        k_moving,
        0.0,
        OMEGA_DRIVE,
        colors=RED,
        linestyles="--",
        linewidth=1.3,
        alpha=0.75,
        zorder=1,
    )

    # k labels
    ax.text(
        k_rest,
        -0.45,
        r"$k_{\rm rest}$",
        ha="center",
        va="top",
        fontsize=ANNOTATION_SIZE,
        color=BLUE,
    )

    ax.text(
        k_moving,
        -0.45,
        r"$k_{\rm moving}$",
        ha="center",
        va="top",
        fontsize=ANNOTATION_SIZE,
        color=RED,
    )

    # -------------------------------------------------------------------------
    # Axes styling
    # -------------------------------------------------------------------------

    ax.set_xlim(K_MIN, K_MAX)

    y_max = max(
        np.max(omega_rest),
        np.max(omega_moving),
        OMEGA_DRIVE,
    )

    ax.set_ylim(
        0,
        1.08 * y_max,
    )


    ax.grid(
        True,
        color=GRID,
        linewidth=0.8,
        alpha=0.34,
    )

    # Put the x-axis exactly at omega = 0
    ax.spines["bottom"].set_position(("data", 0.0))
    ax.spines["bottom"].set_color(MUTED)
    ax.spines["bottom"].set_linewidth(1.0)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(MUTED)

    # Keep the y-axis at k = 0
    ax.spines["left"].set_position(("data", 0.0))

    # Ticks follow the moved axes
    ax.xaxis.set_ticks_position("bottom")
    ax.yaxis.set_ticks_position("left")

    ax.set_xlabel(
        r"wavenumber,  $k_B = 2\pi/\lambda$",
        fontsize=AXIS_LABEL_SIZE,
        labelpad=10,
    )

    ax.set_ylabel(
        r"$frequency, \omega_B = 2\pi/f$",
        fontsize=AXIS_LABEL_SIZE,
    )

    ax.legend(
        loc="lower right",
        frameon=True,
        facecolor=BG,
        edgecolor=MUTED,
        framealpha=0.80,
    )

    # fig.suptitle(
    #     "A Local Experiment Reveals Motion Through The Water",
    #     fontsize=TITLE_SIZE,
    #     y=0.98,
    # )

    fig.subplots_adjust(
        left=0.15,
        right=0.975,
        top=0.90,
        bottom=0.14,
    )

    fig.savefig(
        OUTPUT_PATH,
        dpi=DPI,
        bbox_inches="tight",
        pad_inches=0.10,
    )

    plt.close(fig)

    # -------------------------------------------------------------------------
    # Diagnostics
    # -------------------------------------------------------------------------

    print()
    print("Figure 1 — local wave experiment")
    print("--------------------------------")
    print(f"Water depth h                = {H:.3f} m")
    print(f"Shallow-water speed c0       = {C0:.3f} m/s")
    print(f"Bob's relative speed         = {V_MOVING:.3f} m/s")
    print(f"v / c0                       = {V_MOVING / C0:.3f}")
    print(f"Drive frequency omega_B      = {OMEGA_DRIVE:.3f} rad/s")
    print()
    print("Co-moving:")
    print(f"  k                           = {k_rest:.4f} rad/m")
    print(f"  wavelength lambda           = {lambda_rest:.4f} m")
    print(f"  phase velocity omega/k      = {phase_speed_rest:.4f} m/s")
    print()
    print("Moving relative to water:")
    print(f"  k                           = {k_moving:.4f} rad/m")
    print(f"  wavelength lambda           = {lambda_moving:.4f} m")
    print(f"  phase velocity omega/k      = {phase_speed_moving:.4f} m/s")
    print()
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
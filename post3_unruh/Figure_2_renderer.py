#!/usr/bin/env python3
"""
generate_figure_2_undetectable_ether.py

Figure 2 — What must an undetectable 'ether' look like?

Both panels start with exactly the same hypothetical rest-frame dispersion:

    omega^2 - c^2 k^2 = omega_0^2

Blue:
    dispersion measured in the hypothetical ether rest frame

Red:
    dispersion measured by an observer moving at velocity v

Left panel:
    Galilean transformation

        k'     = k
        omega' = omega - v k

    The dispersion changes.

Right panel:
    Lorentz transformation

        omega' = gamma (omega - v k)

        k' = gamma (k - v omega / c^2)

    The transformed points remain on exactly the same dispersion curve.

The point is visual rather than historical:
given the two different transformation laws, what happens to the same
wave dispersion when the observer changes?

Output:
    Figure_2.png
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
OUTPUT_PATH = SCRIPT_DIR / "Figure_2.png"


# =============================================================================
# Model parameters
# =============================================================================

# Dimensionless units
C = 1.0
OMEGA_0 = 1.0

# Observer velocity
V = 0.55 * C

GAMMA = 1.0 / np.sqrt(1.0 - (V / C) ** 2)

# Rest-frame k range
K_MIN = -3.2
K_MAX = +3.2
N_K = 5000

k = np.linspace(K_MIN, K_MAX, N_K)


# =============================================================================
# Visual style
# =============================================================================

BG = "#090b10"
FG = "#eef2f7"
MUTED = "#9aa6b2"
GRID = "#27303a"

BLUE = "#57a6ff"
RED = "#ff6b70"
WHITE = "#ffffff"

FIGSIZE = (12.0, 5.8)
DPI = 190

TITLE_SIZE = 19
PANEL_TITLE_SIZE = 18
AXIS_LABEL_SIZE = 18
TICK_SIZE = 13
LEGEND_SIZE = 12
ANNOTATION_SIZE = 13


def configure_style() -> None:
    """Apply the same dark visual language as the earlier figures."""
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
# Dispersion
# =============================================================================

def omega_rest(k_value: np.ndarray) -> np.ndarray:
    """
    Positive-frequency branch:

        omega^2 - c^2 k^2 = omega_0^2

    so

        omega = sqrt(omega_0^2 + c^2 k^2)
    """
    return np.sqrt(
        OMEGA_0**2 + C**2 * k_value**2
    )


# =============================================================================
# Transformations
# =============================================================================

def galilean_transform(
    k_value: np.ndarray,
    omega_value: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Galilean transformation:

        k'     = k
        omega' = omega - v k
    """
    k_prime = k_value
    omega_prime = omega_value - V * k_value

    return k_prime, omega_prime


def lorentz_transform(
    k_value: np.ndarray,
    omega_value: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Lorentz transformation of the wave four-vector:

        omega' = gamma (omega - v k)

        k' = gamma (k - v omega / c^2)
    """
    omega_prime = GAMMA * (
        omega_value - V * k_value
    )

    k_prime = GAMMA * (
        k_value - V * omega_value / C**2
    )

    return k_prime, omega_prime


# =============================================================================
# Axes
# =============================================================================

def style_axes(ax: plt.Axes) -> None:
    """Shared plot styling."""
    ax.grid(
        True,
        color=GRID,
        linewidth=0.8,
        alpha=0.34,
    )

    # Put k-axis at omega = 0
    ax.spines["bottom"].set_position(("data", 0.0))
    ax.spines["bottom"].set_color(MUTED)
    ax.spines["bottom"].set_linewidth(1.0)

    # Put omega-axis at k = 0
    ax.spines["left"].set_position(("data", 0.0))
    ax.spines["left"].set_color(MUTED)
    ax.spines["left"].set_linewidth(1.0)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.xaxis.set_ticks_position("bottom")
    ax.yaxis.set_ticks_position("left")

    ax.set_xlim(-3.6, 3.6)
    ax.set_ylim(0.0, 4.1)

    # Place compact axis labels manually so moving the spines does not
    # create awkward xlabel/ylabel positions.
    ax.text(
        0.985,
        0.045,
        r"$k$",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=AXIS_LABEL_SIZE,
        color=FG,
    )

    ax.text(
        0.515,
        0.965,
        r"$\omega$",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=AXIS_LABEL_SIZE,
        color=FG,
    )


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    configure_style()

    omega = omega_rest(k)

    # -------------------------------------------------------------------------
    # Transform the same rest-frame dispersion in two different ways
    # -------------------------------------------------------------------------

    k_gal, omega_gal = galilean_transform(
        k,
        omega,
    )

    k_lor, omega_lor = lorentz_transform(
        k,
        omega,
    )

    # Sort Lorentz-transformed points by k' so they form a clean curve
    order = np.argsort(k_lor)

    k_lor_sorted = k_lor[order]
    omega_lor_sorted = omega_lor[order]

    # -------------------------------------------------------------------------
    # Figure
    # -------------------------------------------------------------------------

    fig, axes = plt.subplots(
        1,
        2,
        figsize=FIGSIZE,
    )

    ax_gal, ax_lor = axes

    # =========================================================================
    # Left — Galilean
    # =========================================================================

    ax_gal.plot(
        k,
        omega,
        color=BLUE,
        lw=3.2,
        label=r"$v=0$",
        zorder=3,
    )

    ax_gal.plot(
        k_gal,
        omega_gal,
        color=RED,
        lw=3.2,
        label=rf"$v={V / C:.2f}\,c$",
        zorder=3,
    )

    ax_gal.set_title(
        "Galilean",
        fontsize=PANEL_TITLE_SIZE,
        pad=14,
    )

    ax_gal.text(
        0.2,
        1.01,
        r"$k'=k$",
        transform=ax_gal.transAxes,
        ha="left",
        va="top",
        fontsize=ANNOTATION_SIZE,
        color=MUTED,
    )

    ax_gal.text(
        0.2,
        0.94,
        r"$\omega'=\omega-vk$",
        transform=ax_gal.transAxes,
        ha="left",
        va="top",
        fontsize=ANNOTATION_SIZE,
        color=MUTED,
    )

    ax_gal.annotate(
        "",
        xy=(2.15, omega_rest(np.array([2.15]))[0] - V * 2.15),
        xytext=(2.15, omega_rest(np.array([2.15]))[0]),
        arrowprops=dict(
            arrowstyle="->",
            color=FG,
            lw=1.4,
            alpha=0.8,
        ),
    )

    ax_gal.text(
        2.30,
        2.25,
        "changes",
        color=FG,
        fontsize=ANNOTATION_SIZE,
        rotation=-18,
        ha="left",
        va="center",
    )

    # =========================================================================
    # Right — Lorentz
    # =========================================================================

    # Red transformed curve first
    ax_lor.plot(
        k_lor_sorted,
        omega_lor_sorted,
        color=RED,
        lw=5.0,
        alpha=0.85,
        zorder=2,
        label=rf"$v={V / C:.2f}\,c$",
    )

    # Blue original curve on top, slightly thinner.
    # Because the two curves coincide, the red remains visible around the edge.
    ax_lor.plot(
        k,
        omega,
        color=BLUE,
        lw=2.7,
        zorder=3,
        label=r"$v=0$",
    )

    # A few transformed points make the mapping visible.
    sample_indices = np.linspace(
        350,
        N_K - 350,
        9,
        dtype=int,
    )

    ax_lor.scatter(
        k_lor[sample_indices],
        omega_lor[sample_indices],
        s=48,
        facecolors=RED,
        edgecolors=BG,
        linewidths=1.0,
        zorder=4,
    )

    ax_lor.set_title(
        "Einstein / Lorentz",
        fontsize=PANEL_TITLE_SIZE,
        pad=14,
    )

    ax_lor.text(
        0.10,
        0.91,
        r"$\omega'=\gamma(\omega-vk)$",
        transform=ax_lor.transAxes,
        ha="left",
        va="top",
        fontsize=ANNOTATION_SIZE,
        color=MUTED,
    )

    ax_lor.text(
        0.10,
        0.84,
        r"$k'=\gamma(k-v\omega/c^2)$",
        transform=ax_lor.transAxes,
        ha="left",
        va="top",
        fontsize=ANNOTATION_SIZE,
        color=MUTED,
    )

    ax_lor.text(
        0.68,
        0.20,
        r"$\omega^2-c^2k^2=\omega_0^2$",
        transform=ax_lor.transAxes,
        ha="center",
        va="center",
        fontsize=ANNOTATION_SIZE,
        color=FG,
    )

    ax_lor.text(
        0.60,
        0.65,
        "moves along\nthe same\ncurve",
        transform=ax_lor.transAxes,
        ha="left",
        va="center",
        fontsize=ANNOTATION_SIZE,
        color=FG,
    )

    ax_lor.annotate(
            "",
            xy=(0.95, 1.5),
            xytext=(2.45, 2.8),
            arrowprops=dict(
                arrowstyle="->",
                color=FG,
                lw=1.4,
                alpha=0.8,
            ),
        )

    # -------------------------------------------------------------------------
    # Shared styling
    # -------------------------------------------------------------------------

    for ax in axes:
        style_axes(ax)

    # Put legends in opposite corners to avoid covering the curves
    ax_gal.legend(
        loc="upper right",
        frameon=False,
    )

    ax_lor.legend(
        loc="upper right",
        frameon=False,
    )

    fig.subplots_adjust(
        left=0.06,
        right=0.985,
        top=0.92,
        bottom=0.08,
        wspace=0.18,
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

    invariant_before = omega**2 - C**2 * k**2
    invariant_after = omega_lor**2 - C**2 * k_lor**2

    max_error = np.max(
        np.abs(invariant_after - invariant_before)
    )

    print()
    print("Figure 2")
    print("--------")
    print(f"v / c                  = {V / C:.3f}")
    print(f"gamma                  = {GAMMA:.6f}")
    print(f"omega_0                = {OMEGA_0:.3f}")
    print(f"max invariant error    = {max_error:.3e}")
    print(f"saved                   = {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
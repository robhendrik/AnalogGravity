#!/usr/bin/env python3
"""
generate_figure_4_bogoliubov_mixing.py

Figure 4 — From frequency mixing to particles.

Top:
    The same classical wave is decomposed differently by Alice and Bob.

    Alice sees a purely positive-frequency spectrum.

    Bob's accelerated sampling produces an asymmetric spectrum with a tail
    extending into negative frequencies.

    For ideal uniform acceleration:

        |beta|^2 / |alpha|^2 = exp(-2 pi c Omega / a)

Bottom:
    In the quantum field expansion:

        positive-frequency modes pair with annihilation operators
        negative-frequency modes pair with creation operators

    Alice's number operator gives zero on the Minkowski vacuum.

    Bob's accelerated number operator gives

        <N_B> = |beta|^2
              = 1 / [exp(2 pi c Omega / a) - 1]

Output:
    Figure_4.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


# =============================================================================
# Paths
# =============================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = SCRIPT_DIR / "Figure_4.png"


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

FIGSIZE = (10.8, 11.2)
DPI = 190

SECTION_SIZE = 19
COLUMN_SIZE = 17
MAIN_SIZE = 18
EQ_SIZE = 18
SMALL_SIZE = 13


def configure_style() -> None:
    """Apply the dark visual language used in the article."""
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
            "font.size": SMALL_SIZE,
            "mathtext.fontset": "dejavusans",
        }
    )


# =============================================================================
# Helpers
# =============================================================================

def rounded_box(
    ax: plt.Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    edge_color: str = MUTED,
    linewidth: float = 1.3,
) -> None:
    """Draw a rounded rectangle."""
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.015,rounding_size=0.018",
        facecolor=BG,
        edgecolor=edge_color,
        linewidth=linewidth,
        zorder=1,
    )
    ax.add_patch(patch)


def arrow(
    ax: plt.Axes,
    start: tuple[float, float],
    end: tuple[float, float],
    color: str = FG,
    linewidth: float = 1.8,
    mutation_scale: float = 17,
) -> None:
    """Draw an arrow."""
    patch = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=mutation_scale,
        linewidth=linewidth,
        color=color,
        shrinkA=2,
        shrinkB=2,
        zorder=5,
    )
    ax.add_patch(patch)


def gaussian(x: np.ndarray, mu: float, sigma: float) -> np.ndarray:
    """Gaussian profile."""
    return np.exp(
        -0.5 * ((x - mu) / sigma) ** 2
    )


# =============================================================================
# Spectrum sketches
# =============================================================================

def draw_alice_spectrum(ax: plt.Axes) -> None:
    """Draw Alice's positive-frequency-only spectrum."""
    x0 = 0.08
    x1 = 0.43
    y0 = 0.755

    # Horizontal axis
    ax.plot(
        [x0, x1],
        [y0, y0],
        color=MUTED,
        lw=1.0,
    )

    # Zero-frequency axis
    x_zero = 0.245
    ax.plot(
        [x_zero, x_zero],
        [y0 - 0.012, y0 + 0.18],
        color=GRID,
        lw=1.0,
    )

    # Positive peak
    x = np.linspace(
        x_zero,
        x1 - 0.015,
        500,
    )

    mu = 0.34
    sigma = 0.022

    y = (
        y0
        + 0.115 * gaussian(
            x,
            mu,
            sigma,
        )
    )

    ax.plot(
        x,
        y,
        color=BLUE,
        lw=2.8,
    )

    ax.fill_between(
        x,
        y0,
        y,
        color=BLUE,
        alpha=0.18,
    )

    # Labels
    ax.text(
        0.34,
        0.885,
        r"$+\Omega$",
        ha="center",
        va="center",
        fontsize=MAIN_SIZE,
        color=BLUE,
    )

    ax.text(
        0.15,
        0.785,
        r"$-\Omega$",
        ha="center",
        va="center",
        fontsize=MAIN_SIZE,
        color=RED,
        alpha=0.45,
    )

    ax.text(
        0.15,
        0.724,
        "none",
        ha="center",
        va="center",
        fontsize=SMALL_SIZE,
        color=MUTED,
    )

    ax.text(
        0.34,
        0.714,
        "positive frequency",
        ha="center",
        va="center",
        fontsize=SMALL_SIZE,
        color=BLUE,
    )


def draw_bob_spectrum(ax: plt.Axes) -> None:
    """
    Draw Bob's spectrum as one asymmetric peak with a negative-frequency tail.

    The blue part dominates at positive frequencies.
    The red part highlights the tail extending through zero into negative
    frequencies.

    This is schematic rather than a literal quantitative spectrum.
    """
    x0 = 0.57
    x1 = 0.92
    y0 = 0.755

    x_zero = 0.745

    # Horizontal axis
    ax.plot(
        [x0, x1],
        [y0, y0],
        color=MUTED,
        lw=1.0,
    )

    # Zero-frequency marker
    ax.plot(
        [x_zero, x_zero],
        [y0 - 0.012, y0 + 0.18],
        color=GRID,
        lw=1.0,
    )

    # Build one asymmetric spectral profile:
    #
    # - a narrow positive-frequency peak
    # - a broader low-frequency shoulder/tail
    #
    x = np.linspace(
        x0 + 0.015,
        x1 - 0.015,
        1000,
    )

    positive_peak = gaussian(
        x,
        0.835,
        0.027,
    )

    broad_tail = 0.25 * gaussian(
        x,
        0.765,
        0.075,
    )

    profile = (
        positive_peak
        + broad_tail
    )

    profile /= profile.max()

    y = y0 + 0.115 * profile

    # Draw complete profile faintly first
    ax.plot(
        x,
        y,
        color=BLUE,
        lw=2.7,
        alpha=0.92,
    )

    ax.fill_between(
        x,
        y0,
        y,
        color=BLUE,
        alpha=0.13,
    )

    # Highlight the negative-frequency part in red.
    mask_neg = x <= x_zero

    ax.plot(
        x[mask_neg],
        y[mask_neg],
        color=RED,
        lw=2.8,
        zorder=5,
    )

    ax.fill_between(
        x[mask_neg],
        y0,
        y[mask_neg],
        color=RED,
        alpha=0.18,
        zorder=3,
    )

    # Smoothly blend a little into the positive side so the tail reads
    # visually as part of the SAME peak rather than a second peak.
    mask_blend = (
        (x > x_zero)
        & (x < x_zero + 0.035)
    )

    ax.plot(
        x[mask_blend],
        y[mask_blend],
        color=RED,
        lw=2.2,
        alpha=0.65,
        zorder=5,
    )

    # Labels
    ax.text(
        0.84,
        0.885,
        r"$+\Omega$",
        ha="center",
        va="center",
        fontsize=MAIN_SIZE,
        color=BLUE,
    )

    ax.text(
        0.655,
        0.785,
        r"$-\Omega$",
        ha="center",
        va="center",
        fontsize=MAIN_SIZE,
        color=RED,
    )

    ax.text(
        0.835,
        0.714,
        r"$|\alpha|^2$",
        ha="center",
        va="center",
        fontsize=SMALL_SIZE + 1,
        color=BLUE,
    )

    ax.text(
        0.655,
        0.714,
        r"$|\beta|^2$",
        ha="center",
        va="center",
        fontsize=SMALL_SIZE + 1,
        color=RED,
    )


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    """Generate Figure 4."""
    configure_style()

    fig, ax = plt.subplots(
        figsize=FIGSIZE,
        facecolor=BG,
    )

    ax.set_xlim(
        0.0,
        1.0,
    )
    ax.set_ylim(
        0.0,
        1.0,
    )
    ax.axis("off")

    # =========================================================================
    # TOP — CLASSICAL FIELD
    # =========================================================================

    ax.text(
        0.50,
        0.965,
        "Classical field",
        ha="center",
        va="center",
        fontsize=SECTION_SIZE,
        color=FG,
    )

    ax.text(
        0.25,
        0.918,
        "Alice — inertial",
        ha="center",
        va="center",
        fontsize=COLUMN_SIZE,
        color=FG,
    )

    ax.text(
        0.75,
        0.918,
        "Bob — accelerated",
        ha="center",
        va="center",
        fontsize=COLUMN_SIZE,
        color=FG,
    )

    draw_alice_spectrum(
        ax
    )

    draw_bob_spectrum(
        ax
    )

    # Same-wave arrow
    arrow(
        ax,
        (0.445, 0.82),
        (0.555, 0.82),
        color=FG,
        linewidth=1.5,
    )

    ax.text(
        0.50,
        0.85,
        "same wave",
        ha="center",
        va="center",
        fontsize=SMALL_SIZE,
        color=MUTED,
    )

    # Classical relation
    ax.text(
        0.50,
        0.645,
        r"$\frac{|\beta|^2}{|\alpha|^2}"
        r"="
        r"e^{-2\pi c\Omega/a}$",
        ha="center",
        va="center",
        fontsize=EQ_SIZE,
        color=FG,
    )

    ax.text(
        0.50,
        0.600,
        "acceleration mixes positive and negative frequencies",
        ha="center",
        va="center",
        fontsize=SMALL_SIZE,
        color=MUTED,
    )

    # =========================================================================
    # DIVIDER / QUANTIZATION
    # =========================================================================

    divider_y = 0.535

    ax.plot(
        [0.08, 0.92],
        [divider_y, divider_y],
        color=GRID,
        lw=1.0,
    )

    ax.text(
        0.50,
        0.505,
        "quantize",
        ha="center",
        va="center",
        fontsize=SMALL_SIZE,
        color=MUTED,
    )

    arrow(
        ax,
        (0.50, 0.485),
        (0.50, 0.448),
        color=FG,
        linewidth=1.6,
    )

    # =========================================================================
    # QUANTUM FIELD
    # =========================================================================

    ax.text(
        0.50,
        0.410,
        "Quantum field",
        ha="center",
        va="center",
        fontsize=SECTION_SIZE,
        color=FG,
    )

    # Positive frequency -> annihilation
    ax.text(
        0.28,
        0.355,
        r"$+\Omega$",
        ha="center",
        va="center",
        fontsize=MAIN_SIZE,
        color=BLUE,
    )

    arrow(
        ax,
        (0.34, 0.355),
        (0.405, 0.355),
        color=BLUE,
        linewidth=1.8,
    )

    ax.text(
        0.46,
        0.355,
        r"$\hat a$",
        ha="center",
        va="center",
        fontsize=25,
        color=FG,
    )

    ax.text(
        0.46,
        0.322,
        "annihilation",
        ha="center",
        va="center",
        fontsize=SMALL_SIZE,
        color=BLUE,
    )

    # Negative frequency -> creation
    ax.text(
        0.58,
        0.355,
        r"$-\Omega$",
        ha="center",
        va="center",
        fontsize=MAIN_SIZE,
        color=RED,
    )

    arrow(
        ax,
        (0.64, 0.355),
        (0.705, 0.355),
        color=RED,
        linewidth=1.8,
    )

    ax.text(
        0.76,
        0.355,
        r"$\hat a^\dagger$",
        ha="center",
        va="center",
        fontsize=25,
        color=FG,
    )

    ax.text(
        0.76,
        0.322,
        "creation",
        ha="center",
        va="center",
        fontsize=SMALL_SIZE,
        color=RED,
    )

    # =========================================================================
    # ALICE / BOB NUMBER OPERATORS
    # =========================================================================

    ax.text(
        0.25,
        0.265,
        "Alice",
        ha="center",
        va="center",
        fontsize=COLUMN_SIZE,
        color=FG,
    )

    ax.text(
        0.75,
        0.265,
        "Bob",
        ha="center",
        va="center",
        fontsize=COLUMN_SIZE,
        color=FG,
    )

    # Alice box
    rounded_box(
        ax,
        0.09,
        0.105,
        0.32,
        0.125,
        edge_color=BLUE,
        linewidth=1.5,
    )

    ax.text(
        0.25,
        0.198,
        r"$\hat N_A=\hat a^\dagger\hat a$",
        ha="center",
        va="center",
        fontsize=EQ_SIZE,
        color=FG,
    )

    ax.text(
        0.25,
        0.155,
        r"$\langle0_A|\hat N_A|0_A\rangle=0$",
        ha="center",
        va="center",
        fontsize=EQ_SIZE,
        color=BLUE,
    )

    ax.text(
        0.25,
        0.122,
        "vacuum",
        ha="center",
        va="center",
        fontsize=SMALL_SIZE,
        color=MUTED,
    )

    # Bob box
    rounded_box(
        ax,
        0.59,
        0.085,
        0.32,
        0.145,
        edge_color=RED,
        linewidth=1.5,
    )

    ax.text(
        0.75,
        0.198,
        r"$\hat N_B=\hat b^\dagger\hat b$",
        ha="center",
        va="center",
        fontsize=EQ_SIZE,
        color=FG,
    )

    ax.text(
        0.75,
        0.157,
        r"$\langle0_A|\hat N_B|0_A\rangle"
        r"="
        r"|\beta|^2$",
        ha="center",
        va="center",
        fontsize=EQ_SIZE,
        color=RED,
    )

    ax.text(
        0.75,
        0.110,
        r"$|\beta|^2"
        r"="
        r"\frac{1}{e^{2\pi c\Omega/a}-1}$",
        ha="center",
        va="center",
        fontsize=EQ_SIZE - 1,
        color=FG,
    )

    # Bogoliubov normalization below both boxes
    ax.text(
        0.50,
        0.038,
        r"$|\alpha|^2-|\beta|^2=1$",
        ha="center",
        va="center",
        fontsize=SMALL_SIZE,
        color=MUTED,
    )

    # =========================================================================
    # Save
    # =========================================================================

    fig.savefig(
        OUTPUT_PATH,
        dpi=DPI,
        bbox_inches="tight",
        pad_inches=0.12,
        facecolor=BG,
    )

    plt.close(
        fig
    )

    print()
    print("Figure 4 — From frequency mixing to particles")
    print("----------------------------------------------")
    print()
    print("Top:")
    print("  Alice sees only positive frequency.")
    print("  Bob sees the same wave with a tail extending into negative frequency.")
    print()
    print("Classical relation:")
    print(
        "  |beta|^2 / |alpha|^2 "
        "= exp(-2 pi c Omega / a)"
    )
    print()
    print("Quantum:")
    print("  positive frequency -> annihilation operator")
    print("  negative frequency -> creation operator")
    print()
    print("Alice:")
    print("  <N_A> = 0")
    print()
    print("Bob:")
    print(
        "  <N_B> = |beta|^2 "
        "= 1 / [exp(2 pi c Omega/a) - 1]"
    )
    print()
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

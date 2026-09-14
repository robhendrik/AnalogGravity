#!/usr/bin/env python3
"""
generate_appendix_exponential.py

Appendix figure — Where does the exponential come from?

Purpose
-------
Show, compactly and visually, why a uniformly accelerated observer
samples a monochromatic Minkowski wave with an exponential phase.

The logic is:

1. Successive infinitesimal Lorentz boosts:
       v + dv = (v + du) / (1 + v du / c^2)

2. For constant proper acceleration:
       du = a dτ

   giving:
       dv/dτ = a (1 - v^2/c^2)

3. Integrating:
       v/c = tanh(aτ/c)

4. Therefore the uniformly accelerated trajectory is:
       ct = (c^2/a) sinh(aτ/c)
       x  = (c^2/a) cosh(aτ/c)

5. A right-moving wave depends on:
       u = t - x/c

   so:
       u(τ)
       = (c/a)[sinh(aτ/c) - cosh(aτ/c)]
       = -(c/a) exp(-aτ/c)

6. Therefore:
       exp[-iω(t-x/c)]
       ->
       exp[i (ωc/a) exp(-aτ/c)]

The exponential frequency chirp follows directly from the hyperbolic
Lorentz-boost trajectory.

Output
------
Appendix_exponential.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


# =============================================================================
# Paths
# =============================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = SCRIPT_DIR / "Appendix_exponential.png"


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

FIGSIZE = (9.0, 11.5)
DPI = 190

TITLE_SIZE = 19
STEP_SIZE = 14
EQ_SIZE = 18
BIG_EQ_SIZE = 21
SMALL_SIZE = 12


def configure_style() -> None:
    """Apply the visual style used throughout the article."""
    mpl.rcParams.update(
        {
            "figure.facecolor": BG,
            "axes.facecolor": BG,
            "savefig.facecolor": BG,
            "text.color": FG,
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
    edge_color: str = GRID,
    linewidth: float = 1.2,
) -> None:
    """Draw a rounded rectangle."""
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.014,rounding_size=0.018",
        facecolor=BG,
        edgecolor=edge_color,
        linewidth=linewidth,
        zorder=1,
    )
    ax.add_patch(patch)


def down_arrow(
    ax: plt.Axes,
    y_start: float,
    y_end: float,
    color: str = MUTED,
) -> None:
    """Draw a centered downward arrow."""
    patch = FancyArrowPatch(
        (0.50, y_start),
        (0.50, y_end),
        arrowstyle="-|>",
        mutation_scale=16,
        linewidth=1.5,
        color=color,
        zorder=5,
    )
    ax.add_patch(patch)


def equation(
    ax: plt.Axes,
    y: float,
    text: str,
    color: str = FG,
    fontsize: float = EQ_SIZE,
) -> None:
    """Draw a centered equation."""
    ax.text(
        0.50,
        y,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=color,
        zorder=5,
    )


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    """Generate the appendix derivation figure."""
    configure_style()

    fig, ax = plt.subplots(
        figsize=FIGSIZE,
        facecolor=BG,
    )

    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)
    ax.axis("off")

    # =========================================================================
    # Title
    # =========================================================================

    ax.text(
        0.50,
        0.965,
        "Where Does The Exponential Come From?",
        ha="center",
        va="center",
        fontsize=TITLE_SIZE,
        color=FG,
    )

    ax.text(
        0.50,
        0.930,
        "constant proper acceleration = successive Lorentz boosts",
        ha="center",
        va="center",
        fontsize=SMALL_SIZE,
        color=MUTED,
    )

    # =========================================================================
    # Step 1 — Lorentz velocity addition
    # =========================================================================

    rounded_box(
        ax,
        0.10,
        0.795,
        0.80,
        0.105,
        edge_color=BLUE,
    )

    ax.text(
        0.15,
        0.873,
        "1   Infinitesimal Lorentz boost",
        ha="left",
        va="center",
        fontsize=STEP_SIZE,
        color=BLUE,
    )

    equation(
        ax,
        0.830,
        r"$v+dv="
        r"\frac{v+du}"
        r"{1+v\,du/c^2}$",
    )

    ax.text(
        0.50,
        0.800,
        r"$du=a\,d\tau$   for constant proper acceleration",
        ha="center",
        va="center",
        fontsize=SMALL_SIZE,
        color=MUTED,
    )

    down_arrow(
        ax,
        0.785,
        0.755,
    )

    # =========================================================================
    # Step 2 — differential equation
    # =========================================================================

    rounded_box(
        ax,
        0.15,
        0.670,
        0.70,
        0.075,
    )

    ax.text(
        0.19,
        0.722,
        "2   Repeated boosts",
        ha="left",
        va="center",
        fontsize=STEP_SIZE,
        color=FG,
    )

    equation(
        ax,
        0.690,
        r"$\frac{dv}{d\tau}"
        r"="
        r"a\left(1-\frac{v^2}{c^2}\right)$",
    )

    down_arrow(
        ax,
        0.657,
        0.625,
    )

    # =========================================================================
    # Step 3 — velocity / rapidity
    # =========================================================================

    rounded_box(
        ax,
        0.15,
        0.535,
        0.70,
        0.080,
    )

    ax.text(
        0.19,
        0.592,
        "3   Integrate",
        ha="left",
        va="center",
        fontsize=STEP_SIZE,
        color=FG,
    )

    equation(
        ax,
        0.555,
        r"$\frac{v}{c}"
        r"="
        r"\tanh\!\left(\frac{a\tau}{c}\right)$",
        color=BLUE,
    )

    down_arrow(
        ax,
        0.522,
        0.490,
    )

    # =========================================================================
    # Step 4 — trajectory
    # =========================================================================

    rounded_box(
        ax,
        0.10,
        0.365,
        0.80,
        0.115,
        edge_color=BLUE,
    )

    ax.text(
        0.15,
        0.458,
        "4   Hyperbolic trajectory",
        ha="left",
        va="center",
        fontsize=STEP_SIZE,
        color=BLUE,
    )

    equation(
        ax,
        0.417,
        r"$t(\tau)"
        r"="
        r"\frac{c}{a}"
        r"\sinh\!\left(\frac{a\tau}{c}\right)$",
    )

    equation(
        ax,
        0.382,
        r"$x(\tau)"
        r"="
        r"\frac{c^2}{a}"
        r"\cosh\!\left(\frac{a\tau}{c}\right)$",
    )

    down_arrow(
        ax,
        0.352,
        0.320,
    )

    # =========================================================================
    # Step 5 — light-cone coordinate becomes exponential
    # =========================================================================

    ax.text(
        0.50,
        0.298,
        "For a right-moving wave, only  "
        r"$t-x/c$"
        "  matters",
        ha="center",
        va="center",
        fontsize=SMALL_SIZE,
        color=MUTED,
    )

    equation(
        ax,
        0.255,
        r"$t-\frac{x}{c}"
        r"="
        r"\frac{c}{a}"
        r"\left["
        r"\sinh\!\left(\frac{a\tau}{c}\right)"
        r"-"
        r"\cosh\!\left(\frac{a\tau}{c}\right)"
        r"\right]$",
        fontsize=EQ_SIZE - 1,
    )

    equation(
        ax,
        0.205,
        r"$\sinh\eta-\cosh\eta=-e^{-\eta}$",
        color=RED,
        fontsize=EQ_SIZE,
    )

    equation(
        ax,
        0.155,
        r"$t-\frac{x}{c}"
        r"="
        r"-\frac{c}{a}"
        r"e^{-a\tau/c}$",
        color=RED,
        fontsize=BIG_EQ_SIZE,
    )

    # =========================================================================
    # Final wave
    # =========================================================================

    down_arrow(
        ax,
        0.125,
        0.100,
        color=RED,
    )

    ax.text(
        0.50,
        0.075,
        r"$e^{-i\omega(t-x/c)}"
        r"\quad\longrightarrow\quad"
        r"e^{\,i(\omega c/a)e^{-a\tau/c}}$",
        ha="center",
        va="center",
        fontsize=BIG_EQ_SIZE - 1,
        color=FG,
    )

    ax.text(
        0.50,
        0.030,
        "a single frequency for Alice becomes an exponential chirp for Bob",
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

    plt.close(fig)

    print()
    print("Appendix — Where does the exponential come from?")
    print("-------------------------------------------------")
    print()
    print("Lorentz velocity addition")
    print("        ↓")
    print("constant proper acceleration")
    print("        ↓")
    print("v/c = tanh(a tau / c)")
    print("        ↓")
    print("t ~ sinh(a tau/c), x ~ cosh(a tau/c)")
    print("        ↓")
    print("sinh(eta) - cosh(eta) = -exp(-eta)")
    print("        ↓")
    print("t - x/c = -(c/a) exp(-a tau/c)")
    print()
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
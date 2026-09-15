#!/usr/bin/env python3
"""
generate_figure_4_bogoliubov_mixing_v2.py

Figure 4 — From frequency mixing to thermal occupation.

Requested layout:
- Classical field: Alice has only Omega > 0; Bob has the same wave with
  a negative-frequency tail.
- Omega < 0 and Omega > 0 appear in BOTH panels at the same height.
- No "none", "positive frequency", explanatory Omega sentence, "quantize",
  or downward quantization arrow.
- Quantum bridge explicitly shows:
      Omega > 0 -> annihilation
      Omega < 0 -> creation
- Alice and Bob number-operator boxes are equal size, with comfortable
  line spacing.
- No |alpha|^2 - |beta|^2 = 1 line at the bottom.

Output:
    Figure_4.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = SCRIPT_DIR / "Figure_4.png"

BG = "#090b10"
FG = "#eef2f7"
MUTED = "#9aa6b2"
GRID = "#27303a"
BLUE = "#57a6ff"
RED = "#ff6b70"

FIGSIZE = (10.8, 11.2)
DPI = 190

SECTION_SIZE = 19
COLUMN_SIZE = 17
EQ_SIZE = 22
SMALL_SIZE = 13


def configure_style() -> None:
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


def rounded_box(
    ax: plt.Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    edge_color: str,
    linewidth: float = 1.5,
) -> None:
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
    return np.exp(-0.5 * ((x - mu) / sigma) ** 2)


def frequency_region_labels(
    ax: plt.Axes,
    x_neg: float,
    x_pos: float,
    y: float,
) -> None:
    """Put Omega<0 and Omega>0 at identical vertical positions."""
    ax.text(
        x_neg,
        y+0.01,
        r"$\Omega < 0$",
        ha="center",
        va="center",
        fontsize=SMALL_SIZE + 1,
        color=RED,
    )
    ax.text(
        x_pos,
        y+0.01,
        r"$\Omega > 0$",
        ha="center",
        va="center",
        fontsize=SMALL_SIZE + 1,
        color=BLUE,
    )


def draw_alice_spectrum(ax: plt.Axes) -> None:
    x0, x1 = 0.08, 0.43
    y0 = 0.765
    x_zero = 0.245

    ax.plot([x0, x1], [y0, y0], color=MUTED, lw=1.0)
    ax.plot(
        [x_zero, x_zero],
        [y0 - 0.012, y0 + 0.175],
        color=GRID,
        lw=1.0,
    )

    x = np.linspace(x_zero, x1 - 0.015, 500)
    y = y0 + 0.115 * gaussian(x, 0.34, 0.022)

    ax.plot(x, y, color=BLUE, lw=2.8)
    ax.fill_between(x, y0, y, color=BLUE, alpha=0.18)

    # Same height as Bob's labels.
    frequency_region_labels(
        ax,
        x_neg=0.165,
        x_pos=0.365,
        y=0.885,
    )


def draw_bob_spectrum(ax: plt.Axes) -> None:
    x0, x1 = 0.57, 0.92
    y0 = 0.765
    x_zero = 0.745

    ax.plot([x0, x1], [y0, y0], color=MUTED, lw=1.0)
    ax.plot(
        [x_zero, x_zero],
        [y0 - 0.012, y0 + 0.175],
        color=GRID,
        lw=1.0,
    )

    x = np.linspace(x0 + 0.015, x1 - 0.015, 1000)

    positive_peak = gaussian(x, 0.835, 0.027)
    broad_tail = 0.25 * gaussian(x, 0.765, 0.075)
    profile = positive_peak + broad_tail
    profile /= profile.max()

    y = y0 + 0.115 * profile

    # One continuous spectrum.
    ax.plot(x, y, color=BLUE, lw=2.7, alpha=0.92)
    ax.fill_between(x, y0, y, color=BLUE, alpha=0.13)

    # Highlight the negative-frequency part.
    mask_neg = x <= x_zero
    ax.plot(x[mask_neg], y[mask_neg], color=RED, lw=2.8, zorder=5)
    ax.fill_between(
        x[mask_neg],
        y0,
        y[mask_neg],
        color=RED,
        alpha=0.18,
        zorder=3,
    )

    # Slight blend across zero so it still reads as one peak.
    mask_blend = (x > x_zero) & (x < x_zero + 0.035)
    ax.plot(
        x[mask_blend],
        y[mask_blend],
        color=RED,
        lw=2.2,
        alpha=0.65,
        zorder=5,
    )

    frequency_region_labels(
        ax,
        x_neg=0.665,
        x_pos=0.865,
        y=0.885,
    )

    # Bogoliubov weights beneath the two frequency regions.
    ax.text(
        0.655,
        0.720,
        r"$|\beta|^2$",
        ha="center",
        va="center",
        fontsize=SMALL_SIZE + 1,
        color=RED,
    )
    ax.text(
        0.835,
        0.720,
        r"$|\alpha|^2$",
        ha="center",
        va="center",
        fontsize=SMALL_SIZE + 1,
        color=BLUE,
    )


def main() -> None:
    configure_style()

    fig, ax = plt.subplots(figsize=FIGSIZE, facecolor=BG)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)
    ax.axis("off")

    # -------------------------------------------------------------------------
    # Classical field
    # -------------------------------------------------------------------------

    ax.text(
        0.50, 0.965,
        "Classical field",
        ha="center", va="center",
        fontsize=SECTION_SIZE, color=FG,
    )

    ax.text(
        0.25, 0.925,
        "Alice — inertial",
        ha="center", va="center",
        fontsize=COLUMN_SIZE, color=FG,
    )
    ax.text(
        0.75, 0.925,
        "Bob — accelerated",
        ha="center", va="center",
        fontsize=COLUMN_SIZE, color=FG,
    )

    draw_alice_spectrum(ax)
    draw_bob_spectrum(ax)

    # Same-wave arrow.
    ax.text(
        0.50, 0.855,
        "same wave",
        ha="center", va="center",
        fontsize=SMALL_SIZE, color=MUTED,
    )
    arrow(
        ax,
        (0.445, 0.825),
        (0.555, 0.825),
        color=FG,
        linewidth=1.5,
    )

    # Classical mixing relation.
    ax.text(
        0.50, 0.665,
        r"$\frac{|\beta|^2}{|\alpha|^2}"
        r"=e^{-2\pi c\Omega/a}$",
        ha="center", va="center",
        fontsize=EQ_SIZE, color=FG,
    )

    # ax.text(
    #     0.50, 0.620,
    #     "acceleration mixes positive and negative frequencies",
    #     ha="center", va="center",
    #     fontsize=SMALL_SIZE, color=MUTED,
    # )

    # Divider only: no "quantize" label and no downward arrow.
    divider_y = 0.570
    ax.plot(
        [0.08, 0.92],
        [divider_y, divider_y],
        color=GRID,
        lw=1.0,
    )

    # -------------------------------------------------------------------------
    # Quantum field
    # -------------------------------------------------------------------------

    ax.text(
        0.50, 0.525,
        "Quantum field",
        ha="center", va="center",
        fontsize=SECTION_SIZE, color=FG,
    )

    # Positive-frequency modes -> annihilation operators.
    ax.text(
        0.275, 0.465,
        r"$\Omega > 0$",
        ha="center", va="center",
        fontsize=SMALL_SIZE + 1, color=BLUE,
    )
    arrow(
        ax,
        (0.345, 0.465),
        (0.405, 0.465),
        color=BLUE,
        linewidth=1.8,
    )
    ax.text(
        0.455, 0.465,
        r"$\hat a$",
        ha="center", va="center",
        fontsize=25, color=FG,
    )
    ax.text(
        0.455, 0.418,
        "annihilation",
        ha="center", va="center",
        fontsize=SMALL_SIZE, color=BLUE,
    )

    # Negative-frequency modes -> creation operators.
    ax.text(
        0.575, 0.465,
        r"$\Omega < 0$",
        ha="center", va="center",
        fontsize=SMALL_SIZE + 1, color=RED,
    )
    arrow(
        ax,
        (0.645, 0.465),
        (0.705, 0.465),
        color=RED,
        linewidth=1.8,
    )
    ax.text(
        0.755, 0.465,
        r"$\hat a^\dagger$",
        ha="center", va="center",
        fontsize=25, color=FG,
    )
    ax.text(
        0.755, 0.418,
        "creation",
        ha="center", va="center",
        fontsize=SMALL_SIZE, color=RED,
    )

    # -------------------------------------------------------------------------
    # Equal Alice / Bob boxes
    # -------------------------------------------------------------------------

    box_y = 0.075
    box_h = 0.265
    box_w = 0.38
    alice_x = 0.055
    bob_x = 0.565

    rounded_box(ax, alice_x, box_y, box_w, box_h, BLUE)
    rounded_box(ax, bob_x, box_y, box_w, box_h, RED)

    # Box headings are inside the boxes only — no duplicate Alice/Bob labels.
    ax.text(
        alice_x + box_w / 2, box_y + 0.222,
        "Alice",
        ha="center", va="center",
        fontsize=COLUMN_SIZE, color=FG,
    )
    ax.text(
        bob_x + box_w / 2, box_y + 0.222,
        "Bob",
        ha="center", va="center",
        fontsize=COLUMN_SIZE, color=FG,
    )

    # Alice: three well-separated lines.
    ax.text(
        alice_x + box_w / 2, box_y + 0.158,
        r"$\hat N_A=\hat a^\dagger\hat a$",
        ha="center", va="center",
        fontsize=EQ_SIZE - 2, color=FG,
    )
    ax.text(
        alice_x + box_w / 2, box_y + 0.095,
        r"$\langle0_A|\hat N_A|0_A\rangle=0$",
        ha="center", va="center",
        fontsize=EQ_SIZE - 3, color=BLUE,
    )
    ax.text(
        alice_x + box_w / 2, box_y + 0.038,
        "vacuum",
        ha="center", va="center",
        fontsize=SMALL_SIZE, color=MUTED,
    )

    # Bob: three well-separated lines.
    ax.text(
        bob_x + box_w / 2, box_y + 0.158,
        r"$\hat N_B=\hat b^\dagger\hat b$",
        ha="center", va="center",
        fontsize=EQ_SIZE - 2, color=FG,
    )
    ax.text(
        bob_x + box_w / 2, box_y + 0.095,
        r"$\langle0_A|\hat N_B|0_A\rangle"
        r"=|\beta|^2$",
        ha="center", va="center",
        fontsize=EQ_SIZE - 4, color=RED,
    )
    ax.text(
        bob_x + box_w / 2, box_y + 0.038,
        r"$|\beta|^2="
        r"\frac{1}{e^{2\pi c\Omega/a}-1}$",
        ha="center", va="center",
        fontsize=EQ_SIZE - 3, color=FG,
    )

    fig.savefig(
        OUTPUT_PATH,
        dpi=DPI,
        bbox_inches="tight",
        pad_inches=0.12,
        facecolor=BG,
    )
    plt.close(fig)

    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

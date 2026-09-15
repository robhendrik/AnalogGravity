#!/usr/bin/env python3
"""
generate_appendix_exponential_textbook.py

Appendix — Where does the exponential come from?

A deliberately textbook-like derivation:
- short explanatory sentences
- equations
- no boxes
- no arrows
- no accent colors
- no decorative flow-chart elements

Output:
    Appendix_exponential.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = SCRIPT_DIR / "Appendix_exponential.png"

BG = "#090b10"
FG = "#eef2f7"
MUTED = "#b2bac5"

FIGSIZE = (8.5, 10.0)
DPI = 190

TITLE_SIZE = 19
TEXT_SIZE = 12.5
EQ_SIZE = 17
FINAL_EQ_SIZE = 19


def configure_style() -> None:
    mpl.rcParams.update(
        {
            "figure.facecolor": BG,
            "axes.facecolor": BG,
            "savefig.facecolor": BG,
            "text.color": FG,
            "font.size": TEXT_SIZE,
            "mathtext.fontset": "dejavusans",
        }
    )


def sentence(ax: plt.Axes, y: float, text: str) -> None:
    """Draw a short left-aligned explanatory sentence."""
    ax.text(
        0.10,
        y,
        text,
        ha="left",
        va="center",
        fontsize=TEXT_SIZE,
        color=MUTED,
    )


def equation(
    ax: plt.Axes,
    y: float,
    text: str,
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
        color=FG,
    )


def main() -> None:
    configure_style()

    fig, ax = plt.subplots(figsize=FIGSIZE, facecolor=BG)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)
    ax.axis("off")

    # # Title
    # ax.text(
    #     0.50,
    #     0.955,
    #     "Where Does The Exponential Come From?",
    #     ha="center",
    #     va="center",
    #     fontsize=TITLE_SIZE,
    #     color=FG,
    # )

    # 1. Infinitesimal boost
    sentence(
        ax,
        0.895,
        "For constant proper acceleration, each small step is a Lorentz boost:",
    )

    equation(
        ax,
        0.850,
        r"$v+dv=\frac{v+du}{1+v\,du/c^2},"
        r"\qquad du=a\,d\tau.$",
    )

    # 2. Differential equation
    sentence(
        ax,
        0.785,
        "Keeping only first-order terms gives",
    )

    equation(
        ax,
        0.740,
        r"$\frac{dv}{d\tau}"
        r"=a\left(1-\frac{v^2}{c^2}\right).$",
    )

    # 3. Integrate
    sentence(
        ax,
        0.675,
        r"Integrating, with $v=0$ at $\tau=0$,",
    )

    equation(
        ax,
        0.630,
        r"$\frac{v}{c}"
        r"=\tanh\!\left(\frac{a\tau}{c}\right).$",
    )

    # 4. Trajectory
    sentence(
        ax,
        0.565,
        r"Using $dt/d\tau=\gamma$ and $dx/d\tau=v\gamma$ then gives",
    )

    equation(
        ax,
        0.515,
        r"$t(\tau)=\frac{c}{a}"
        r"\sinh\!\left(\frac{a\tau}{c}\right),"
        r"\qquad"
        r"x(\tau)=\frac{c^2}{a}"
        r"\cosh\!\left(\frac{a\tau}{c}\right).$",
    )

    # 5. Light-cone coordinate
    sentence(
        ax,
        0.440,
        r"For a right-moving wave, the phase depends only on $t-x/c$:",
    )

    equation(
        ax,
        0.390,
        r"$t-\frac{x}{c}"
        r"=\frac{c}{a}"
        r"\left["
        r"\sinh\!\left(\frac{a\tau}{c}\right)"
        r"-"
        r"\cosh\!\left(\frac{a\tau}{c}\right)"
        r"\right].$",
        fontsize=EQ_SIZE - 1,
    )

    sentence(
        ax,
        0.320,
        r"Since $\sinh\eta-\cosh\eta=-e^{-\eta}$,",
    )

    equation(
        ax,
        0.270,
        r"$t-\frac{x}{c}"
        r"=-\frac{c}{a}e^{-a\tau/c}.$",
        fontsize=FINAL_EQ_SIZE,
    )

    # 6. Wave phase
    sentence(
        ax,
        0.195,
        "Therefore Alice's single-frequency wave becomes",
    )

    equation(
        ax,
        0.140,
        r"$e^{-i\omega(t-x/c)}"
        r"\;\longrightarrow\;"
        r"\exp\!\left["
        r"i\frac{\omega c}{a}e^{-a\tau/c}"
        r"\right].$",
        fontsize=FINAL_EQ_SIZE - 1,
    )

    sentence(
        ax,
        0.070,
        "For Bob, the phase is an exponential chirp in proper time.",
    )

    fig.savefig(
        OUTPUT_PATH,
        dpi=DPI,
        bbox_inches="tight",
        pad_inches=0.18,
        facecolor=BG,
    )
    plt.close(fig)

    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

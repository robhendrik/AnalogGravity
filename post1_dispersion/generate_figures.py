#!/usr/bin/env python3
"""
generate_figures.py

Generate the figures and animations for:

    The Speeds of Light — How Dispersion Connects Rainbows to Hawking Radiation

The script changes the current working directory to:

    post1_dispersion/

and writes all output to:

    post1_dispersion/figures/

Outputs
-------
figure_1.png / .gif / .mp4
    Nondispersive packet: v_group = v_phase.

figure_2.png / .gif / .mp4
    2x2 comparison:
      v_group < v_phase
      v_group > v_phase
    with the corresponding dispersion curves below.

figure_3.png / .gif / .mp4
    Moving water shown simultaneously in the lab and co-moving views.
    The flow speed sweeps through zero.

figure_4.png
    Static water-wave dispersion construction with three allowed modes.

Requirements
------------
numpy
matplotlib
pillow          # for GIF export
ffmpeg          # optional, for MP4 export

Run from the directory containing post1_dispersion/:

    python generate_figures.py

Optional:

    python generate_figures.py --only 3
    python generate_figures.py --no-mp4
    python generate_figures.py --no-gif
    python generate_figures.py --fps 30
"""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
import numpy as np


# =============================================================================
# CHANGE CWD TO THE ARTICLE DIRECTORY
# =============================================================================

POST_DIR_NAME = "post1_dispersion"

if Path.cwd().name != POST_DIR_NAME:
    post_dir = Path.cwd() / POST_DIR_NAME
    if not post_dir.is_dir():
        raise FileNotFoundError(
            f"Expected to find '{POST_DIR_NAME}' below the current directory:\n"
            f"    {Path.cwd()}\n\n"
            f"Run this script from the parent directory of '{POST_DIR_NAME}', "
            f"or from '{POST_DIR_NAME}' itself."
        )
    os.chdir(post_dir)

OUTPUT_DIR = Path("figures")


# =============================================================================
# GLOBAL SETTINGS
# =============================================================================

FIGSIZE = (12, 6.5)
FIGSIZE_2X2 = (12, 9.0)

DPI = 160
FPS = 24

# Keep the apparent animation speed consistent between figures.
#
# Earlier Figure 2 used 15 physical time units in 6 seconds of animation:
# 15 / 6 = 2.5 physical time units per displayed second.
#
# We preserve that mapping even when an animation is made longer so packets
# can leave the frame completely before the loop restarts.
TIME_UNITS_PER_VIDEO_SECOND = 2.5

BG = "#090b10"
FG = "#eef2f7"
MUTED = "#8e9aaa"
GRID = "#27303a"

BLUE = "#57a6ff"
CYAN = "#52e0e0"
ORANGE = "#ffad5c"
RED = "#ff6b70"
PURPLE = "#c38cff"
WHITE = "#ffffff"

LINEWIDTH = 3.0
G = 9.81


def configure_style() -> None:
    """Set the common visual style."""
    mpl.rcParams.update(
        {
            "figure.figsize": FIGSIZE,
            "figure.facecolor": BG,
            "axes.facecolor": BG,
            "savefig.facecolor": BG,
            "text.color": FG,
            "axes.labelcolor": FG,
            "axes.edgecolor": MUTED,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "font.size": 15,
            "axes.titlesize": 18,
            "axes.labelsize": 15,
            "xtick.labelsize": 11,
            "ytick.labelsize": 11,
            "legend.fontsize": 11,
            "animation.embed_limit": 100,
        }
    )


def style_axes(ax, *, grid: bool = False) -> None:
    """Apply shared axis styling."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.spines["bottom"].set_color(MUTED)

    if grid:
        ax.grid(True, alpha=0.28, linewidth=0.8, color=GRID)


def number_of_frames(duration: float, fps: int) -> int:
    """
    Return a frame count that preserves the same apparent animation speed.
    """
    video_seconds = duration / TIME_UNITS_PER_VIDEO_SECOND
    return max(2, int(np.ceil(video_seconds * fps)))


def save_png(fig, number: int) -> None:
    """Save a static PNG."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"figure_{number}.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=0.12)
    print(f"saved {path}")


def save_animation(
    anim,
    number: int,
    fps: int,
    make_gif: bool,
    make_mp4: bool,
) -> None:
    """Save GIF and/or MP4 versions of an animation."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if make_gif:
        gif_path = OUTPUT_DIR / f"figure_{number}.gif"
        anim.save(gif_path, writer=PillowWriter(fps=fps), dpi=95)
        print(f"saved {gif_path}")

    if make_mp4:
        mp4_path = OUTPUT_DIR / f"figure_{number}.mp4"

        if shutil.which("ffmpeg") is None:
            print(f"skipped {mp4_path}  [ffmpeg not found]")
        else:
            writer = FFMpegWriter(
                fps=fps,
                codec="libx264",
                bitrate=2600,
                extra_args=["-pix_fmt", "yuv420p"],
            )
            anim.save(mp4_path, writer=writer, dpi=110)
            print(f"saved {mp4_path}")


# =============================================================================
# ROOT FINDING FOR GRAPHICAL DISPERSION CONSTRUCTIONS
# =============================================================================

def roots_from_samples(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Locate zero crossings in sampled data using linear interpolation.
    """
    idx = np.where(y[:-1] * y[1:] < 0.0)[0]
    roots = []

    for j in idx:
        x0, x1 = x[j], x[j + 1]
        y0, y1 = y[j], y[j + 1]
        roots.append(x0 - y0 * (x1 - x0) / (y1 - y0))

    return np.asarray(roots)


# =============================================================================
# FIGURE 1 — NONDISPERSIVE PACKET
# =============================================================================

def figure_1(fps: int, make_gif: bool, make_mp4: bool) -> None:
    """
    Animate a narrow-band packet in a nondispersive medium.

    The wave uses the same blue carrier / white envelope styling as Figure 2.
    The packet enters from fully outside the left edge, crosses the frame,
    disappears fully beyond the right edge, and only then loops.
    """
    x = np.linspace(-10.0, 10.0, 1600)

    c = 1.0
    k0 = 6.5
    sigma = 1.65

    x_start = -10.0 - 4.5 * sigma
    x_end = +10.0 + 4.5 * sigma

    duration = (x_end - x_start) / c
    n_frames = number_of_frames(duration, fps)
    times = np.linspace(0.0, duration, n_frames, endpoint=False)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    style_axes(ax)

    ax.set_xlim(-10, 10)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xlabel("position")
    ax.set_ylabel("displacement")
    ax.set_yticks([-1, 0, 1])
    ax.set_title(
        r"$v_{\mathrm{group}} = v_{\mathrm{phase}}$",
        loc="center",
    )
    ax.axhline(0.0, color=MUTED, alpha=0.35, lw=1.0)

    # Same styling as the wave panels in Figure 2.
    line, = ax.plot([], [], color=BLUE, lw=2.5)
    envelope_top, = ax.plot([], [], color=WHITE, lw=1.15, alpha=0.50)
    envelope_bottom, = ax.plot([], [], color=WHITE, lw=1.15, alpha=0.50)

    def field(t: float):
        xc = x_start + c * t
        envelope = np.exp(-0.5 * ((x - xc) / sigma) ** 2)
        y = envelope * np.cos(k0 * (x - xc))
        return y, envelope

    def update(i: int):
        y, envelope = field(times[i])

        line.set_data(x, y)
        envelope_top.set_data(x, envelope)
        envelope_bottom.set_data(x, -envelope)

        return line, envelope_top, envelope_bottom

    update(int(0.50 * len(times)))
    save_png(fig, 1)

    anim = FuncAnimation(
        fig,
        update,
        frames=len(times),
        interval=1000 / fps,
        blit=False,
    )
    save_animation(anim, 1, fps, make_gif, make_mp4)

    plt.close(fig)


# =============================================================================
# FIGURE 2 — PHASE VELOCITY VS GROUP VELOCITY
# =============================================================================

def omega_sublinear(k: np.ndarray) -> np.ndarray:
    """
    Concave dispersion curve with v_group < v_phase near the carrier.
    """
    return 1.20 * k - 0.055 * k**2


def domega_sublinear(k: np.ndarray) -> np.ndarray:
    return 1.20 - 0.110 * k


def omega_superlinear(k: np.ndarray) -> np.ndarray:
    """
    Convex dispersion curve with v_group > v_phase near the carrier.
    """
    return 0.48 * k + 0.075 * k**2


def domega_superlinear(k: np.ndarray) -> np.ndarray:
    return 0.48 + 0.150 * k


def figure_2(fps: int, make_gif: bool, make_mp4: bool) -> None:
    """
    2x2 figure.

    Top:
        left  — v_group < v_phase
        right — v_group > v_phase

    Bottom:
        corresponding dispersion curves.

    The tangent is shown only as a short local line segment centered on the
    carrier point. The old secant from the origin is intentionally omitted.
    """
    x = np.linspace(-12.0, 12.0, 1600)
    k_plot = np.linspace(0.0, 6.5, 800)

    k0 = 4.0
    sigma = 2.4

    omega0_left = float(omega_sublinear(np.array([k0]))[0])
    vp_left = omega0_left / k0
    vg_left = float(domega_sublinear(np.array([k0]))[0])

    omega0_right = float(omega_superlinear(np.array([k0]))[0])
    vp_right = omega0_right / k0
    vg_right = float(domega_superlinear(np.array([k0]))[0])

    velocity_scale = 1.15
    vp_left *= velocity_scale
    vg_left *= velocity_scale
    vp_right *= velocity_scale
    vg_right *= velocity_scale

    # Both packets start completely outside the left-hand side.
    x_start = -12.0 - 4.5 * sigma
    x_end = +12.0 + 4.5 * sigma

    # Keep the same apparent speed as before.  Use the slower envelope to
    # determine when the animation can safely loop.
    slowest_vg = min(vg_left, vg_right)
    duration = (x_end - x_start) / slowest_vg
    n_frames = number_of_frames(duration, fps)
    times = np.linspace(0.0, duration, n_frames, endpoint=False)

    fig, axes = plt.subplots(
        2,
        2,
        figsize=FIGSIZE_2X2,
        gridspec_kw={"height_ratios": [1.15, 1.0]},
    )

    ax_wave_left = axes[0, 0]
    ax_wave_right = axes[0, 1]
    ax_disp_left = axes[1, 0]
    ax_disp_right = axes[1, 1]

    for ax in (ax_wave_left, ax_wave_right):
        style_axes(ax)
        ax.set_xlim(-12, 12)
        ax.set_ylim(-1.18, 1.18)
        ax.set_xlabel("position")
        ax.set_ylabel("amplitude")
        ax.set_yticks([-1, 0, 1])
        ax.axhline(0.0, color=MUTED, alpha=0.30, lw=1.0)

    ax_wave_left.set_title(
        r"$v_{\mathrm{group}} < v_{\mathrm{phase}}$"
    )
    ax_wave_right.set_title(
        r"$v_{\mathrm{group}} > v_{\mathrm{phase}}$"
    )

    wave_left, = ax_wave_left.plot([], [], color=BLUE, lw=2.5)
    env_left_top, = ax_wave_left.plot([], [], color=WHITE, lw=1.15, alpha=0.50)
    env_left_bottom, = ax_wave_left.plot([], [], color=WHITE, lw=1.15, alpha=0.50)

    wave_right, = ax_wave_right.plot([], [], color=BLUE, lw=2.5)
    env_right_top, = ax_wave_right.plot([], [], color=WHITE, lw=1.15, alpha=0.50)
    env_right_bottom, = ax_wave_right.plot([], [], color=WHITE, lw=1.15, alpha=0.50)

    # Dispersion panels --------------------------------------------------------
    for ax in (ax_disp_left, ax_disp_right):
        style_axes(ax)
        ax.set_xlim(0.0, 6.5)
        ax.set_xlabel("$k$")
        ax.set_ylabel("$\\omega$")
        ax.set_xticks([0, k0, 6])
        ax.set_xticklabels(["0", "$k_0$", ""])
        ax.set_yticks([])

    w_left = omega_sublinear(k_plot)
    w_right = omega_superlinear(k_plot)

    ax_disp_left.plot(k_plot, w_left, color=ORANGE, lw=LINEWIDTH)
    ax_disp_right.plot(k_plot, w_right, color=ORANGE, lw=LINEWIDTH)

    # Short tangent segments centered on the touch point.
    tangent_half_width = 1.05
    k_tangent = np.linspace(
        k0 - tangent_half_width,
        k0 + tangent_half_width,
        120,
    )

    tangent_left = (
        omega0_left
        + domega_sublinear(np.array([k0]))[0] * (k_tangent - k0)
    )
    tangent_right = (
        omega0_right
        + domega_superlinear(np.array([k0]))[0] * (k_tangent - k0)
    )

    ax_disp_left.plot(
        k_tangent,
        tangent_left,
        color=PURPLE,
        lw=1.8,
        alpha=0.95,
    )
    ax_disp_right.plot(
        k_tangent,
        tangent_right,
        color=PURPLE,
        lw=1.8,
        alpha=0.95,
    )

    ax_disp_left.plot(
        [k0], [omega0_left],
        "o", color=WHITE, ms=8, mec=BG, mew=1.2,
    )
    ax_disp_right.plot(
        [k0], [omega0_right],
        "o", color=WHITE, ms=8, mec=BG, mew=1.2,
    )

    ymax = max(np.nanmax(w_left), np.nanmax(w_right)) * 1.08
    ax_disp_left.set_ylim(0.0, ymax)
    ax_disp_right.set_ylim(0.0, ymax)

    # Minimal mathematical labels, placed on opposite sides of the point.
    for ax, omega0, deriv in (
        (ax_disp_left, omega0_left, domega_sublinear(np.array([k0]))[0]),
        (ax_disp_right, omega0_right, domega_superlinear(np.array([k0]))[0]),
    ):
        y_left = omega0 + deriv * (-0.78)
        y_right = omega0 + deriv * (+0.78)

        ax.text(
            k0 - 0.88,
            y_left + 0.26,
            r"$v_{\mathrm{group}}=\dfrac{d\omega}{dk}$",
            color=PURPLE,
            fontsize=12,
            ha="right",
            va="bottom",
        )
        ax.text(
            k0 + 0.62,
            y_right - 0.32,
            r"$v_{\mathrm{phase}}=\dfrac{\omega}{k}$",
            color=CYAN,
            fontsize=12,
            ha="left",
            va="top",
        )

    # Animation ---------------------------------------------------------------
    def packet(t: float, vp: float, vg: float):
        xc = x_start + vg * t
        envelope = np.exp(-0.5 * ((x - xc) / sigma) ** 2)

        phase = k0 * (x - x_start - vp * t)
        y = envelope * np.cos(phase)

        return y, envelope

    def update(i: int):
        t = times[i]

        y_l, e_l = packet(t, vp_left, vg_left)
        y_r, e_r = packet(t, vp_right, vg_right)

        wave_left.set_data(x, y_l)
        env_left_top.set_data(x, e_l)
        env_left_bottom.set_data(x, -e_l)

        wave_right.set_data(x, y_r)
        env_right_top.set_data(x, e_r)
        env_right_bottom.set_data(x, -e_r)

        return (
            wave_left,
            env_left_top,
            env_left_bottom,
            wave_right,
            env_right_top,
            env_right_bottom,
        )

    fig.tight_layout(h_pad=2.0, w_pad=2.2)

    # Representative still while both packets are visible.
    target_x = 0.0
    still_t = (target_x - x_start) / slowest_vg
    still_i = int(np.argmin(np.abs(times - still_t)))
    update(still_i)
    save_png(fig, 2)

    anim = FuncAnimation(
        fig,
        update,
        frames=len(times),
        interval=1000 / fps,
        blit=False,
    )
    save_animation(anim, 2, fps, make_gif, make_mp4)

    plt.close(fig)


# =============================================================================
# WATER-WAVE DISPERSION USED IN FIGURES 3 AND 4
# =============================================================================

def signed_water_omega(
    k: np.ndarray,
    h: float = 0.18,
    g: float = G,
) -> np.ndarray:
    """
    Signed intrinsic gravity-wave dispersion in the co-moving frame.

        Omega(k)^2 = g |k| tanh(|k| h)

    We plot the odd extension

        Omega(k) = sign(k) sqrt(g |k| tanh(|k| h))

    Surface tension is omitted.
    """
    q = np.abs(k)
    omega_abs = np.sqrt(g * q * np.tanh(q * h))
    return np.sign(k) * omega_abs


# =============================================================================
# FIGURE 3 — LAB FRAME VS CO-MOVING FRAME
# =============================================================================

def figure_3(fps: int, make_gif: bool, make_mp4: bool) -> None:
    """
    Same moving-water modes in two equivalent graphical views.

    LEFT — lab frame
        omega_0 is horizontal and conserved.
        The lab-frame dispersion changes with flow:

            omega(k) = Omega(k) + u k

    RIGHT — co-moving frame
        the intrinsic dispersion Omega(k) stays fixed.
        The same conserved lab frequency is the tilted line:

            Omega = omega_0 - u k

        The flow speed starts at zero, becomes increasingly negative,
    passes just beyond the tangency where the additional roots appear,
    and then returns to zero.
    """
    h = 0.18
    omega0 = 0.80

    k_limit = 14.0
    y_limit = 16.0

    k = np.linspace(-k_limit, k_limit, 6000)
    Omega = signed_water_omega(k, h=h)

    # For h = 0.18 and omega0 = 0.80, the tangency occurs at
    # approximately u = -1.031 m/s. Go slightly beyond it so the
    # transition from one to three real modes is clearly visible.
    u_min = -1.08

    # Smooth loop:
    #   zero flow -> beyond tangency -> zero flow
    half_frames = 120
    u_down = np.linspace(0.0, u_min, half_frames, endpoint=False)
    u_up = np.linspace(u_min, 0.0, half_frames)
    u_values = np.concatenate([u_down, u_up])

    fig, (ax_lab, ax_comoving) = plt.subplots(1, 2, figsize=(13.2, 6.4))

    # LEFT: lab frame ---------------------------------------------------------
    style_axes(ax_lab, grid=True)
    ax_lab.set_xlim(-k_limit, k_limit)
    ax_lab.set_ylim(-y_limit, y_limit)
    ax_lab.set_xlabel("$k$")
    ax_lab.set_ylabel("$\\omega$")
    ax_lab.set_title("Lab frame")

    lab_curve, = ax_lab.plot([], [], color=BLUE, lw=LINEWIDTH)
    ax_lab.axhline(omega0, color=RED, lw=2.2)
    ax_lab.axhline(0.0, color=MUTED, lw=1.0, alpha=0.45)
    ax_lab.axvline(0.0, color=MUTED, lw=1.0, alpha=0.45)

    lab_points, = ax_lab.plot(
        [], [], "o",
        color=WHITE,
        ms=9,
        mec=BG,
        mew=1.3,
    )

    lab_flow_text = ax_lab.text(
        0.04, 0.94, "",
        transform=ax_lab.transAxes,
        ha="left", va="top",
        fontsize=13,
        color=FG,
    )

    # RIGHT: co-moving frame --------------------------------------------------
    style_axes(ax_comoving, grid=True)
    ax_comoving.set_xlim(-k_limit, k_limit)
    ax_comoving.set_ylim(-y_limit, y_limit)
    ax_comoving.set_xlabel("$k$")
    ax_comoving.set_ylabel("$\\Omega$")
    ax_comoving.set_title("Co-moving frame")

    ax_comoving.plot(k, Omega, color=BLUE, lw=LINEWIDTH)
    tilted_line, = ax_comoving.plot([], [], color=RED, lw=2.2)
    ax_comoving.axhline(0.0, color=MUTED, lw=1.0, alpha=0.45)
    ax_comoving.axvline(0.0, color=MUTED, lw=1.0, alpha=0.45)

    comoving_points, = ax_comoving.plot(
        [], [], "o",
        color=WHITE,
        ms=9,
        mec=BG,
        mew=1.3,
    )

    comoving_flow_text = ax_comoving.text(
        0.04, 0.94, "",
        transform=ax_comoving.transAxes,
        ha="left", va="top",
        fontsize=13,
        color=FG,
    )

    def update(i: int):
        u = u_values[i]

        # Lab-frame dispersion.
        omega_lab = Omega + u * k
        lab_curve.set_data(k, omega_lab)

        # Co-moving-frame representation of the same fixed lab frequency.
        omega_line_comoving = omega0 - u * k
        tilted_line.set_data(k, omega_line_comoving)

        # Same k roots in both panels.
        roots = roots_from_samples(k, omega_lab - omega0)

        lab_points.set_data(
            roots,
            np.full_like(roots, omega0),
        )

        comoving_points.set_data(
            roots,
            np.interp(roots, k, Omega),
        )

        flow_label = rf"$u={u:+.2f}\ \mathrm{{m\,s^{{-1}}}}$"
        lab_flow_text.set_text(flow_label)
        comoving_flow_text.set_text(flow_label)

        return (
            lab_curve,
            lab_points,
            tilted_line,
            comoving_points,
            lab_flow_text,
            comoving_flow_text,
        )

    fig.tight_layout(w_pad=2.0)

    # Save the still close to u = -1 m/s, where three roots are visible.
    still_i = int(np.argmin(np.abs(u_values - (-1.0))))
    update(still_i)
    save_png(fig, 3)

    anim = FuncAnimation(
        fig,
        update,
        frames=len(u_values),
        interval=1000 / fps,
        blit=False,
    )
    save_animation(anim, 3, fps, make_gif, make_mp4)

    plt.close(fig)


# =============================================================================
# FIGURE 4 — THREE POSSIBLE MODES AT ONE LAB FREQUENCY
# =============================================================================

def figure_4() -> None:
    """
    Static graphical mode construction with three real crossings.

    Parameters are chosen so the interesting parts of the full water-wave
    dispersion remain inside the visible frame.
    """
    h = 0.18
    omega0 = 0.80
    u = -1.00

    k_limit = 14.0
    y_limit = 16.0

    k = np.linspace(-k_limit, k_limit, 8000)
    Omega = signed_water_omega(k, h=h)
    doppler_line = omega0 - u * k

    roots = roots_from_samples(k, Omega - doppler_line)
    root_values = np.interp(roots, k, Omega)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    style_axes(ax, grid=True)

    ax.set_xlim(-k_limit, k_limit)
    ax.set_ylim(-y_limit, y_limit)
    ax.set_xlabel("$k$")
    ax.set_ylabel("$\\Omega$")

    ax.plot(k, Omega, color=BLUE, lw=LINEWIDTH)
    ax.plot(k, doppler_line, color=RED, lw=2.3)

    ax.axhline(0.0, color=MUTED, lw=1.0, alpha=0.45)
    ax.axvline(0.0, color=MUTED, lw=1.0, alpha=0.45)

    ax.plot(
        roots,
        root_values,
        "o",
        color=WHITE,
        ms=10,
        mec=BG,
        mew=1.4,
        zorder=5,
    )

    ax.text(
        0.04,
        0.94,
        rf"$u={u:+.2f}\ \mathrm{{m\,s^{{-1}}}}$",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=13,
        color=FG,
    )

    labels = [r"$k_1$", r"$k_2$", r"$k_3$"]
    offsets = [(-0.45, 0.75), (-0.25, 0.75), (0.35, 0.75)]

    for root, value, label, (dx, dy) in zip(
        roots, root_values, labels, offsets
    ):
        ax.text(
            root + dx,
            value + dy,
            label,
            color=FG,
            fontsize=14,
            ha="center",
        )

    save_png(fig, 4)
    plt.close(fig)


# =============================================================================
# MAIN
# =============================================================================

FIGURE_FUNCTIONS = {
    1: figure_1,
    2: figure_2,
    3: figure_3,
    4: figure_4,
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate all dispersion-post figures."
    )

    parser.add_argument(
        "--only",
        type=int,
        choices=sorted(FIGURE_FUNCTIONS),
        help="Generate one figure only.",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=FPS,
        help=f"Animation FPS (default: {FPS}).",
    )
    parser.add_argument(
        "--no-gif",
        action="store_true",
        help="Do not write GIF files.",
    )
    parser.add_argument(
        "--no-mp4",
        action="store_true",
        help="Do not write MP4 files.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    configure_style()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    make_gif = not args.no_gif
    make_mp4 = not args.no_mp4

    numbers = (
        [args.only]
        if args.only is not None
        else sorted(FIGURE_FUNCTIONS)
    )

    for number in numbers:
        print(f"\n--- figure {number} ---")

        if number == 4:
            figure_4()
        else:
            FIGURE_FUNCTIONS[number](
                args.fps,
                make_gif,
                make_mp4,
            )

    print(f"\nDone. Output directory: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
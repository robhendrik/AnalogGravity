#!/usr/bin/env python3
"""
generate_figures.py

Generate the figures and animations for:

    The Speeds of Light — How Dispersion Connects Rainbows to Hawking Radiation

Outputs:
    figures/figure_1.png
    figures/figure_2.png / .gif / .mp4
    figures/figure_3.png / .gif / .mp4
    figures/figure_4.png / .gif / .mp4
    figures/figure_5.png
    figures/figure_6.png / .gif / .mp4
    figures/figure_7.png / .gif / .mp4

The script uses Matplotlib only. GIF export requires Pillow.
MP4 export requires an ffmpeg executable visible to Matplotlib.

Run:
    python generate_figures.py

Optional:
    python generate_figures.py --no-mp4
    python generate_figures.py --no-gif
    python generate_figures.py --only 6
    python generate_figures.py --fps 24
"""

from __future__ import annotations

import argparse
import math
import shutil
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
import numpy as np


# =============================================================================
# GLOBAL SETTINGS
# =============================================================================

OUTPUT_DIR = Path("figures")

FIGSIZE = (12, 6.5)
DPI = 160
FPS = 24
N_FRAMES = 144

BG = "#090b10"
FG = "#eef2f7"
MUTED = "#8e9aaa"
GRID = "#27303a"

BLUE = "#57a6ff"
CYAN = "#52e0e0"
ORANGE = "#ffad5c"
RED = "#ff6b70"
GREEN = "#7ddc82"
PURPLE = "#c38cff"
YELLOW = "#f6df6b"
WHITE = "#ffffff"

LINEWIDTH = 3.0
THIN = 1.5

G = 9.81


def configure_style() -> None:
    """Set the common publication style."""
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
            "axes.titlesize": 20,
            "axes.labelsize": 16,
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
            "legend.fontsize": 12,
            "animation.embed_limit": 80,
        }
    )


def style_axes(ax, *, grid=False) -> None:
    """Apply shared axis styling."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.spines["bottom"].set_color(MUTED)
    if grid:
        ax.grid(True, alpha=0.32, linewidth=0.8, color=GRID)


def save_png(fig, number: int) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"figure_{number}.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=0.16)
    print(f"saved {path}")


def save_animation(anim, number: int, fps: int, make_gif: bool, make_mp4: bool) -> None:
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
                bitrate=2400,
                extra_args=["-pix_fmt", "yuv420p"],
            )
            anim.save(mp4_path, writer=writer, dpi=110)
            print(f"saved {mp4_path}")


def phase_wrap(frac: float) -> float:
    """Smooth 0..1 periodic phase."""
    return 2.0 * np.pi * frac


# =============================================================================
# FIGURE 1 — A PRISM: DIFFERENT COLOURS, DIFFERENT SPEEDS
# =============================================================================

def figure_1() -> None:
    """
    Static conceptual prism figure.

    The geometry is illustrative rather than a full Snell-law ray tracer. The
    point is simply that a material can assign different phase velocities /
    refractive indices to different frequencies.
    """
    fig, ax = plt.subplots()
    ax.set_xlim(0, 12)
    ax.set_ylim(-4.0, 4.0)
    ax.set_aspect("equal")
    ax.axis("off")

    # Prism
    prism = np.array([[5.0, -3.1], [7.4, 0.0], [5.0, 3.1], [5.0, -3.1]])
    ax.fill(prism[:, 0], prism[:, 1], facecolor="#9fc8de", alpha=0.18)
    ax.plot(prism[:, 0], prism[:, 1], color=FG, alpha=0.75, lw=2.0)

    # Incident white ray
    ax.plot([0.7, 5.0], [0, 0], lw=8, color=WHITE, solid_capstyle="round")
    ax.annotate(
        "",
        xy=(4.95, 0), xytext=(3.9, 0),
        arrowprops=dict(arrowstyle="-|>", lw=2.5, color=WHITE),
    )

    # Inside ray
    ax.plot([5.0, 7.4], [0, 0], lw=5, color=WHITE, alpha=0.68)

    colors = [
        ("red", RED, 1.10),
        ("orange", ORANGE, 0.72),
        ("green", GREEN, 0.24),
        ("blue", BLUE, -0.42),
        ("violet", PURPLE, -0.96),
    ]
    for label, color, y_end in colors:
        ax.plot([7.4, 11.3], [0, y_end], color=color, lw=4, solid_capstyle="round")
        ax.text(11.45, y_end, label, va="center", ha="left", color=color, fontsize=13)

    ax.text(
        0.7, 2.9,
        "Dispersion starts with a simple surprise",
        fontsize=23, fontweight="bold", ha="left"
    )
    ax.text(
        0.7, 2.25,
        "the medium gives different frequencies different wave speeds",
        fontsize=15, color=MUTED, ha="left"
    )
    ax.text(
        6.1, -3.65,
        "one material  →  a family of speeds",
        fontsize=15, ha="center", color=FG
    )

    save_png(fig, 1)
    plt.close(fig)


# =============================================================================
# FIGURE 2 — CONTINUOUS ROPE: A PACKET THAT KEEPS ITS SHAPE
# =============================================================================

def figure_2(fps: int, make_gif: bool, make_mp4: bool) -> None:
    """Animate a narrow-band packet in a nondispersive medium."""
    x = np.linspace(-10, 10, 1400)
    c = 1.0
    k0 = 7.0
    sigma = 2.0

    fig, ax = plt.subplots()
    style_axes(ax)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-1.25, 1.25)
    ax.set_xlabel("position")
    ax.set_ylabel("displacement")
    ax.set_yticks([-1, 0, 1])
    ax.set_title("A continuous rope: every wavelength travels at the same speed", loc="left")

    line, = ax.plot([], [], color=CYAN, lw=2.8)
    envelope_top, = ax.plot([], [], color=MUTED, lw=1.2, alpha=0.7)
    envelope_bottom, = ax.plot([], [], color=MUTED, lw=1.2, alpha=0.7)
    ax.axhline(0, color=MUTED, alpha=0.35, lw=1)

    label = ax.text(
        0.02, 0.92, "", transform=ax.transAxes, color=FG,
        fontsize=15, ha="left", va="top"
    )

    times = np.linspace(0, 9.0, N_FRAMES)

    def field(t):
        xc = -6.2 + c * t
        env = np.exp(-0.5 * ((x - xc) / sigma) ** 2)
        y = env * np.cos(k0 * (x - xc))
        return y, env, xc

    def update(i):
        t = times[i]
        y, env, xc = field(t)
        line.set_data(x, y)
        envelope_top.set_data(x, env)
        envelope_bottom.set_data(x, -env)
        label.set_text(r"$\omega=ck$   →   $v_p=v_g=c$" + f"\npacket centre = {xc:+.1f}")
        return line, envelope_top, envelope_bottom, label

    update(len(times) // 2)
    save_png(fig, 2)

    anim = FuncAnimation(fig, update, frames=len(times), interval=1000 / fps, blit=False)
    save_animation(anim, 2, fps, make_gif, make_mp4)
    plt.close(fig)


# =============================================================================
# FIGURE 3 — BEADS ON A STRING: THE DISPERSION CURVE BENDS
# =============================================================================

def lattice_omega(k, a=1.0, c0=1.0):
    """
    Acoustic branch of a monatomic bead/string lattice.

    Omega = (2 c0 / a) |sin(ka/2)|.
    Near k=0 this tends to c0 |k|.
    """
    return (2.0 * c0 / a) * np.abs(np.sin(0.5 * k * a))


def figure_3(fps: int, make_gif: bool, make_mp4: bool) -> None:
    """Animate a wave packet built from the beaded-string dispersion relation."""
    a = 1.0
    c0 = 1.0
    kmax = np.pi / a

    k = np.linspace(-kmax, kmax, 1800)
    omega = lattice_omega(k, a=a, c0=c0)

    # Spectral packet centered away from k=0 so curvature is visible.
    k0 = 0.67 * kmax
    sigma_k = 0.19
    spectrum = np.exp(-0.5 * ((k - k0) / sigma_k) ** 2)

    x = np.linspace(-22, 22, 1200)
    times = np.linspace(0.0, 30.0, N_FRAMES)

    # Precompute exp(ikx); moderate memory but fast animation.
    E = np.exp(1j * np.outer(k, x))
    dk = k[1] - k[0]

    fig = plt.figure(figsize=FIGSIZE)
    ax = fig.add_axes([0.08, 0.13, 0.62, 0.77])
    axd = fig.add_axes([0.75, 0.56, 0.21, 0.30])

    style_axes(ax)
    style_axes(axd)

    ax.set_xlim(-22, 22)
    ax.set_ylim(-1.15, 1.15)
    ax.set_xlabel("position")
    ax.set_ylabel("displacement")
    ax.set_title("Add a microscopic spacing — and the packet starts to spread", loc="left")
    ax.axhline(0, color=MUTED, alpha=0.3, lw=1)

    line, = ax.plot([], [], color=ORANGE, lw=2.6)

    axd.plot(k, omega, color=ORANGE, lw=2.1)
    marker, = axd.plot([k0], [lattice_omega(np.array([k0]), a, c0)[0]], "o", ms=8, color=WHITE)
    axd.set_xlim(0, kmax)
    axd.set_ylim(0, 2.15)
    axd.set_xlabel("$k$", fontsize=12)
    axd.set_ylabel("$\\omega$", fontsize=12)
    axd.set_title("bent $\\omega(k)$", fontsize=14, loc="left")
    axd.set_xticks([0, np.pi])
    axd.set_xticklabels(["0", "$\\pi/a$"])
    axd.set_yticks([])

    note = ax.text(
        0.73, 0.36,
        r"$v_p=\omega/k$" "\n"
        r"$v_g=d\omega/dk$" "\n\n"
        "Different Fourier components\n"
        "now move at different speeds.",
        transform=ax.transAxes, color=FG, fontsize=14,
        ha="left", va="top",
    )

    def field(t):
        # Real part of Fourier synthesis. Shift initial packet to x=-11.
        phase = np.exp(-1j * omega * t) * np.exp(1j * k * 11.0)
        psi = np.real((spectrum * phase) @ E) * dk
        m = np.max(np.abs(psi))
        if m > 0:
            psi = psi / np.max(np.abs(np.real((spectrum * np.exp(1j * k * 11.0)) @ E) * dk))
        return psi

    def update(i):
        line.set_data(x, field(times[i]))
        return line, marker, note

    update(int(0.62 * len(times)))
    save_png(fig, 3)

    anim = FuncAnimation(fig, update, frames=len(times), interval=1000 / fps, blit=False)
    save_animation(anim, 3, fps, make_gif, make_mp4)
    plt.close(fig)


# =============================================================================
# FIGURE 4 — PHASE VELOCITY VS GROUP VELOCITY
# =============================================================================

def figure_4(fps: int, make_gif: bool, make_mp4: bool) -> None:
    """Show crests moving through a slower wave-packet envelope."""
    x = np.linspace(-14, 14, 1400)
    sigma = 3.0
    k0 = 3.8

    vp = 1.45
    vg = 0.72

    times = np.linspace(0, 12.0, N_FRAMES)

    fig, ax = plt.subplots()
    style_axes(ax)
    ax.set_xlim(-14, 14)
    ax.set_ylim(-1.35, 1.35)
    ax.set_xlabel("position")
    ax.set_ylabel("amplitude")
    ax.set_title("Two velocities hide inside one wave packet", loc="left")
    ax.axhline(0, color=MUTED, alpha=0.3, lw=1)

    carrier, = ax.plot([], [], color=BLUE, lw=2.6)
    env_top, = ax.plot([], [], color=WHITE, alpha=0.55, lw=1.4)
    env_bottom, = ax.plot([], [], color=WHITE, alpha=0.55, lw=1.4)

    phase_dot, = ax.plot([], [], "o", color=ORANGE, ms=9)
    group_dot, = ax.plot([], [], "o", color=CYAN, ms=9)

    ax.text(0.02, 0.92, "orange: one crest (phase)", transform=ax.transAxes, color=ORANGE)
    ax.text(0.02, 0.86, "cyan: packet centre (group)", transform=ax.transAxes, color=CYAN)

    def update(i):
        t = times[i]
        xc = -8.0 + vg * t
        env = np.exp(-0.5 * ((x - xc) / sigma) ** 2)
        y = env * np.cos(k0 * (x - vp * t))

        # One particular crest trajectory, modulo enough periods to keep it near packet.
        crest_x_raw = -8.0 + vp * t
        period = 2 * np.pi / k0
        nshift = np.round((crest_x_raw - xc) / period)
        crest_x = crest_x_raw - nshift * period
        crest_y = np.exp(-0.5 * ((crest_x - xc) / sigma) ** 2)

        carrier.set_data(x, y)
        env_top.set_data(x, env)
        env_bottom.set_data(x, -env)
        phase_dot.set_data([crest_x], [crest_y])
        group_dot.set_data([xc], [0.0])
        return carrier, env_top, env_bottom, phase_dot, group_dot

    update(len(times) // 2)
    save_png(fig, 4)

    anim = FuncAnimation(fig, update, frames=len(times), interval=1000 / fps, blit=False)
    save_animation(anim, 4, fps, make_gif, make_mp4)
    plt.close(fig)


# =============================================================================
# FIGURE 5 — A ZOO OF DISPERSION CURVES
# =============================================================================

def figure_5() -> None:
    """Static montage of representative dispersion relations."""
    fig, ax = plt.subplots()
    style_axes(ax, grid=False)

    k = np.linspace(0, 5.5, 900)

    # Normalized illustrative curves.
    rope = 0.66 * k
    beads = 2.25 * np.sin(np.minimum(k, np.pi) / 2.0)
    beads[k > np.pi] = np.nan
    deep_water = 1.44 * np.sqrt(k)
    massive = 0.18 * k**2 + 0.08

    ax.plot(k, rope, lw=LINEWIDTH, color=CYAN)
    ax.plot(k, beads, lw=LINEWIDTH, color=ORANGE)
    ax.plot(k, deep_water, lw=LINEWIDTH, color=BLUE)
    ax.plot(k, massive, lw=LINEWIDTH, color=PURPLE)

    ax.text(4.7, rope[np.argmin(np.abs(k - 4.7))] + 0.15, "continuous rope", color=CYAN)
    ax.text(2.6, 2.34, "beads on a string", color=ORANGE)
    ax.text(4.0, 3.08, "deep-water waves", color=BLUE)
    ax.text(4.15, 3.75, "massive matter wave", color=PURPLE)

    ax.set_xlim(0, 5.6)
    ax.set_ylim(0, 5.6)
    ax.set_xlabel("wavenumber  $k$")
    ax.set_ylabel("frequency  $\\omega$")
    ax.set_title("A zoo of curves — one graph encodes how a medium carries waves", loc="left")
    ax.set_xticks([])
    ax.set_yticks([])

    ax.text(
        0.02, 0.06,
        "straight line → no dispersion     •     curvature → phase and group velocities separate",
        transform=ax.transAxes, color=MUTED, fontsize=14
    )

    save_png(fig, 5)
    plt.close(fig)


# =============================================================================
# FIGURE 6 — MOVING MEDIUM: DOPPLER TILT OF THE DISPERSION CURVE
# =============================================================================

def signed_water_omega(k: np.ndarray, h: float = 0.35, g: float = G) -> np.ndarray:
    """
    Signed intrinsic gravity-wave dispersion:
        Omega(k) = sign(k) sqrt(g |k| tanh(|k| h))
    Surface tension omitted.
    """
    q = np.abs(k)
    om = np.sqrt(g * q * np.tanh(q * h))
    return np.sign(k) * om


def figure_6(fps: int, make_gif: bool, make_mp4: bool) -> None:
    """
    Animate transformation from comoving dispersion Omega(k) to
    laboratory dispersion omega(k) = Omega(k) + u k.
    """
    k = np.linspace(-10.0, 10.0, 1600)
    Omega = signed_water_omega(k)

    u_values = np.linspace(0.0, -1.55, N_FRAMES)

    fig, ax = plt.subplots()
    style_axes(ax, grid=True)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-7.5, 7.5)
    ax.set_xlabel("wavenumber  $k$")
    ax.set_ylabel("frequency")
    ax.set_title("Move the medium — and the whole dispersion relation tilts", loc="left")

    intrinsic, = ax.plot(k, Omega, color=MUTED, lw=2.0, ls="--", alpha=0.9, label="$\\Omega(k)$")
    lab, = ax.plot([], [], color=CYAN, lw=3.2, label="$\\omega(k)=\\Omega(k)+uk$")
    tangent, = ax.plot([], [], color=ORANGE, lw=1.4, alpha=0.8)

    ax.axhline(0, color=MUTED, lw=1.0, alpha=0.5)
    ax.axvline(0, color=MUTED, lw=1.0, alpha=0.5)

    note = ax.text(
        0.02, 0.93, "", transform=ax.transAxes,
        ha="left", va="top", fontsize=15
    )

    ax.legend(frameon=False, loc="lower right")

    def update(i):
        u = u_values[i]
        omega = Omega + u * k
        lab.set_data(k, omega)
        tangent.set_data(k, u * k)
        note.set_text(
            r"$\Omega=\omega-uk$"
            + f"\nflow speed  u = {u:+.2f}"
            + "\n(dashed: medium at rest)"
        )
        return lab, tangent, note

    update(int(0.72 * len(u_values)))
    save_png(fig, 6)

    anim = FuncAnimation(fig, update, frames=len(u_values), interval=1000 / fps, blit=False)
    save_animation(anim, 6, fps, make_gif, make_mp4)
    plt.close(fig)


# =============================================================================
# FIGURE 7 — FIXED LAB FREQUENCY: ONE OMEGA, SEVERAL K
# =============================================================================

def roots_from_samples(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Locate zero crossings by linear interpolation.

    Good enough for plotting intersections and avoids a SciPy dependency.
    """
    roots = []

    # Exact/nearly exact sampled zeros
    near = np.where(np.abs(y) < 1e-6)[0]
    roots.extend(x[near].tolist())

    idx = np.where(y[:-1] * y[1:] < 0)[0]
    for j in idx:
        x0, x1 = x[j], x[j + 1]
        y0, y1 = y[j], y[j + 1]
        r = x0 - y0 * (x1 - x0) / (y1 - y0)
        roots.append(float(r))

    if not roots:
        return np.array([])

    roots = np.array(sorted(roots))
    keep = np.ones(len(roots), dtype=bool)
    keep[1:] = np.diff(roots) > 1e-3
    return roots[keep]


def figure_7(fps: int, make_gif: bool, make_mp4: bool) -> None:
    """
    Animate Leonhardt/Weinfurtner-style graphical root finding.

    At each frame the intrinsic water-wave dispersion is fixed. Changing the
    flow speed changes the straight Doppler line

        Omega = omega0 - u k

    and the intersections are the allowed wavenumbers at one conserved
    laboratory frequency omega0.

    This is the bridge from ordinary dispersion to horizon mode conversion.
    """
    h = 0.18
    omega0 = 2.1

    k = np.linspace(-18.0, 18.0, 5000)
    Omega = signed_water_omega(k, h=h)

    # Sweep from weak to strong counterflow and back slightly for a loopable feel.
    half = N_FRAMES // 2
    u_down = np.linspace(-0.35, -1.85, half, endpoint=False)
    u_up = np.linspace(-1.85, -0.35, N_FRAMES - half)
    u_values = np.concatenate([u_down, u_up])

    fig, ax = plt.subplots()
    style_axes(ax, grid=True)
    ax.set_xlim(-18, 18)
    ax.set_ylim(-7.2, 7.2)
    ax.set_xlabel("wavenumber  $k$")
    ax.set_ylabel("comoving frequency  $\\Omega$")
    ax.set_title("Keep the lab frequency fixed — the allowed wavelengths rearrange", loc="left")

    ax.plot(k, Omega, color=BLUE, lw=3.0)
    doppler, = ax.plot([], [], color=RED, lw=2.5)
    points, = ax.plot([], [], "o", color=WHITE, ms=9, mec=BG, mew=1.5)

    ax.axhline(0, color=MUTED, lw=1.0, alpha=0.4)
    ax.axvline(0, color=MUTED, lw=1.0, alpha=0.4)

    info = ax.text(
        0.02, 0.93, "", transform=ax.transAxes, ha="left", va="top", fontsize=14
    )
    ax.text(
        0.98, 0.06,
        "intersections = allowed $k$ values",
        transform=ax.transAxes, ha="right", va="bottom", color=MUTED, fontsize=13
    )

    def update(i):
        u = u_values[i]
        line = omega0 - u * k
        doppler.set_data(k, line)

        roots = roots_from_samples(k, Omega - line)
        vals = np.interp(roots, k, Omega) if len(roots) else np.array([])
        points.set_data(roots, vals)

        n = len(roots)
        info.set_text(
            f"fixed lab frequency  $\\omega$ = {omega0:.2f}\n"
            f"counterflow  u = {u:+.2f}\n"
            f"{n} real intersection{'s' if n != 1 else ''}"
        )
        return doppler, points, info

    # Save a still near the strongest-flow point, where multiple roots are clearest.
    update(half - 1)
    save_png(fig, 7)

    anim = FuncAnimation(fig, update, frames=len(u_values), interval=1000 / fps, blit=False)
    save_animation(anim, 7, fps, make_gif, make_mp4)
    plt.close(fig)


# =============================================================================
# MAIN
# =============================================================================

FIGURE_FUNCTIONS = {
    1: figure_1,
    2: figure_2,
    3: figure_3,
    4: figure_4,
    5: figure_5,
    6: figure_6,
    7: figure_7,
}


def parse_args():
    p = argparse.ArgumentParser(description="Generate all article figures.")
    p.add_argument("--only", type=int, choices=sorted(FIGURE_FUNCTIONS), help="Generate one figure only.")
    p.add_argument("--fps", type=int, default=FPS, help=f"Animation FPS (default: {FPS}).")
    p.add_argument("--no-gif", action="store_true", help="Do not write GIF files.")
    p.add_argument("--no-mp4", action="store_true", help="Do not write MP4 files.")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    configure_style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    make_gif = not args.no_gif
    make_mp4 = not args.no_mp4

    numbers = [args.only] if args.only is not None else sorted(FIGURE_FUNCTIONS)

    for number in numbers:
        print(f"\n--- figure {number} ---")
        fn = FIGURE_FUNCTIONS[number]
        if number in (1, 5):
            fn()
        else:
            fn(args.fps, make_gif, make_mp4)

    print("\nDone.")


if __name__ == "__main__":
    main()
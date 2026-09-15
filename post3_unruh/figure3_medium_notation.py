#!/usr/bin/env python3
"""
generate_figure_3_alice_bob.py

Figure 3 — The same wave for Alice and accelerated Bob.

LEFT PANELS
-----------
The complex field is shown as a NORMALIZED helix.

The Gaussian envelope is used to define the time interval, but the
amplitude is normalized to unity when plotting:

    phi_plot = phi / |phi|

This deliberately removes the packet envelope from the helix visualisation,
leaving only the phase evolution.

Alice:
    Uniformly spaced turns.

Bob:
    Nonuniformly spaced turns because the same Minkowski wave is sampled
    along an accelerated trajectory.

For visual clarity, the acceleration used for the helix is larger than
the acceleration used for the spectral calculation:

    KAPPA_HELIX = 5.0
    KAPPA_SPECTRUM = 1.0

RIGHT PANELS
------------
Alice:
    Analytical Fourier amplitude of a Gaussian-envelope carrier.

Bob:
    Numerical Fourier transform of a Gaussian packet sampled along
    Bob's accelerated trajectory.

The spectral calculations use the ACTUAL packet amplitude and are not
affected by the normalization used in the left-hand helix plots.

Fourier convention:

    F(Omega) = integral phi(t) exp(+i Omega t) dt

so

    exp(-i omega0 t)

appears at positive Omega.

Output:
    Figure_3.png
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
OUTPUT_PATH = SCRIPT_DIR / "Figure_3.png"


# =============================================================================
# Physical / illustrative parameters
# =============================================================================

C = 1.0

# Alice's monochromatic Minkowski angular frequency.
# Omega below is reserved for the Fourier-frequency coordinate.
OMEGA_M = 600.0

# Stronger acceleration for the visual helix so the chirp is obvious.
KAPPA_HELIX = 5.0

# More moderate acceleration for the spectrum calculation.
KAPPA_SPECTRUM = 1.0


# =============================================================================
# Packet widths
# =============================================================================

# Number of carrier cycles across approximately +/- 3 sigma
# in the LEFT helix panels.
HELIX_CYCLES_ALICE = 25
HELIX_CYCLES_BOB = 25

# Effective number of cycles across +/- 3 sigma
# in the RIGHT spectrum panels.
SPECTRUM_CYCLES_ALICE = 50
SPECTRUM_CYCLES_BOB = 50


def sigma_from_cycles(
    n_cycles: float,
) -> float:
    """
    Return Gaussian sigma corresponding to approximately n_cycles
    carrier periods across [-3 sigma, +3 sigma].

        6 sigma * omega0 / (2 pi) = n_cycles
    """
    return (
        n_cycles
        * 2.0
        * np.pi
        / (6.0 * OMEGA_M)
    )


SIGMA_HELIX_ALICE = sigma_from_cycles(
    HELIX_CYCLES_ALICE
)

SIGMA_HELIX_BOB = sigma_from_cycles(
    HELIX_CYCLES_BOB
)

SIGMA_SPEC_ALICE = sigma_from_cycles(
    SPECTRUM_CYCLES_ALICE
)

SIGMA_SPEC_BOB = sigma_from_cycles(
    SPECTRUM_CYCLES_BOB
)


# =============================================================================
# Numerical parameters
# =============================================================================

HELIX_EXTENT_SIGMA_ALICE = 3.3
HELIX_EXTENT_SIGMA_BOB = 3.3

SPECTRUM_EXTENT_SIGMA = 3.7

N_HELIX = 6000
N_SPECTRUM_TIME = 2**16

OMEGA_PLOT_MAX = 1200.0

DB_FLOOR = -100.0


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

FIGSIZE = (12.2, 8.2)
DPI = 190

ROW_LABEL_SIZE = 18
AXIS_LABEL_SIZE = 15
TICK_SIZE = 11
SIGN_SIZE = 13

HELIX_LW = 1.8
SPECTRUM_LW = 2.3


def configure_style() -> None:
    """Apply the dark visual language used in the other article figures."""
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
            "grid.color": GRID,
            "font.size": TICK_SIZE,
            "axes.labelsize": AXIS_LABEL_SIZE,
            "xtick.labelsize": TICK_SIZE,
            "ytick.labelsize": TICK_SIZE,
        }
    )


# =============================================================================
# Minkowski wave packet
# =============================================================================

def packet_field(
    u: np.ndarray,
    sigma_u: float,
) -> np.ndarray:
    """
    Right-moving complex Gaussian wave packet.

        phi(u)
            = exp[-u^2 / (2 sigma_u^2)]
              exp[-i omega0 u]

    where

        u = t - x/c.
    """
    envelope = np.exp(
        -0.5
        * (u / sigma_u) ** 2
    )

    carrier = np.exp(
        -1j
        * OMEGA_M
        * u
    )

    return envelope * carrier


# =============================================================================
# Accelerated trajectories
# =============================================================================

def bob_u_helix(
    tau: np.ndarray,
) -> np.ndarray:
    """
    Accelerated trajectory used for the illustrative helix.

        u_B(tau)
            = (1/kappa) [1 - exp(-kappa tau)]
    """
    return (
        1.0
        / KAPPA_HELIX
        * (
            1.0
            - np.exp(
                -KAPPA_HELIX * tau
            )
        )
    )


def bob_u_spectrum(
    tau: np.ndarray,
) -> np.ndarray:
    """
    Accelerated trajectory used for the spectrum calculation.
    """
    return (
        1.0
        / KAPPA_SPECTRUM
        * (
            1.0
            - np.exp(
                -KAPPA_SPECTRUM * tau
            )
        )
    )


def tau_from_u(
    u: float,
    kappa: float,
) -> float:
    """
    Invert

        u = (1/kappa) [1 - exp(-kappa tau)]

    for a specified acceleration parameter.
    """
    argument = (
        1.0
        - kappa * u
    )

    if argument <= 0.0:
        raise ValueError(
            "Requested packet extent crosses the Rindler horizon. "
            "Reduce packet width or extent."
        )

    return (
        -np.log(argument)
        / kappa
    )


# =============================================================================
# Helix signals
# =============================================================================

def make_alice_helix() -> tuple[
    np.ndarray,
    np.ndarray,
]:
    """
    Packet used to define Alice's visual helix interval.
    """
    extent = (
        HELIX_EXTENT_SIGMA_ALICE
        * SIGMA_HELIX_ALICE
    )

    t = np.linspace(
        -extent,
        +extent,
        N_HELIX,
    )

    phi = packet_field(
        t,
        SIGMA_HELIX_ALICE,
    )

    return t, phi


def make_bob_helix() -> tuple[
    np.ndarray,
    np.ndarray,
]:
    """
    Bob helix using enhanced visual acceleration KAPPA_HELIX.
    """
    extent = (
        HELIX_EXTENT_SIGMA_BOB
        * SIGMA_HELIX_BOB
    )

    u_min = -extent
    u_max = +extent

    tau_min = tau_from_u(
        u_min,
        KAPPA_HELIX,
    )

    tau_max = tau_from_u(
        u_max,
        KAPPA_HELIX,
    )

    tau = np.linspace(
        tau_min,
        tau_max,
        N_HELIX,
    )

    u = bob_u_helix(
        tau
    )

    phi = packet_field(
        u,
        SIGMA_HELIX_BOB,
    )

    return tau, phi


# =============================================================================
# Alice spectrum — analytical
# =============================================================================

def alice_analytic_spectrum(
    omega_axis: np.ndarray,
) -> np.ndarray:
    """
    Analytical Fourier amplitude of Alice's Gaussian-envelope carrier.

        |F(Omega)|
            proportional to
            exp[-sigma^2 (Omega - omega0)^2 / 2]
    """
    amplitude = np.exp(
        -0.5
        * (
            SIGMA_SPEC_ALICE
            * (
                omega_axis
                - OMEGA_M
            )
        )
        ** 2
    )

    amplitude /= np.max(
        amplitude
    )

    return amplitude


# =============================================================================
# Bob spectrum — numerical
# =============================================================================

def fourier_amplitude(
    signal: np.ndarray,
    dt: float,
) -> tuple[
    np.ndarray,
    np.ndarray,
]:
    """
    Fourier transform using

        F(Omega)
            = integral f(t) exp(+i Omega t) dt.

    numpy.ifft uses the desired positive exponential sign.
    """
    n = len(signal)

    transform = (
        np.fft.ifft(signal)
        * n
        * dt
    )

    frequency = np.fft.fftfreq(
        n,
        d=dt,
    )

    omega_axis = (
        2.0
        * np.pi
        * frequency
    )

    omega_axis = np.fft.fftshift(
        omega_axis
    )

    transform = np.fft.fftshift(
        transform
    )

    amplitude = np.abs(
        transform
    )

    return (
        omega_axis,
        amplitude,
    )


def make_bob_spectrum() -> tuple[
    np.ndarray,
    np.ndarray,
]:
    """
    Calculate Bob's spectrum using KAPPA_SPECTRUM.
    """
    extent = (
        SPECTRUM_EXTENT_SIGMA
        * SIGMA_SPEC_BOB
    )

    u_min = -extent
    u_max = +extent

    tau_min = tau_from_u(
        u_min,
        KAPPA_SPECTRUM,
    )

    tau_max = tau_from_u(
        u_max,
        KAPPA_SPECTRUM,
    )

    tau = np.linspace(
        tau_min,
        tau_max,
        N_SPECTRUM_TIME,
        endpoint=False,
    )

    dtau = (
        tau[1]
        - tau[0]
    )

    u = bob_u_spectrum(
        tau
    )

    phi = packet_field(
        u,
        SIGMA_SPEC_BOB,
    )

    omega_axis, amplitude = (
        fourier_amplitude(
            phi,
            dtau,
        )
    )

    return (
        omega_axis,
        amplitude,
    )


# =============================================================================
# dB conversion
# =============================================================================

def amplitude_to_db(
    amplitude: np.ndarray,
    reference: float | None = None,
) -> np.ndarray:
    """
    Convert amplitude to dB.

    If reference is omitted, normalize to the largest amplitude.
    """
    if reference is None:
        reference = np.max(
            amplitude
        )

    minimum = (
        reference
        * 10.0
        ** (
            DB_FLOOR
            / 20.0
        )
    )

    safe = np.maximum(
        amplitude,
        minimum,
    )

    db = (
        20.0
        * np.log10(
            safe / reference
        )
    )

    return np.maximum(
        db,
        DB_FLOOR,
    )


# =============================================================================
# Helix plotting
# =============================================================================

def normalize_complex_field(
    field: np.ndarray,
) -> np.ndarray:
    """
    Normalize a complex field to unit magnitude while preserving phase.

        phi -> phi / |phi| = exp(i arg(phi))

    This removes the Gaussian envelope so the helix shows only the
    progression of phase / instantaneous frequency.
    """
    return np.exp(
        1j * np.angle(field)
    )


def style_3d_axes(
    ax,
    x_min: float,
    x_max: float,
) -> None:
    """Minimal 3D styling for the normalized complex-field helices."""
    ax.set_facecolor(BG)

    for axis in (
        ax.xaxis,
        ax.yaxis,
        ax.zaxis,
    ):
        axis.pane.set_facecolor(
            BG
        )

        axis.pane.set_edgecolor(
            BG
        )

    ax.xaxis._axinfo["grid"]["color"] = GRID
    ax.yaxis._axinfo["grid"]["color"] = GRID
    ax.zaxis._axinfo["grid"]["color"] = GRID

    ax.xaxis._axinfo["grid"]["linewidth"] = 0.55
    ax.yaxis._axinfo["grid"]["linewidth"] = 0.55
    ax.zaxis._axinfo["grid"]["linewidth"] = 0.55

    ax.tick_params(
        colors=MUTED,
        labelsize=TICK_SIZE,
    )

    ax.set_xlim(
        x_min,
        x_max,
    )

    ax.set_ylim(
        -1.10,
        +1.10,
    )

    ax.set_zlim(
        -1.10,
        +1.10,
    )

    ax.set_yticks(
        [-1, 0, 1]
    )

    ax.set_zticks(
        [-1, 0, 1]
    )

    ax.view_init(
        elev=18,
        azim=-66,
    )

    ax.set_box_aspect(
        (3.2, 1.0, 1.0)
    )


def plot_helix(
    ax,
    observer_time: np.ndarray,
    field: np.ndarray,
    time_label: str,
) -> None:
    """
    Plot the NORMALIZED complex field as a constant-radius helix.

    The amplitude envelope is deliberately removed here so spacing
    between successive turns directly represents instantaneous frequency.
    """
    normalized_field = normalize_complex_field(
        field
    )

    ax.plot(
        observer_time,
        np.real(normalized_field),
        np.imag(normalized_field),
        color=BLUE,
        lw=HELIX_LW,
    )

    # Central observer-time axis.
    ax.plot(
        [
            observer_time.min(),
            observer_time.max(),
        ],
        [0, 0],
        [0, 0],
        color=MUTED,
        lw=0.85,
        alpha=0.70,
    )
    # Illustrative time axis: keep the axis but remove numerical tick labels.
    ax.set_xticklabels([])
    ax.set_xticks([])
    ax.set_xlabel(
        time_label,
        labelpad=9,
        color=FG,
    )

    ax.set_ylabel(
        r"$\mathrm{Re}\,\phi$",
        labelpad=6,
        color=MUTED,
    )

    ax.set_zlabel(
        r"$\mathrm{Im}\,\phi$",
        labelpad=6,
        color=MUTED,
    )

    style_3d_axes(
        ax,
        observer_time.min(),
        observer_time.max(),
    )


# =============================================================================
# Spectrum plotting
# =============================================================================

def style_spectrum_axes(
    ax: plt.Axes,
) -> None:
    """Shared styling for Fourier-amplitude plots."""
    ax.set_xlim(
        -OMEGA_PLOT_MAX,
        +OMEGA_PLOT_MAX,
    )

    ax.set_ylim(
        DB_FLOOR,
        4.0,
    )

    ax.axvline(
        0.0,
        color=MUTED,
        lw=1.0,
        alpha=0.80,
    )

    ax.grid(
        True,
        linewidth=0.7,
        alpha=0.30,
    )

    ax.spines["top"].set_visible(
        False
    )

    ax.spines["right"].set_visible(
        False
    )

    ax.spines["left"].set_color(
        MUTED
    )

    ax.spines["bottom"].set_color(
        MUTED
    )

    ax.set_xlabel(
        r"Fourier frequency  $\Omega$",
        color=FG,
    )

    ax.set_ylabel(
        r"Fourier amplitude  (dB)",
        color=FG,
    )

    ax.text(
        0.24,
        0.92,
        r"$\Omega < 0$",
        transform=ax.transAxes,
        color=RED,
        fontsize=SIGN_SIZE,
        ha="center",
    )

    ax.text(
        0.88,
        0.92,
        r"$\Omega > 0$",
        transform=ax.transAxes,
        color=BLUE,
        fontsize=SIGN_SIZE,
        ha="center",
    )


def plot_spectrum(
    ax: plt.Axes,
    omega_axis: np.ndarray,
    amplitude_db: np.ndarray,
) -> None:
    """
    Plot negative frequencies in red and positive frequencies in blue.
    """
    visible = (
        np.abs(omega_axis)
        <= OMEGA_PLOT_MAX
    )

    positive = (
        visible
        & (omega_axis >= 0.0)
    )

    negative = (
        visible
        & (omega_axis < 0.0)
    )

    # Positive frequencies.
    ax.plot(
        omega_axis[positive],
        amplitude_db[positive],
        color=BLUE,
        lw=SPECTRUM_LW,
    )

    ax.fill_between(
        omega_axis[positive],
        DB_FLOOR,
        amplitude_db[positive],
        color=BLUE,
        alpha=0.14,
    )

    # Negative frequencies.
    visible_negative = (
        negative
        & (
            amplitude_db
            > DB_FLOOR + 0.5
        )
    )

    if np.any(
        visible_negative
    ):
        ax.plot(
            omega_axis[
                visible_negative
            ],
            amplitude_db[
                visible_negative
            ],
            color=RED,
            lw=SPECTRUM_LW,
        )

        ax.fill_between(
            omega_axis[
                visible_negative
            ],
            DB_FLOOR,
            amplitude_db[
                visible_negative
            ],
            color=RED,
            alpha=0.14,
        )

    style_spectrum_axes(
        ax
    )


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    """Generate and save Figure 3."""
    configure_style()

    # -------------------------------------------------------------------------
    # Helices
    # -------------------------------------------------------------------------

    t_alice_helix, phi_alice_helix = (
        make_alice_helix()
    )

    tau_bob_helix, phi_bob_helix = (
        make_bob_helix()
    )

    # -------------------------------------------------------------------------
    # Alice spectrum
    # -------------------------------------------------------------------------

    omega_alice = np.linspace(
        -OMEGA_PLOT_MAX,
        +OMEGA_PLOT_MAX,
        8000,
    )

    amp_alice = (
        alice_analytic_spectrum(
            omega_alice
        )
    )

    alice_db = amplitude_to_db(
        amp_alice
    )

    # -------------------------------------------------------------------------
    # Bob spectrum
    # -------------------------------------------------------------------------

    omega_bob, amp_bob = (
        make_bob_spectrum()
    )

    bob_positive = (
        omega_bob > 0.0
    )

    bob_reference = np.max(
        amp_bob[
            bob_positive
        ]
    )

    bob_db = amplitude_to_db(
        amp_bob,
        reference=bob_reference,
    )

    # -------------------------------------------------------------------------
    # Layout
    # -------------------------------------------------------------------------

    fig = plt.figure(
        figsize=FIGSIZE,
        facecolor=BG,
    )

    gs = fig.add_gridspec(
        2,
        2,
        width_ratios=[
            1.75,
            1.00,
        ],
        height_ratios=[
            1.0,
            1.0,
        ],
        left=0.045,
        right=0.975,
        bottom=0.075,
        top=0.955,
        wspace=0.13,
        hspace=0.26,
    )

    ax_alice_wave = fig.add_subplot(
        gs[0, 0],
        projection="3d",
    )

    ax_alice_spec = fig.add_subplot(
        gs[0, 1],
    )

    ax_bob_wave = fig.add_subplot(
        gs[1, 0],
        projection="3d",
    )

    ax_bob_spec = fig.add_subplot(
        gs[1, 1],
    )

    # -------------------------------------------------------------------------
    # Alice
    # -------------------------------------------------------------------------

    plot_helix(
        ax_alice_wave,
        t_alice_helix,
        phi_alice_helix,
        r"Alice's time  $t$",
    )

    plot_spectrum(
        ax_alice_spec,
        omega_alice,
        alice_db,
    )

    ax_alice_spec.annotate(
        r"Alice's carrier $\omega$",
        xy=(OMEGA_M, -1.0),
        xytext=(OMEGA_M - 460.0, -22.0),
        color=BLUE,
        fontsize=11,
        ha="center",
        arrowprops={
            "arrowstyle": "->",
            "color": BLUE,
            "lw": 1.1,
        },
    )

    # -------------------------------------------------------------------------
    # Bob
    # -------------------------------------------------------------------------

    plot_helix(
        ax_bob_wave,
        tau_bob_helix,
        phi_bob_helix,
        r"Bob's proper time  $\tau$",
    )

    # Bob's local instantaneous frequency changes continuously along
    # the accelerated trajectory.  This is distinct from Omega, which
    # labels the constant-frequency components in the Fourier spectrum.
    ax_bob_wave.text2D(
        0.50,
        0.92,
        r"$\omega(\tau)=\omega e^{-a\tau/c}$",
        transform=ax_bob_wave.transAxes,
        ha="center",
        va="center",
        fontsize=13,
        color=FG,
    )

    # ax_bob_wave.text2D(
    #     0.50,
    #     0.855,
    #     "instantaneous frequency changes",
    #     transform=ax_bob_wave.transAxes,
    #     ha="center",
    #     va="center",
    #     fontsize=11,
    #     color=MUTED,
    # )

    plot_spectrum(
        ax_bob_spec,
        omega_bob,
        bob_db,
    )

    # -------------------------------------------------------------------------
    # Row labels
    # -------------------------------------------------------------------------

    fig.text(
        0.045,
        0.952,
        "Alice — inertial",
        color=FG,
        fontsize=ROW_LABEL_SIZE,
        ha="left",
        va="top",
    )

    fig.text(
        0.045,
        0.478,
        "Bob — accelerated",
        color=FG,
        fontsize=ROW_LABEL_SIZE,
        ha="left",
        va="top",
    )

    # -------------------------------------------------------------------------
    # Save
    # -------------------------------------------------------------------------

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

    bob_negative = (
        omega_bob < 0.0
    )

    max_bob_positive = np.max(
        amp_bob[
            bob_positive
        ]
    )

    max_bob_negative = np.max(
        amp_bob[
            bob_negative
        ]
    )

    ratio = (
        max_bob_negative
        / max_bob_positive
    )

    ratio_db = (
        20.0
        * np.log10(
            ratio
        )
    )

    tau_early = np.min(
        tau_bob_helix
    )

    tau_late = np.max(
        tau_bob_helix
    )

    omega_bob_early = (
        OMEGA_M
        * np.exp(
            -KAPPA_HELIX
            * tau_early
        )
    )

    omega_bob_late = (
        OMEGA_M
        * np.exp(
            -KAPPA_HELIX
            * tau_late
        )
    )

    print()
    print(
        "Figure 3 — Alice and accelerated Bob"
    )
    print(
        "------------------------------------"
    )

    print(
        f"Alice Minkowski frequency omega_M = "
        f"{OMEGA_M:.3f}"
    )

    print()

    print(
        f"kappa helix                       = "
        f"{KAPPA_HELIX:.3f}"
    )

    print(
        f"kappa spectrum                    = "
        f"{KAPPA_SPECTRUM:.3f}"
    )

    print()

    print(
        f"helix cycles Alice                = "
        f"{HELIX_CYCLES_ALICE}"
    )

    print(
        f"helix cycles Bob                  = "
        f"{HELIX_CYCLES_BOB}"
    )

    print(
        f"spectrum cycles Alice             = "
        f"{SPECTRUM_CYCLES_ALICE}"
    )

    print(
        f"spectrum cycles Bob               = "
        f"{SPECTRUM_CYCLES_BOB}"
    )

    print()

    print(
        "Bob helix instantaneous frequency:"
    )

    print(
        f"  early                           = "
        f"{omega_bob_early:.2f}"
    )

    print(
        f"  late                            = "
        f"{omega_bob_late:.2f}"
    )

    print()

    print(
        "Bob spectrum:"
    )

    print(
        f"  max negative / positive amp     = "
        f"{ratio:.6e}"
    )

    print(
        f"  relative negative amplitude     = "
        f"{ratio_db:.2f} dB"
    )

    print()

    print(
        "Left helices are amplitude-normalized."
    )

    print()

    print(
        f"Saved: {OUTPUT_PATH}"
    )

    print(
        r"Figure 3 — One frequency becomes a chirp.\n",
        r"Left: Alice's Minkowski wave has one constant carrier frequency omega. Along Bob's accelerated trajectory, the same wave has an instantaneous frequency omega(tau)=omega exp(-a tau/c), so its phase turns progressively spread apart. Right: decomposing the signals into constant Fourier-frequency components Omega gives Alice a narrow positive-frequency spectrum, while Bob's chirped signal spreads over many Omega and develops a small negative-frequency component. The acceleration is exaggerated in the lower-left illustration to make the chirp visible; the spectra use a smaller acceleration and the actual wave-packet envelope."
    )

if __name__ == "__main__":
    main()
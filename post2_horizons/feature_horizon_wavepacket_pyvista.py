"""
feature_horizon_wavepacket_pyvista.py

Stylized feature image for the horizon post:
a wave packet propagating over a water surface whose height follows a tanh
profile, with the front of the packet compressed near the 'horizon' region.

This is intentionally illustrative rather than scientifically exact.

Requirements:
    pip install pyvista numpy

Optional:
    If interactive rendering gives issues on Windows, try:
        pip install pyvistaqt
"""

from __future__ import annotations

import numpy as np
import pyvista as pv
import os
from pathlib import Path
os.chdir("post2_horizons")
print(os.getcwd())


# =============================================================================
# User settings
# =============================================================================

# Output
# Saved in the current working directory when you press "s".
OUT_PNG = Path.cwd() / "Feature_image.png"

# Window / rendering
WINDOW_SIZE = (1800, 1000)
OFF_SCREEN = False   # set True if you only want to save a screenshot

# Domain
NX = 900
NY = 220
XMIN, XMAX = -14.0, 14.0
YMIN, YMAX = -5.0, 5.0

# Base 'flow profile' visualized as surface height
RAMP_CENTER = 2.0
RAMP_WIDTH = 2.8
RAMP_HEIGHT = 1.9

# Wave packet position and shape
PACKET_CENTER = -2.0
PACKET_WIDTH = 3.6
PACKET_AMPLITUDE = 1.32
TRANSVERSE_TAPER = 0.7

# Carrier / compression
K0 = 2.0                 # base wavenumber
COMPRESSION_CENTER = 1.2
COMPRESSION_WIDTH = 1.5
COMPRESSION_STRENGTH = 2.8

# Optional slight skew so the packet feels like it is being pulled in
FRONT_STEEPNESS = 0.35

# Visual exaggeration
VERTICAL_SCALE = 1.0

# Optional arrows indicating counterflow
ADD_FLOW_ARROWS = False
N_ARROWS_X = 11
N_ARROWS_Y = 3


# =============================================================================
# Helper functions
# =============================================================================

def smooth_step(x: np.ndarray, x0: float, w: float) -> np.ndarray:
    """0-to-1 smooth step based on tanh."""
    return 0.5 * (1.0 + np.tanh((x - x0) / w))


def make_base_surface(x: np.ndarray) -> np.ndarray:
    """
    Stylized tanh-shaped height profile.
    Think of it as a visual cue for increasing counterflow / obstacle region.
    """
    return 0.5 * RAMP_HEIGHT * (1.0 + np.tanh((x - RAMP_CENTER) / RAMP_WIDTH))


def make_local_wavenumber(x: np.ndarray) -> np.ndarray:
    """
    Increase k smoothly near the 'horizon' region so the front gets compressed.
    """
    compress = smooth_step(x, COMPRESSION_CENTER, COMPRESSION_WIDTH)
    return K0 * (1.0 + COMPRESSION_STRENGTH * compress)


def integrate_phase(x: np.ndarray, kx: np.ndarray) -> np.ndarray:
    """Integrate k(x) to obtain a spatial phase."""
    dx = x[1] - x[0]
    phase = np.cumsum(kx) * dx
    phase -= phase.mean()
    return phase


# =============================================================================
# Build grid
# =============================================================================

x = np.linspace(XMIN, XMAX, NX)
y = np.linspace(YMIN, YMAX, NY)
X, Y = np.meshgrid(x, y, indexing="xy")

# Base water surface: a rising tanh profile
Z_base_1d = make_base_surface(x)

# Wave packet envelope
env_x = np.exp(-((x - PACKET_CENTER) / PACKET_WIDTH) ** 2)

# Slight asymmetry so it looks more dramatic
skew = 1.0 / (1.0 + np.exp(-FRONT_STEEPNESS * (x - PACKET_CENTER)))
env_x = env_x * (0.82 + 0.36 * skew)

# Local wavenumber and integrated phase
k_local = make_local_wavenumber(x)
phase = integrate_phase(x, k_local)

# Carrier
carrier_1d = np.sin(phase)

# 1D packet
packet_1d = PACKET_AMPLITUDE * env_x * carrier_1d

# Transverse taper so the surface feels more water-like than sheet-like
taper_y = np.exp(-(Y / (TRANSVERSE_TAPER * (YMAX - YMIN) / 2.0)) ** 2)

# Lift the packet slightly near the center across y, but keep it broad
packet_2d = np.outer(np.ones(NY), packet_1d) * taper_y

# Slight additional long-wavelength cross ripples for realism
cross_ripple = 0.018 * np.cos(0.75 * Y) * np.exp(-((X - PACKET_CENTER) / 7.0) ** 2)

# Final surface
Z = np.outer(np.ones(NY), Z_base_1d) + packet_2d + cross_ripple
Z *= VERTICAL_SCALE

# Structured grid
grid = pv.StructuredGrid(X, Y, Z)

# Scalars for coloring: combine base height and local slope / packet prominence
# This gives some subtle visual structure without turning into a heatmap.
slope_x = np.gradient(Z, x, axis=1)
scalar_field = 0.15 * Z + 0.25 * np.abs(slope_x) + 0.20 * np.abs(packet_2d)
grid["water_scalar"] = scalar_field.ravel(order="F")


# =============================================================================
# Plotting
# =============================================================================

pv.set_plot_theme("document")

plotter = pv.Plotter(window_size=WINDOW_SIZE, off_screen=OFF_SCREEN)
plotter.set_background("#0b1020")

# Water surface
plotter.add_mesh(
    grid,
    scalars="water_scalar",
    cmap="ocean",
    smooth_shading=True,
    specular=0.55,
    specular_power=30,
    ambient=0.22,
    diffuse=0.85,
    show_scalar_bar=False,
)

# Optional soft wireframe very subtle, sometimes helps depth
# Uncomment if desired:
# plotter.add_mesh(
#     grid.extract_all_edges(),
#     color="white",
#     opacity=0.035,
#     line_width=1,
# )

# Add a faint translucent 'under-surface slab' to make it feel like volume
bottom_offset = 0.55
Xb = X.copy()
Yb = Y.copy()
Zb = Z - bottom_offset
bottom = pv.StructuredGrid(Xb, Yb, Zb)

plotter.add_mesh(
    bottom,
    color="#1c355e",
    opacity=0.18,
    smooth_shading=True,
)

# Flow arrows indicating counterflow (leftward)
if ADD_FLOW_ARROWS:
    xs = np.linspace(XMIN + 1.5, XMAX - 1.5, N_ARROWS_X)
    ys = np.linspace(YMIN * 0.5, YMAX * 0.5, N_ARROWS_Y)
    pts = []
    vecs = []

    for yy in ys:
        for xx in xs:
            zz = make_base_surface(np.array([xx]))[0] + 0.06
            pts.append([xx, yy, zz])

            # Stronger leftward arrows toward the right
            strength = 0.7 + 1.4 * smooth_step(np.array([xx]), RAMP_CENTER, RAMP_WIDTH)[0]
            vecs.append([-strength, 0.0, 0.0])

    pts = np.array(pts)
    vecs = np.array(vecs)

    pdata = pv.PolyData(pts)
    pdata["vectors"] = vecs
    pdata["mag"] = np.linalg.norm(vecs, axis=1)

    arrows = pdata.glyph(
        orient="vectors",
        scale="mag",
        factor=0.55,
        geom=pv.Arrow(tip_length=0.35, tip_radius=0.07, shaft_radius=0.025),
    )

    plotter.add_mesh(
        arrows,
        color="white",
        opacity=0.22,
        smooth_shading=True,
    )

# Lighting
light_1 = pv.Light(
    position=(-20, -12, 10),
    focal_point=(2, 0, 0),
    intensity=0.85,
)
light_2 = pv.Light(
    position=(8, 10, 16),
    focal_point=(2, 0, 0),
    intensity=0.55,
)
light_3 = pv.Light(
    position=(0, 0, 20),
    focal_point=(2, 0, 0),
    intensity=0.25,
)

lights = [light_1, light_2, light_3]
for light in lights:
    plotter.add_light(light)

# A little zoom can help composition
plotter.camera.zoom(1.15)

# Optional axes off for clean feature image
plotter.hide_axes()

# Camera settings
plotter.camera_position = [
    (-19.75079872725819, -11.403292961267057, 9.272212691148168),
    (0.7426539638586409, 1.6765842393211856, -0.12651984119343992),
    (0.30753739399901076, 0.18836196604601407, 0.9327060206943973),
]
plotter.camera.view_angle = 26.086956521739133
plotter.camera.clipping_range = (0.06044013918971281, 60.44013918971281)
plotter.camera.parallel_projection = False

# =============================================================================
# Interactive save callback
# =============================================================================

def save_feature_image() -> None:
    """Save the current view and print reproducible camera/light settings."""
    plotter.render()

    plotter.screenshot(
        str(OUT_PNG),
        transparent_background=False,
        window_size=WINDOW_SIZE,
    )

    cam = plotter.camera

    print("\n" + "=" * 76)
    print(f"Saved feature image: {OUT_PNG.resolve()}")
    print("=" * 76)

    print("\n# Camera settings")
    print("plotter.camera_position = [")
    print(f"    {tuple(cam.position)},")
    print(f"    {tuple(cam.focal_point)},")
    print(f"    {tuple(cam.up)},")
    print("]")
    print(f"plotter.camera.view_angle = {cam.view_angle!r}")
    print(f"plotter.camera.clipping_range = {tuple(cam.clipping_range)!r}")
    print(f"plotter.camera.parallel_projection = {cam.parallel_projection!r}")
    if cam.parallel_projection:
        print(f"plotter.camera.parallel_scale = {cam.parallel_scale!r}")

    print("\n# Light settings")
    for i, light in enumerate(lights, start=1):
        print(f"light_{i} = pv.Light(")
        print(f"    position={tuple(light.position)!r},")
        print(f"    focal_point={tuple(light.focal_point)!r},")
        print(f"    intensity={light.intensity!r},")
        print(f"    color={tuple(light.GetColor())!r},")
        print(")")
        print(f"plotter.add_light(light_{i})")
    print("=" * 76 + "\n")


# Press "s" in the PyVista window to save the current view.
plotter.add_key_event("s", save_feature_image)

print(f'Press "s" to save the current view as: {OUT_PNG.resolve()}')
print("The current camera and light settings will be printed at the same time.")

plotter.show()
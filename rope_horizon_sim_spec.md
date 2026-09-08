# Analog Horizon on a Moving Rope — Simulation Spec

## 0. Goal, split into two rounds

> **Round 1 (this document):** demonstrate the horizon, the characteristic
> slowing of the incident wave ($v_g\to0$), and the divergent
> trans-Planckian blueshift ($k\to\infty$) in the simplest **nondispersive**
> model. The nondispersive equation has only two linear dispersion
> branches — it cannot and should not be expected to produce
> positive/negative-frequency mode conversion; Schützhold & Unruh state
> this explicitly: in the nondispersive limit, incident waves pile up at
> the horizon and become arbitrarily blue-shifted, precisely because
> there is no mechanism to stop the blueshift.
>
> **Round 2 (later):** add a dispersive term (e.g. Corley–Jacobson-style
> $\omega^2=c^2k^2(1-\ell^2k^2)$, or the full $\tanh(kh)$ to connect
> directly to Rousseaux) so the dispersion relation develops a third real
> root for a given $\omega$. Only then does positive/negative
> comoving-frequency mode conversion — the actual classical analog of
> Hawking radiation — become possible to look for.

This split matters because it changes what Steps 6–7 below should check.

## 1. Physical system

A 1D string (rope) with:

- **Tension $T$** — constant in space and time.
- **Linear mass density $\mu$** — constant in space and time.
- **Background transport speed $v(x)$** — the rope material itself is being
  carried through the lab frame at a *position-dependent* speed. We do not
  worry about the mechanism (what pulls the rope, where it goes at the
  ends) — $v(x)$ is simply prescribed as a background field, the same way
  a fluid velocity profile is prescribed in the acoustic analog-gravity
  literature.

Because $T$ and $\mu$ are constant, the **intrinsic wave speed relative to
the rope material** is a single constant:

$$c = \sqrt{T/\mu}$$

All the interesting structure in this round comes purely from $v(x)$, not
from $c(x)$. (This is a deliberate simplification vs. the earlier
"varying tension" / shoaling discussion — no shoaling effect is expected
here, since $c$ never changes. Any amplitude change we see must come from
the advection/Doppler physics, not from impedance mismatch.)

**Caveat on physical consistency.** For an actual conserved material
string, a stationary spatially-varying transport velocity cannot coexist
with constant linear density without stretching or a mass source/sink:
continuity would require $\partial_t\mu + \partial_x(\mu v) = 0$, so a
truly stationary constant $\mu$ forces $v_x=0$. We are not attempting a
mechanically self-consistent continuously-moving rope. Instead, **$v(x)$
is treated as an externally prescribed effective advection field**,
exactly the convention used throughout the analog-gravity literature
(the background flow is simply specified, not derived from a closed
material model). This also means this model is a deliberately simpler
construction than Heyl's rope analog, which instead varies tension/mass
density to produce horizons via divergent travel time.

## 2. Governing equation

**Derivation, not analogy.** The equation must come from Newton's law
applied to a rope element advected at the local material velocity
$v(x)$, i.e. the material derivative $D/Dt = \partial_t + v(x)\partial_x$
applied twice:

$$\frac{D^2y}{Dt^2} = c^2\,y_{xx}$$

Expanding this explicitly (careful: since $v=v(x)$, this is *not* the
same operator as Rousseaux's fluid conservative-form
$(\partial_t+\partial_x v)(\partial_t+v\partial_x)$, which comes from the
combined mass/momentum-conservation structure of the fluid problem — the
two forms only coincide when $v$ is constant. The rope, being a material
advected by $v(x)$ rather than a conserved fluid flux, uses the
material-derivative-squared form):

$$y_{tt} + 2v(x)\,y_{tx} + v(x)^2\,y_{xx} + v(x)\,v'(x)\,y_x = c^2\,y_{xx}$$

- Local (no bulk boundary-value problem) — a real, hyperbolic, 2nd-order
  PDE, everywhere well posed to simulate with finite differences.
- Reduces to the plain wave equation $\partial_t^2y = c^2\partial_x^2y$
  when $v \equiv 0$, and to $(\partial_t+v\partial_x)^2y=c^2y_{xx}$ for
  constant $v$ — matching Step 2's uniform-flow check either way.

**Local dispersion relation** (from plane-wave ansatz, valid where $v$ is
locally ~constant — leave in this factored form rather than introducing
$|k|$, which confuses branch bookkeeping once negative $k$ is discussed):

$$(\omega - v(x)k)^2 = c^2k^2 \quad\Longrightarrow\quad \omega = \big(v(x)+c\big)k \ \ \text{or}\ \ \omega = \big(v(x)-c\big)k$$

Two linear branches only — no third root, unlike the dispersive water-wave
case. This is important later (Section 5, Step 6).

**Incident branch** (against the flow, launched from the subsonic side):

$$\omega = \big(v(x)+c\big)k \quad\Longrightarrow\quad k(x) = \frac{\omega_0}{v(x)+c}, \qquad v_g(x) = v(x)+c$$

**Horizon condition:** $|v(x)| = c$, i.e. $v(x)+c \to 0$ for this branch.
As $x\to x_h$: $k(x)\to+\infty$ and $v_g(x)\to0$ — the wave slows to a
halt and blueshifts without bound. This divergence, not a sign change in
comoving frequency, is the correct nondispersive-limit target (see
Section 5, Step 6).

## 3. Chosen configuration: white hole

We simulate a **white-hole** horizon (waves blocked from *entering* a
region), because it is the lab-realizable, numerically well-posed choice
(this is the Rousseaux et al. 2008 configuration), as opposed to a black
hole (which would require launching a wave from *behind* an inaccessible
horizon).

**Flow profile** (leftward flow, strengthening with $x$):

$$v(x) = -\left[v_0 + v_1\cdot\tfrac12\big(1+\tanh\big(\tfrac{x-x_0}{w}\big)\big)\right]$$

- $x \to -\infty$: $v \to -v_0$ — weak flow, **subsonic** ($|v_0| < c$) — this is "outside."
- $x \to +\infty$: $v \to -(v_0+v_1)$ — strong flow, **supersonic**
  ($|v_0+v_1| > c$) — this is "inside," behind the horizon.
- Horizon at some $x_h > x_0$ where $|v(x_h)| = c$.

**Wave launch:** from the **subsonic (left) side**, with a carrier
wavenumber $k_0>0$ chosen so the packet's intrinsic group velocity
relative to the fluid ($+c$, "against the flow" branch) gives a **net
rightward lab-frame group velocity**, $v(x)+c$, positive on the left and
shrinking toward zero as $x\to x_h$. The packet is swept toward the
horizon, decelerates, and (for the nondispersive equation) never crosses
— it piles up and blueshifts without bound. This is the correct Round 1
target: the trans-Planckian precursor to Hawking radiation, not the
mode-conversion signature itself (which needs dispersion — see Section 0).

## 4. Architecture

- **`Grid`** — `x` array, `dx`, `nx`, `dt` (set from CFL once `Medium` is known).
- **`Medium`** — holds `c` (scalar constant here) and `v(x)` (array), evaluated once on the grid. Static in time for this round.
- **`WaveState`** — `y_curr`, `y_prev` (leapfrog), current time `t`.
- **`Simulation`** — owns one `Medium` + one `WaveState`; provides `step()`, `run()`, stores `history` for plotting.
- **`make_wavepacket(grid, medium, x_center, width, k0, branch)`** — free function, builds `(y0, ydot0)` consistent with the local dispersion relation on the chosen branch.
- **Diagnostics** — space-time plot, animated line plot, local `k(x)` extraction (windowed FFT or Hilbert transform), local co-moving frequency $\omega'(x) = \omega - v(x)k(x)$.

## 5. Stepwise build-and-check plan

Each step should run and produce a plot/number to confirm before moving to
the next. Do not proceed on a step whose check fails.

### Step 1 — Static medium, no flow, sanity check
- Build `Grid`, `Medium` with `v(x) ≡ 0`, constant `c`.
- Launch a simple Gaussian pulse (no carrier, or a simple carrier) at the
  center of the domain with **symmetric** initial velocity (zero `ydot0`,
  i.e. a pulse that will split into left- and right-going halves).
- **Check:** the pulse splits into two identical pulses moving at exactly
  $\pm c$ (measure numerically via peak position vs. time), amplitude
  unchanged, no numerical dispersion or growth. Confirms `step()`,
  ghost-step init, and CFL/`dt` are correct before any flow is added.

### Step 2 — Uniform nonzero flow, no horizon
- Set `v(x) ≡ v_const` (subsonic, no ramp).
- Launch a one-directional wavepacket (constructed via `make_wavepacket`,
  chosen branch).
- **Check:** measured lab-frame group velocity matches $v_\text{const}+c$
  (or $-c$, depending on branch) to numerical precision. Confirms the
  Doppler/advection term in the discretized PDE is implemented correctly,
  isolated from any spatial-ramp effects.

### Step 3 — Introduce the ramp, no wave yet
- Set `v(x)` to the full white-hole ramp.
- Just plot $v(x)$ against $\pm c$ and locate $x_h$ (root of $|v(x)|=c$)
  numerically.
- **Check:** horizon location matches what you'd compute analytically from
  the ramp parameters. No simulation run needed yet — pure setup
  validation.

### Step 4 — Wavepacket far from the horizon (WKB check)
- Launch the packet from the subsonic side, but stop the simulation well
  before it reaches the horizon.
- Extract local $k(x)$ from the numerical field (windowed FFT or Hilbert
  transform) at a few points along its path.
- **Check:** measured $k(x)$ matches the root of the local dispersion
  relation $(\omega - v(x)k)^2 = c^2k^2$ for the known launch $\omega$.
  Confirms the packet is behaving as a well-defined WKB mode before we
  trust anything near the horizon.

### Step 5 — Full run: approach and pile-up
- Run the full simulation through the horizon region.
- **Check (qualitative):** space-time plot shows the packet's wavelength
  visibly compressing (blueshift) as $x\to x_h$, and the packet **piling
  up** progressively closer to the horizon without crossing it — this is
  the expected nondispersive behavior (Schützhold & Unruh). Do **not**
  expect a clean reflected packet: if a well-defined reflected wave
  appears once the local wavelength has dropped to only a few grid cells,
  that is very likely the numerical lattice acting as an artificial
  (unphysical) dispersion relation, not continuum physics — see the
  resolution guard below.
- **Check (resolution guard):** confirm the local wavelength never drops
  below ~10 grid points before the run ends / before you stop trusting the
  output (see trans-Planckian/lattice-cutoff discussion — grid discreteness
  becomes an uncontrolled regulator beyond that point). If you want to
  push further without lattice artifacts contaminating the result, you
  need finer resolution near $x_h$, not more time steps.

### Step 6 — Near-horizon blueshift / trans-Planckian diagnostic

This replaces the earlier "hunt for $k<0$" version of Step 6 — that
diagnostic requires dispersion (Round 2) and is not meaningful here.

- Track the wavepacket peak/ridge position $x_\text{packet}(t)$ and
  measure its group velocity numerically: $v_g(x) = dx_\text{packet}/dt$.
- Compare against the analytic prediction $v_g(x) = v(x)+c$.
- Extract the local wavenumber $k(x)$ (windowed FFT or Hilbert transform)
  and compare against $k(x) = \omega_0 / (v(x)+c)$.
- Compute $\omega'(x) = \omega_0 - v(x)k(x)$ and verify it equals
  $c\,k(x)$ for the incident branch.
- **Check:** as $x\to x_h$, all three diagnostics should show
  $v_g\to0$, $k\to\infty$, $\omega'\to\infty$ — the lab-frame frequency
  $\omega_0$ stays finite and conserved throughout (medium is
  time-independent), while the locally-measured comoving frequency and
  wavenumber diverge. This is the trans-Planckian problem, demonstrated
  cleanly and quantitatively. Stop trusting the run once
  $\lambda_\text{local}\lesssim 10\,\Delta x$ (same guard as Step 5).

### Step 7 — Parameter sweep: resolution independence and surface gravity

- Vary $\Delta x$ (resolution) at fixed $w,k_0$: confirm $k(x) =
  \omega_0/(v(x)+c)$ holds independently of resolution, up to
  progressively closer approach to $x_h$ as resolution improves — i.e.
  confirm the divergence is a continuum feature, not a discretization
  artifact, by checking it persists (and the cutoff point recedes toward
  $x_h$) as $\Delta x\to0$.
- Vary ramp steepness $w$: compute the analog surface gravity
  $\kappa = \left|\dfrac{d(v+c)}{dx}\right|_{x_h}$ and confirm it changes
  with $w$ as expected (sharper ramp → larger $\kappa$). This is a
  meaningful, well-defined Round 1 quantity — unlike "conversion
  strength," which is not defined without dispersion — and is exactly the
  parameter that would set the analog Hawking temperature once Round 2
  introduces dispersion and an actual thermal spectrum becomes
  computable.

## 6. Explicit non-goals for this round

- **No positive/negative-frequency mode conversion.** This is not a
  Round 1 deliverable — it requires dispersion (Round 2) to give the
  dispersion relation a third real root. Looking for a $k<0$ outgoing
  component in Round 1 is not a valid diagnostic; if one appears, suspect
  numerical lattice dispersion (see Step 5/6 resolution guards) rather
  than physics.
- No dispersion ($\tanh(kh)$-type term) — purely the non-dispersive,
  local rope equation.
- No variation in $c(x)$ — $T,\mu$ held constant throughout.
- No nonlinearity, no amplitude-dependent effects.
- No attempt at a single global "flow-frame" transformation — only local
  per-region Galilean boosts (valid in the asymptotic constant-$v$ zones)
  and the pointwise $\omega'(x)$ diagnostic are used to interpret
  co-moving frequency (now understood to diverge, not cross zero, at the
  horizon — see Section 2).

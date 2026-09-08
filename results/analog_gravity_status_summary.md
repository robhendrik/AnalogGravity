# Analog Horizon Simulation — Standalone Status Summary

## Scope

This project studies wave propagation against a spatially varying background flow as a simple analog-gravity model. The central question is what happens to an incident wave packet as it approaches a white-hole-like blocking region, and how that behavior changes once a controlled physical dispersion relation is introduced.

The work so far has been organized in three rounds:

- **Round 1:** establish the nondispersive baseline and verify the horizon/blueshift picture.
- **Round 2:** explore how a lattice-like dispersion changes the mode structure and learn how numerical and physical dispersion must be kept distinct.
- **Round 3:** introduce a controlled, stable dispersive continuum model, validate it in uniform flow, propagate a packet on the tanh ramp, and resolve the outgoing mode content.

The current status is that the **Round-3 dispersive solver is validated in uniform flow**, the incident packet follows the expected local dispersive branch in the WKB regime, and the time-domain simulation shows conversion into a **short-wavelength left-moving positive-comoving-frequency mode**. We have **not yet demonstrated excitation of a negative-comoving-frequency partner**.

---

## 1. Background flow and analog horizon

We use a one-dimensional stationary background velocity profile

$$
v(x)
=
-\left[
v_0
+
\frac{v_1}{2}
\left(
1+\tanh\frac{x-x_0}{w}
\right)
\right],
$$

with intrinsic long-wavelength wave speed

$$
c=1.
$$

The parameters used for the main simulations are

$$
v_0=0.25,\qquad
v_1=1.00,\qquad
x_0=2.0,\qquad
w=3.0.
$$

At long wavelength, the against-flow branch has group velocity

$$
v_g=v(x)+c.
$$

The continuum horizon is therefore defined by

$$
v(x_h)+c=0,
$$

which gives

$$
\boxed{x_h=3.64791843}.
$$

The background is stationary, so the **lab-frame frequency** $\omega$ is conserved along the scattering process.

---

## 2. Round 1 — nondispersive baseline

The first round deliberately used the nondispersive relation

$$
(\omega-vk)^2=c^2k^2.
$$

For the incident branch,

$$
\omega=(v+c)k,
$$

so at fixed lab frequency

$$
k(x)=\frac{\omega_0}{v(x)+c}.
$$

As the packet approaches the continuum horizon,

$$
v(x)+c\rightarrow0,
$$

and therefore

$$
v_g\rightarrow0,
\qquad
k\rightarrow\infty.
$$

The numerical experiments confirmed this behavior while the wavelength remained well resolved:

- the packet slowed as it moved into the stronger counter-flow;
- the local wavelength shortened;
- the measured $k(x)$ followed the WKB prediction;
- increasing numerical resolution allowed the calculation to approach the horizon more closely;
- the apparent cutoff moved with grid resolution, showing that it was numerical rather than physical.

This established the nondispersive baseline: **the continuum theory produces a divergent blueshift and no finite-$k$ escape mechanism.**

---

## 3. Why dispersion is needed

A dispersive analog-gravity calculation should replace the formal divergence with additional finite-$k$ structure.

A useful distinction emerged during development:

1. **Numerical dispersion** is created unintentionally by the spatial discretization.
2. **Physical dispersion** is part of the model and must remain fixed when the numerical grid is refined.

The numerical-dispersion experiments showed that a discretization alone can create an artificial finite-$k$ turning point and even an apparent reversal of group velocity. This made it essential to introduce a physical dispersion relation explicitly rather than rely on the computational lattice.

A lattice-inspired physical model was then explored as a separate dispersion model. It demonstrated the expected qualitative ingredients — multiple fixed-frequency roots and finite-$k$ turning — and was useful for understanding the mode topology.

For the main continuing calculation, however, we chose a controlled continuum dispersion relation that can be tuned independently of the numerical grid.

---

## 4. Round 3 — controlled stabilized dispersion

The intrinsic dispersion used in Round 3 is

$$
\omega'^2
=
c^2k^2
\left[
1-\left(\frac{k}{k_d}\right)^2
+
\gamma
\left(\frac{k}{k_d}\right)^4
\right],
$$

where

$$
\omega'=\omega-vk
$$

is the comoving frequency.

The chosen parameters are

$$
\boxed{k_d=6,\qquad \gamma=0.30}.
$$

The negative quartic term produces the desired subluminal bending at intermediate $k$, while the positive sextic term stabilizes the high-$k$ behavior so that $\omega'^2$ remains positive for all real $k$.

For the positive intrinsic-frequency branch,

$$
\omega'_+(k)
=
ck
\sqrt{
1-\left(\frac{k}{k_d}\right)^2
+
\gamma
\left(\frac{k}{k_d}\right)^4
},
$$

and the lab frequency is

$$
\omega(k,x)=v(x)k+\omega'_+(k).
$$

---

## 5. Uniform-flow validation

Before using the nonuniform tanh profile, the Round-3 solver was tested in uniform flow.

The validation case used

$$
v=-0.25,\qquad
k_0=1.5.
$$

The continuum nondispersive prediction would be

$$
v_g=v+c=0.75.
$$

The stabilized dispersion instead predicts

$$
v_{g,\mathrm{pred}}=0.65676049.
$$

The time-domain simulation measured

$$
v_{g,\mathrm{meas}}=0.65550439,
$$

corresponding to a relative error of only

$$
\boxed{0.191\%}.
$$

The carrier wavenumber remained essentially constant,

$$
k_{\mathrm{med}}=1.49999239,
$$

and the uniform-flow field-power diagnostic changed only at roundoff level.

This is an important validation: the solver does not merely reproduce the old continuum wave speed. It propagates the packet at the group velocity predicted by the **chosen physical dispersion relation**.

---

## 6. Packet propagation on the tanh ramp

The validated dispersive solver was then used with the full background profile.

The launch parameters were

$$
x_{\mathrm{launch}}=-12,
\qquad
k_0=1.5,
$$

giving

$$
v_{\mathrm{launch}}=-0.25008842,
$$

$$
\omega_0=1.07814357,
$$

and

$$
v_{g,\mathrm{launch}}=0.65667207.
$$

The numerical grid spacing was

$$
\Delta x=0.05.
$$

### 6.1 True local dispersive fold

The physical turning point is not defined by the continuum condition $v+c=0$. It is obtained from the simultaneous fixed-frequency conditions

$$
\omega(k,v)=\omega_0,
$$

and

$$
v_g(k,v)
=
\frac{\partial\omega}{\partial k}
=
0.
$$

For the present parameters this gives

$$
\boxed{
x_{\mathrm{turn}}=0.54933586
}
$$

with

$$
\boxed{
v_{\mathrm{turn}}=-0.52545768
}
$$

and

$$
\boxed{
k_{\mathrm{turn}}=3.43562439.
}
$$

Thus physical dispersion replaces the Round-1 divergent blueshift by a **finite-$k$ fold well before the continuum horizon**:

$$
x_{\mathrm{turn}}\approx0.55
<
x_h\approx3.65.
$$

### 6.2 WKB propagation before the interaction region

Before the finite packet enters the fold region, the measured dominant wavenumber follows the local fixed-frequency incident root well.

Restricting the comparison to the pre-conversion WKB region gave

$$
\boxed{\text{median relative }k\text{ error}=1.185\%.}
$$

The packet therefore behaves as expected while it remains approximately a single local mode.

![Incident WKB blueshift and onset of multi-mode behavior](../figures/round3_step3_figure_2_wavenumber.png)

### 6.3 The finite packet reverses before its global center reaches the local fold

The first zero crossing of the **global packet-center velocity** occurred at

$$
t\approx25.228,
$$

when the global center was at

$$
x\approx-0.485.
$$

This is upstream of the local WKB fold at $x\approx0.55$.

This is not interpreted as a contradiction. The packet has finite width in both position and wavenumber. Its leading and higher-$k$ components encounter the strongly dispersive region before the global envelope center reaches the turning point of the central ray. Once mode conversion begins, a single global packet center no longer represents one WKB trajectory.

The spacetime plot shows this transition directly: the incident packet compresses, short-wavelength structure develops near its leading edge, and an outgoing component begins to separate.

![Round 3 Step 3 spacetime evolution](../figures/round3_step3_figure_1_spacetime.png)

The shortest measured wavelength remained reasonably resolved. At the end of the run the dominant measured wavenumber was

$$
k\approx5.52,
$$

corresponding to approximately

$$
22.8
$$

numerical grid points per wavelength, safely above the 12-point resolution guard used in this calculation. The observed short-wavelength structure is therefore not occurring at the numerical grid cutoff.

---

## 7. Mode-resolved analysis

After the packet becomes multi-mode, a single Hilbert-phase estimate of $k$ is no longer sufficient. Round 3 Step 4 therefore analyzes localized spacetime windows and asks which fixed-frequency modes are actually populated.

Four windows were used:

- **incident:** before significant distortion;
- **pre-fold:** approaching the dispersive region;
- **interaction:** during the mode-conversion region;
- **outgoing:** after the global packet-center reversal.

![Localized spacetime windows](../figures/round3_step4_figure_1_windows.png)

Because the background is stationary, the conserved lab frequency is

$$
\omega_0=1.07814357.
$$

For each local flow velocity, all real roots satisfying

$$
\omega(k,v)=\omega_0
$$

were calculated. Each root was classified by

$$
\omega'=\omega_0-vk
$$

and by its lab-frame group velocity $v_g$.

The simulated field was then demodulated at $\omega_0$, giving a fixed-frequency spatial $k$-spectrum that can be compared directly with those roots.

---

## 8. What the mode analysis shows

### 8.1 Incident region

At

$$
x=-6,
\qquad
v=-0.254805,
$$

the relevant predicted incident root is

$$
k=1.5109,
\qquad
\omega'=+1.4631,
\qquad
v_g=+0.6506.
$$

The measured spectral peak is

$$
k_{\mathrm{meas}}=1.5630.
$$

This is the expected right-moving, positive-comoving-frequency incident mode.

### 8.2 Pre-fold region

At

$$
x=-2,
\qquad
v=-0.314969,
$$

the incident root is

$$
k=1.6675,
\qquad
v_g=+0.5700,
$$

and the measured peak is

$$
k_{\mathrm{meas}}=1.7357.
$$

Additional high-$k$ roots already exist in the local dispersion relation, but the time-domain field remains dominated by the incident branch.

### 8.3 Interaction region

At

$$
x=0,
\qquad
v=-0.458609,
$$

the low-$k$ incident root is

$$
k=2.3018,
\qquad
\omega'=+2.1338,
\qquad
v_g=+0.3236.
$$

The measured peak is

$$
k_{\mathrm{meas}}=2.3416.
$$

Thus even close to the interaction region, the incoming spectral component remains consistent with the local fixed-frequency dispersion relation.

### 8.4 Outgoing region: the key observation

At

$$
x=-3,
\qquad
v=-0.284445,
$$

the fixed-frequency spectrum contains two significant measured peaks:

$$
k_{\mathrm{meas}}\approx2.03
$$

and

$$
\boxed{k_{\mathrm{meas}}\approx6.72}.
$$

The short-wavelength peak is close to the predicted root

$$
\boxed{
k=7.0483,
\qquad
\omega'=+3.0830,
\qquad
v_g=-0.3898.
}
$$

This is a **high-$k$, left-moving, positive-comoving-frequency mode**.

That is the clearest current evidence of dispersive mode conversion:

$$
\boxed{
\text{incoming low-}k,\ v_g>0
\quad\longrightarrow\quad
\text{outgoing high-}k,\ v_g<0.
}
$$

![Fixed-lab-frequency mode content](../figures/round3_step4_figure_3_fixed_omega_modes.png)

The summary of predicted roots and observed spectral peaks shows the same transition.

![Predicted local roots and measured spectral peaks](../figures/round3_step4_figure_4_peak_summary.png)

The full localized $k$-$\omega$ spectra provide a complementary view. Because the background velocity changes across each finite spatial window, these plots are primarily qualitative; the fixed-$\omega_0$ spectra above are the cleaner quantitative diagnostic.

![Localized k-omega spectra](../figures/round3_step4_figure_2_k_omega.png)

---

## 9. What has and has not been established

The simulations now support the following statements.

### Established

1. **The nondispersive baseline is reproduced.**  
   An against-flow packet slows and blueshifts as $v+c\rightarrow0$.

2. **The Round-3 dispersion is an explicit physical model, not a grid artifact.**  
   Its scale $k_d$ and stabilizer $\gamma$ are independent of the numerical spacing $\Delta x$.

3. **The dispersive solver is quantitatively validated in uniform flow.**  
   The measured packet velocity agrees with the theoretical group velocity to about $0.2\%$.

4. **The incident packet follows the local fixed-frequency dispersive branch in the WKB region.**

5. **The controlled dispersion produces a finite-$k$ fold before the continuum horizon.**  
   For the present parameters,

   $$
   x_{\mathrm{turn}}\approx0.55,
   \qquad
   k_{\mathrm{turn}}\approx3.44.
   $$

6. **The time-domain solution becomes multi-mode in the turning region.**

7. **A short-wavelength outgoing mode is observed.**  
   Its measured wavenumber agrees reasonably with the predicted high-$k$, left-moving fixed-frequency root.

### Not yet established

The current Step-4 windows do **not** show excitation of a negative-comoving-frequency mode.

All roots relevant to the measured peaks in the sampled regions have

$$
\omega'>0.
$$

Therefore the present result demonstrates **dispersive mode conversion / reflection**, but it is not yet evidence of the positive/negative-frequency mode pair associated with the Hawking analog.

This distinction is important: a short-wavelength reflected mode is not automatically a negative-frequency partner.

---

## 10. Current physical picture

The current simulation can be summarized as follows.

A low-$k$, positive-comoving-frequency wave packet is launched against the flow. Because the background is stationary, its lab frequency remains fixed. As it moves into stronger counter-flow, its local wavenumber increases according to the dispersive fixed-frequency relation.

Unlike the nondispersive model, the blueshift does not continue indefinitely. The incident branch reaches a finite-$k$ fold where its local group velocity vanishes. Because the packet has finite width, its interaction with this region begins before the global envelope center reaches the central-ray fold.

The field then becomes multi-mode. Spectral analysis after the interaction reveals a short-wavelength component on a left-moving fixed-frequency branch. In the windows studied so far, both the incoming and converted outgoing modes have positive comoving frequency.

Schematically,

$$
\text{low-}k,\ \omega'>0,\ v_g>0
\quad\rightarrow\quad
\text{high-}k,\ \omega'>0,\ v_g<0.
$$

This is the stable numerical baseline from which the next stage can search specifically for conversion into negative-$\omega'$ modes.

---

## 11. Current status

The project is currently at:

$$
\boxed{\text{Round 3, Step 4a complete}}
$$

with the following validated chain:

```text
Round 1
  nondispersive horizon and blueshift baseline
        ↓
Round 2
  explicit study of lattice / numerical-dispersion effects
        ↓
Round 3 Step 1
  controlled stabilized dispersion and root topology
        ↓
Round 3 Step 2
  uniform-flow time-domain validation
        ↓
Round 3 Step 3
  WKB blueshift and finite-k fold on tanh ramp
        ↓
Round 3 Step 4a
  mode-resolved identification of high-k outgoing branch
```

The next physics question is now sharply defined:

> When the scattering region includes flow values for which negative-comoving-frequency fixed-$\omega_0$ roots exist, does the time-domain evolution populate those roots?

That is the next test required before making any claim about Hawking-like positive/negative-frequency mode conversion.

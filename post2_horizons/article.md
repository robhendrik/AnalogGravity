# Wave Horizons in Black Holes and Water Tanks

### *A wave approaches a point it cannot cross. Dispersion gives it more than one way forward — and one of those extra modes leads us surprisingly close to Hawking radiation.*

<!--
Purpose:
- Pixar arc in miniature.
- Once upon a time: a horizon simply stops a wave.
- Then: dispersion changes the rules.
- Because of that: one incoming wave can become several modes.
- One of those modes has negative co-moving frequency.
- Until finally: this connects to Hawking's positive/negative-frequency mixing.
- Ever since: analogous horizon physics has been explored in water, light and other wave systems.
-->

- Horizon as simple boundary: wave can no longer make progress against the flow.
- First simulation: packet slows, blueshifts, stalls.
- Add dispersion: several wave modes become possible.
- One mode has negative co-moving frequency.
- Tease Hawking connection without explaining it yet.

---

## Black Holes, White Holes, and Rivers

<!--
Purpose:
- Explain black-hole vs white-hole horizon.
- Establish moving-background viewpoint.
- Introduce white hole as the convenient forward-time version of Hawking's backwards-tracing argument.
- Set up the time-reversal idea early so it pays off later.
-->

- River flow increasing downstream.
- Black-hole analogue:
  - outside: upstream waves can still escape;
  - inside sufficiently fast flow: current carries everything downstream;
  - no upstream escape across the horizon.
- White-hole analogue:
  - reverse the process;
  - incoming upstream wave cannot enter fast-flow region.
- Black-hole and white-hole scattering related by time reversal.
- Preview Hawking:
  - start with an outgoing wave far from black hole;
  - follow it backwards toward horizon;
  - forward-time white-hole scattering gives an accessible analogue of that question.

<!--
FIGURE 1 — Black-hole and white-hole horizons

Suggested visual:
- Side-by-side river-style schematic.
- Left: black-hole analogue.
- Right: white-hole analogue.
- Same flow profile shown in time-reversed form.
- Show flow direction and wave propagation.

Caption:
**Figure 1 — A black-hole horizon and its time-reversed white-hole counterpart.**
In the black-hole case, waves inside the fast-flow region cannot escape upstream. Reverse the process and an incoming wave encounters a white-hole horizon it cannot cross. The white-hole version is especially convenient because we can launch a wave toward the horizon and watch the scattering process unfold.
-->

---

## Running Into a Horizon

<!--
Purpose:
- Show nondispersive case first.
- Establish intuitive horizon.
- Show packet slowing and blueshift.
- Introduce unlimited-shortening problem.
-->

- Assume one intrinsic wave speed $c$.
- Background flow $u(x)$ increases against direction of propagation.
- Launch localized packet.
- Laboratory-frame group velocity decreases.
- Wavelength becomes shorter.
- Near nondispersive horizon:
  - packet approaches zero lab-frame group velocity;
  - blueshift continues without limit in idealized model.
- Numerical version:
  - eventually grid scale matters.
- Physical version:
  - arbitrarily short wavelengths should make us suspicious of the approximation.

<!--
FIGURE 2 — Nondispersive packet approaching the horizon

Suggested visual:
- Animation or 4–6 snapshots.
- Packet moving toward white-hole horizon.
- Horizon position marked.
- Flow direction visible.
- Increasing compression clearly visible.

Caption:
**Figure 2 — A wave packet approaches a nondispersive white-hole horizon.**
The packet travels against an increasingly strong background flow. Its laboratory-frame group velocity decreases while its wavelength becomes shorter. In the nondispersive model nothing prevents this blueshift from continuing as the packet approaches the horizon.
-->

---

## Water Waves Do Not Have One Speed

<!--
Purpose:
- Recover only the dispersion intuition needed here.
- Previous post is helpful, but this section should still stand alone.
- Introduce our simulation as a simplified dispersive model without dwelling on its polynomial form.
-->

- Real waves are dispersive.
- Different wavelengths can have different:
  - phase velocities;
  - group velocities.
- Only fact needed from previous post:
  - wave-packet speed can depend on wavelength.
- Consequence:
  - blocking becomes wavelength-dependent;
  - one mode may stop where another can still propagate.
- Our numerical model:
  - approximately nondispersive at long wavelength;
  - bends strongly at shorter wavelength;
  - stabilizes again at high wavenumber.
- Purpose of model:
  - not to reproduce water quantitatively;
  - make dispersive mode conversion easy to see.

<!--
Optional technical note for GitHub / appendix rather than main prose:

For the simulation we use

$$
\omega'^2
=
c^2k^2
\left[
1-\left(\frac{k}{k_d}\right)^2
+\gamma\left(\frac{k}{k_d}\right)^4
\right].
$$

The final factor produces a stabilizing $k^6$ contribution at large $k$.
-->

---

## One Frequency, Several Waves

<!--
Purpose:
- Introduce multiple fixed-frequency modes.
- Do not make the exact number of roots the conceptual point.
- Reader only needs:
  one incoming mode,
  several possible outgoing modes,
  including positive- and negative-frequency branches.
-->

- Stationary background $\Rightarrow$ laboratory frequency $\omega$ conserved.
- Frequency relative to moving medium:

$$
\omega' = \omega - uk.
$$

- For fixed $\omega$:
  - $\omega'=\omega-uk$ is a straight line on an $\omega'(k)$ diagram.
- Curved dispersion:
  - straight line can intersect dispersion relation more than once;
  - one laboratory frequency can correspond to several wavelengths.
- Modes central to story:
  - incoming long-wavelength mode;
  - short-wavelength positive-frequency mode;
  - short-wavelength negative-frequency mode.
- Exact number of roots depends on dispersion relation and parameters.
- Our toy model also contains an additional reflected channel:
  - keep as technical detail;
  - not central to Hawking analogy.
- Real water-wave experiments often present the cleaner three-mode picture.

<!--
FIGURE 3 — One frequency, several wave modes

Suggested visual:
- Plot intrinsic $\omega'(k)$ dispersion.
- Add straight line $\omega'=\omega-uk$.
- Strongly highlight:
  - incoming long-wave root;
  - positive-frequency high-$k$ root;
  - negative-frequency high-$k$ root.
- Show any additional root faintly.
- Avoid making "four roots" the title or main message.

Caption:
**Figure 3 — Dispersion allows one laboratory frequency to correspond to several wave modes.**
For a stationary background, $\omega$ is conserved, so the allowed waves are found where $\omega'=\omega-uk$ intersects the intrinsic dispersion relation. The modes important for the Hawking analogy are an incoming long-wavelength mode and two short-wavelength branches with opposite signs of co-moving frequency. Our simplified numerical model contains an additional reflected channel, while water-wave experiments often focus on the three modes highlighted here.
-->

- Main transition:
  - horizon problem has become a scattering problem;
  - one incoming mode can feed several outgoing modes.

---

## Watching the Modes Appear

<!--
Purpose:
- Main simulation payoff.
- Show raw packet first.
- Then mode-resolved decomposition.
- Keep interpretation classical.
-->

- Repeat simulation with dispersion included.
- Incoming packet approaches blocking region.
- No unlimited compression.
- Instead:
  - amplitude transfers into other allowed modes.
- Raw field:
  - overlapping components;
  - interference makes individual branches hard to identify by eye.
- Mode-resolved analysis:
  - isolates positive-frequency short-wave branch;
  - isolates weaker negative-frequency short-wave branch.
- Additional reflected channel:
  - part of full numerical scattering;
  - not central to article's main visual story.

<!--
FIGURE 4 — Dispersive mode conversion

Suggested visual:
- Use final enlarged-domain + absorbing-boundary simulation.
- Panel a: outgoing-region $k$ spectrum.
- Panel b: raw spacetime field.
- Panel c: reconstructed negative-frequency branch.
- Panel d: reconstructed positive-frequency branch.
- Explicitly state any visibility boost applied to negative branch.

Caption:
**Figure 4 — Dispersion turns blocking into mode conversion.**
The incoming long-wavelength packet approaches the white-hole horizon, but instead of blueshifting without limit it excites additional dispersive modes. The raw field contains overlapping contributions, while the mode-resolved reconstruction separates the two short-wavelength branches central to the Hawking analogy. One has positive co-moving frequency and the weaker partner has negative co-moving frequency. Any amplification used to make the weaker branch visible is stated explicitly.
-->

- Important observations:
  - different wavelengths;
  - different group velocities;
  - one branch has $\omega'>0$;
  - one branch has $\omega'<0$.

---

## A Negative Frequency?

<!--
Purpose:
- Explain negative co-moving frequency classically.
- Preserve tension.
- Keep rhetorical question as major beat.
-->

- Negative frequency does not mean “negative oscillations per second.”
- Relevant quantity:

$$
\omega' = \omega - uk.
$$

- Sign refers to phase evolution in frame moving with medium.
- Positive- and negative-frequency modes:
  - both valid classical wave solutions;
  - nothing quantum has happened yet.

**Why should the sign of a frequency matter?**

---

## Following Hawking Back Toward the Horizon

<!--
Purpose:
- Explicit bridge to Hawking's original reasoning.
- Start with outgoing late-time packet.
- Trace it backwards.
- Show positive/negative-frequency decomposition near horizon.
- Pay off white-hole time-reversal setup from Figure 1.
-->

- Start far from black hole:
  - ordinary outgoing positive-frequency wave packet.
- Hawking's move:
  - propagate packet backwards toward horizon.
- Near horizon:
  - backwards-traced field contains both positive- and negative-frequency components.
- Link to our simulation:
  - one conserved lab frequency also leads to several modes;
  - one branch has $\omega'<0$.
- Key distinction:
  - systems are not physically identical;
  - same type of positive/negative-frequency mode mixing appears.
- Structural payoff:
  - forward-time white-hole scattering mirrors Hawking's backwards-tracing question.

<!--
FIGURE 5 — Hawking's wave packet traced backwards

Suggested visual:
- Three-stage conceptual illustration.
- Far away / late time:
  - one outgoing positive-frequency packet.
- Middle:
  - arrow labelled "trace backwards in time".
- Near horizon:
  - two components labelled positive frequency and negative frequency.
- Visually echo Figure 1 / white-hole simulation.

Caption:
**Figure 5 — Hawking's argument viewed as a backwards-traced wave packet.**
Begin far from the black hole with an ordinary outgoing positive-frequency wave packet. Tracing it backwards toward the horizon reveals both positive- and negative-frequency components. In forward time, the corresponding mode mixing is closely related to the conversion we can stimulate at a white-hole analogue.
-->

---

## Why the Sign Matters in Quantum Theory

<!--
Purpose:
- Answer question raised above.
- Introduce minimum QFT language.
- No full Bogoliubov derivation.
-->

- Classical field:
  - positive- and negative-frequency components are wave solutions.
- Quantized field:
  - positive-frequency modes associated with annihilation operators;
  - negative-frequency modes associated with creation operators.
- Therefore mode mixing becomes operator mixing.
- Consequence:
  - particle creation becomes possible.

$$
\text{mode conversion}
\rightarrow
\text{positive/negative-frequency mixing}
\rightarrow
\text{annihilation/creation mixing}
\rightarrow
\text{particle creation}.
$$

---

## Stimulated Versus Spontaneous Hawking Radiation

<!--
Purpose:
- State exactly what our simulation does and does not show.
- Preserve scientific distinction.
-->

- Our simulation:
  - deliberately inject classical incoming wave;
  - observe stimulated mode conversion.
- Water-wave experiments:
  - similarly stimulate conversion with incoming classical wave.
- Hawking's quantum result:
  - no incoming classical wave required;
  - incoming state can be vacuum;
  - positive/negative-frequency mixing becomes spontaneous particle creation.
- Common ingredient:
  - same underlying mode-mixing structure.
- Important limit:
  - simulation is not a black hole spontaneously emitting Hawking quanta.

<!--
FIGURE 6 — Stimulated versus spontaneous Hawking process

Suggested visual:
- Two matched panels.

Left:
- classical incoming wave;
- horizon;
- positive- and negative-frequency outgoing modes;
- label: stimulated mode conversion.

Right:
- vacuum input;
- horizon;
- outgoing Hawking quantum + partner;
- label: spontaneous Hawking emission.

Caption:
**Figure 6 — The same mode mixing has a classical and a quantum interpretation.**
In our simulation and in water-wave experiments, an injected classical wave stimulates conversion into positive- and negative-frequency modes. In Hawking's quantum calculation there need not be a classical incoming wave: after quantization, the same positive/negative-frequency mixing becomes spontaneous particle creation.
-->

---

## From a Simulation to a Water Tank

<!--
Purpose:
- Connect simplified simulation to real analogue-gravity experiments.
- Do not re-open detailed discussion of toy-model root count.
- Emphasize shared mode-conversion structure.
-->

- Our simulation:
  - deliberately simplified dispersion;
  - chosen to expose mode conversion.
- Real water:
  - gravity, depth and surface tension determine dispersion.
- Water-channel experiments:
  - long surface wave sent against varying current;
  - blocking region created by flow gradient / obstacle;
  - incoming wave converted into shorter-wavelength modes.
- Observed mode structure:
  - positive-norm outgoing branch;
  - negative-norm outgoing branch.
- Experimental papers commonly describe:
  - $k_{\mathrm{in}}^+$;
  - $k_{\mathrm{out}}^+$;
  - $k_{\mathrm{out}}^-$.
- White-hole geometry:
  - convenient experimental realization;
  - gives access to mode conversion underlying Hawking process.
- Keep caveat short:
  - numerical model is not quantitative water simulation;
  - shared physics is horizon scattering and positive/negative-frequency conversion.

---

## A Black Hole That Radiates

<!--
Purpose:
- Return to Hawking after all ingredients are established.
- Keep concise.
-->

- Far-away outgoing mode.
- Trace backwards:
  - positive + negative frequency near horizon.
- Quantize field:
  - mode mixing becomes particle creation.
- Far-away observer:
  - outgoing Hawking radiation.
- Ideal stationary black hole:
  - thermal spectrum.
- Energy carried away:
  - black hole can lose mass;
  - evaporation in principle.

---

## How Close Can a Water Basin Get?

<!--
Purpose:
- End with scope and limitation.
- Let closing question land cleanly.
-->

- Water tank is not a black hole.
- Background flow does not obey Einstein equations.
- Surface waves are not photons in curved spacetime.
- Our numerical model is even more abstract.
- What analogue systems can reproduce:
  - horizon kinematics;
  - dispersion;
  - blocking;
  - positive/negative-frequency mode conversion;
  - stimulated scattering.
- What they do not automatically reproduce:
  - full gravitational dynamics;
  - spontaneous quantum Hawking emission.

**How much of Hawking radiation belongs specifically to gravity — and how much belongs to horizons themselves?**

---

## References

<!--
Purpose:
Keep reference list focused.

Core references:
- Hawking original paper
- Unruh 1981
- Schützhold & Unruh 2002
- Rousseaux et al. 2008
- Weinfurtner et al. 2010 / 2013
- Leonhardt & Robertson 2012
- Barceló, Liberati & Visser review if broader background is needed

Specific sourcing decisions:
- Cite Hawking directly for backwards-traced positive/negative-frequency decomposition.
- Cite analogue-gravity literature for:
  - white-hole interpretation;
  - positive/negative norm;
  - stimulated mode conversion.
- Keep details of our exact toy dispersion and extra numerical root in:
  - figure caption;
  - methods note;
  - GitHub / simulation documentation.
- Main article should emphasize:
  dispersion -> several modes -> positive/negative frequency -> Hawking.
-->
# Hawking in your bathtub?

### We sent a wave toward a horizon it could never cross — and watched it turn into something that looks remarkably like Hawking radiation.

![Feature](Feature_image.png)
**Feature image** — Wave approaching a white-hole horizon. Image generated with PyVista by author.
*Alt text: Colored visualization of a wave approaching a white-hole horizon. The wave gets compressed near the horizon.*

A black-hole horizon is a point of no return. Cross it, and even light cannot get back out. This is the story we all know; a striking fact about spacetime. Nobody gets to walk up to a real horizon to see what happens.

But the equation describing a wave near a black-hole horizon is, mathematically, the same as the equation for a wave in a fast-flowing fluid. Can we use that to actually build a horizon? Take a channel of moving water, shape the flow, and create a boundary a wave cannot cross. With this, we can send a wave at the horizon and watch what happens.

In fact, scientists have been running this experiment, and what is observed reaches close to one of the most famous predictions in black-hole physics: Hawking radiation. This triggers the question: how much of that mechanism actually needs a black hole at all?

In this post, we are going to run that experiment too, in simulation, and watch what happens.

---

## Black Holes, White Holes.

Picture a wave that propagates at some speed relative to the medium it is travelling through, while the medium itself is also flowing. If that medium flows fast enough, somewhere the wave cannot keep up.

In the *black-hole* version of this story, the flow gets faster as we move inward. A wave sitting in the fast-flow region tries to escape outward, but the current is too strong. It cannot get out.

Now reverse the whole picture. Run the flow the other way, and the same boundary becomes a barrier from the outside instead: a wave approaching from the slow-flow side simply cannot get in. This is the *white-hole* version, and it turns out to be the more convenient one for us. We cannot place a detector inside a black hole and watch a wave fail to escape. But we can launch a wave toward a white-hole horizon from the accessible, slow-flow side, and watch what happens to it in real time.

![Figure_1](Figure_1.png)

**Figure 1 — Black-hole and white-hole horizons.** In a black-hole analogue, a wave in the fast-flow region cannot escape against the current. Reverse the process and we obtain a white-hole horizon: an incoming wave encounters a region it cannot enter. The white-hole version allows us to launch a wave toward the horizon and watch what happens. Image by author.

*Alt text: Side-by-side schematic of black-hole and white-hole analogue horizons. In the black-hole panel, the background flow points toward a fast-flow region and a wave trying to escape is blocked at the horizon. In the white-hole panel, the flow direction is reversed and an incoming wave approaching from the slow-flow side is blocked from entering the fast-flow region.*

So, that will be our experiment: send a wave against a current that gets stronger as it goes, and see what it actually does when it reaches the point it cannot cross.

## Send in the Wave

Let us start with the simplest version we can build: one wave speed relative to the water, no dispersion, and a flow that smoothly speeds up from slow to fast. Launch a wave packet from the slow-flow side, aimed straight at the horizon, and let it travel against the current.

At first, not much happens. The packet moves forward, more or less as it would in still water. But as the counter-current strengthens, its progress in the lab frame slows down — and its wavelength starts shrinking.

![Figure_2](Figure_2.gif)

**Figure 2 — A wave approaching a smooth white-hole horizon without dispersion.** The wave travels against an increasingly strong current. Its progress slows while its wavelength becomes shorter and shorter. In the simulation the wave eventually appears to disappear close to the horizon. Image by author.

*Alt text: Animation of a localized wave packet travelling toward a white-hole horizon through an increasingly strong opposing flow. The packet slows down and its oscillations become progressively shorter in wavelength near the horizon.*

Close to the horizon, the wave seems to vanish. This is because the numerical grid used for the simulation has a smallest wavelength it can represent, and the wave has shrunk past it. This is not a flaw we could fix with a finer grid. In the ideal, continuous version of this model, there is no smallest wavelength at all. As the horizon is approached, the group velocity heads to zero, and the wavelength heads to zero. Any grid, however fine, eventually runs out of resolution.

So, in the idealised version of this experiment, the wave never really stops — it just keeps blueshifting, forever, into shorter and shorter wavelengths as it nears the horizon. Nothing in the model itself puts a floor under how short that wavelength can get.

That is a warning sign. Push the calculation to arbitrarily short wavelengths, and sooner or later we will be making claims about scales where the theory cannot be trusted anymore.

This is an analog of the famous 'trans-Planckian problem', applied to a water wave.

> **The wave never really stops. It just keeps shrinking — forever, into wavelengths our model was never built to reach.**

---

## What If We Make the Horizon Sharp?

So far, we used a smooth ramp from slow flow to fast flow for the simulation. What happens if we make that transition abrupt instead?

![Figure_3](Figure_3.gif)

**Figure 3 — Reflection from a sharp nondispersive horizon.** When the change in flow becomes sufficiently abrupt, part of the incoming wave reflects before the numerical blueshift becomes arbitrarily large. This is ordinary scattering from a sharp background change within the same nondispersive mode structure; no additional wave components have yet appeared. Image by author.

*Alt text: Animation of a wave packet travelling toward a sharp white-hole transition. Part of the packet reflects back toward the slow-flow region while the background remains nondispersive.*

Something different happens; instead of blueshifting away into oblivion, part of the wave bounces straight back the way it came. The abruptness of the transition throws part of the wave backward. Note that this reflection does not give us any *new* type of wave. It is still the same single wave branch we started with, just travelling in the other direction. Nothing has appeared that was not already in our simple model.

A wave can be turned back by an abrupt horizon. That is reflection, nothing extraordinary. This will matter shortly. Once we let the wave itself become dispersive — where different wavelengths travel at different speeds — a sharp horizon will do something new: it will not just reflect the wave, it will convert it into wave components that were not there before.

---

## But Real Waves Do Not Have One Speed

Real water waves are dispersive (see our previous post on this topic). Different wavelengths do not all travel at the same speed. This matters. Go back to the runaway blueshift: in the idealised, nondispersive model, the wave's wavelength shrinks without limit as it approaches the horizon. Real water cannot actually do that; at some scale, the simple picture of a smooth fluid surface simply stops applying. Dispersion is not an inconvenient complication we are choosing to add — it is what any real medium does once you push it to short enough wavelengths.

So dispersion is, in a very concrete sense, water's own way of avoiding the trans-Planckian problem. The wave never actually needs to reach zero wavelength, because somewhere along the way, the physics changes. That raises the question of which dispersion relation to use — and here water offers no special authority. Its dispersion relation is just one physically reasonable cutoff among many.

That is the point: for a real white-hole horizon, we do not know what the dispersion relation is. What we do in our simulation is pick one reasonable dispersion relation, run the experiment, and ask which features of the process survive.

> **The point is not that water has the right microscopic physics. The point is that we do not know the right microscopic physics — so we can ask what survives when we change it.**

This turns out to be a well-studied question, and the answer is reassuring. Push the same wave-equation-near-a-horizon problem through several completely different high-frequency cutoffs — water's own gravity-capillary dispersion, a lattice-like quartic modification, even a laser pulse propagating through a nonlinear dielectric medium — and the same qualitative mode-conversion behaviour keeps showing up. Unruh and Schützhold went as far as naming this the 'universality' of the effect.
---

## Turn On Dispersion
Let us go back to the sharp horizon from a few sections ago, but this time give the wave a real dispersion relation — one where the propagation speed actually depends on wavelength.

To see why that changes anything, it helps to look at the dispersion curve itself, rather than the wave directly.

![Figure 4](Figure_4.png)
**Figure 4 — One lab frequency, different allowed modes.** The blue curve shows the co-moving dispersion relation used in the simulation, while the red line represents the same conserved laboratory frequency at two local flow speeds. In the upper panel, the flow is still subcritical and the relevant roots lie on the positive-frequency side. In the lower panel, after the flow has become supercritical, two negative-frequency roots and one positive-frequency root are available. The fixed labels k₁ to k₅ refer to branches of the dispersion curve, so the same label identifies the same branch in both panels. Image by author.

*Alt text: Two stacked dark-background dispersion plots showing co-moving frequency ω′ versus wavenumber k. In both panels, a blue sixth-order dispersion curve is intersected by a red straight line representing one fixed laboratory frequency. The upper panel, at local flow u = −0.523, has three intersections labeled k₃, k₄, and k₅, all at positive ω′. The lower panel, at u = −0.700, has three intersections labeled k₁, k₂, and k₅; k₁ and k₂ lie at negative ω′, while k₅ lies at positive ω′.*

The red line is the wave's laboratory frequency seen by a co-moving observer; it is the graphical representation of the Doppler effect. The blue curve is the dispersion relation used in our simulation, as seen by this observer. Where the red and blue lines cross, a wave can exist with frequency ω′ in the moving frame and wavenumber *k*. Remember: the wavenumber is inversely related to the wavelength, *k* = 2π/λ, so larger |*k*| means a shorter wavelength. 

In both panels the incoming wave is represented by mode k₃. The top panel shows the flow just before the incoming branch reaches its blocking point: k₃ is still a real solution, sitting close to a neighbouring root k₄. As the flow becomes faster, those two roots move together until the red line becomes tangent to the dispersion curve. At that point their lab-frame group velocity is zero. Beyond it, shown in the bottom panel, k₃ and k₄ are gone — they have merged and disappeared, exactly the blocking mechanism from our first post.

But the laboratory frequency is conserved, and the bent dispersion curve still allows other solutions. Two roots now appear elsewhere on the curve, k₁ and k₂, both with negative ω′. A third root, k₅, exists on the steep positive-frequency branch in both panels, although its wavenumber shifts as the flow changes.

So, launch the same kind of wave packet at the same sharp horizon, only now with this dispersion switched on.

![Figure_5](Figure_5.gif)

**Figure 5 — Wave approaching a sharp horizon with dispersion.** Once wave speed depends on wavelength, the blueshift changes the propagation itself. Near the blocking region the incoming packet converts into additional wave components. One returns toward the slow-flow region, while another mode can continue into the fast-flow side of the white-hole horizon. Image by author..

*Alt text: Animation of a dispersive wave packet approaching a sharp white-hole horizon. As the incoming packet reaches the blocking region, shorter-wavelength components appear. One propagates back toward the slow-flow region while another component continues through the horizon into the fast-flow region.*

In the nondispersive case before the wave either disappeared or bounced straight back. Here, something new comes out the other side. The horizon has not simply reflected the wave. It has changed it into other waves.

---

## One Frequency, Several Waves

So, that is the mechanism: because the flow is steady, the wave's laboratory-frame frequency ω stays fixed all the way to the horizon. In a nondispersive medium, that would pin down a single wavenumber, and nothing more could happen. But the moment the dispersion curve bends, a fixed ω can correspond to several different *k* at once — and as the flow changes, which roots exist, and how many, can change too.

That is exactly what Figure 4 showed us. The incoming root vanished once the flow went supercritical, and two new roots, *k₁* and *k₂*, appeared in its place — both with negative ω′.

What does a negative comoving frequency actually mean?

Not that the wave is somehow travelling backwards, or that its wavelength has gone negative. ω′ is simply the frequency this wave would be measured to have by an observer moving with the water. For *k₁* and *k₂*, that measured frequency comes out negative. The wave is still an entirely ordinary, real, classical solution of the wave equation — it oscillates, it carries energy, it looks like any other ripple if you just watched it go by. The only strange thing about it is what a co-moving observer would call its frequency.

Note that this sign is not just bookkeeping. In the conserved inner product that governs how these wave amplitudes combine, a negative-ω′ mode carries negative norm. We are not going to need the details of that inner product here — but the sign itself is going to matter a great deal once we get to the quantum version of this story.

One caveat before we move on. Our simulation's dispersion relation happens to produce four roots at once (*k₁*, *k₂*, *k₄*, *k₅* across the two panels — *k₃* was the incoming wave itself). That particular number is a feature of the toy dispersion we chose for this simulation, not a universal fact about horizons. Real water-tank experiments typically discuss three relevant counter-propagating roots. The physics we care about — a positive-norm and a negative-norm partner appearing together — is the same either way; the extra root is just our model's own bookkeeping.
---

## Are These Really the Modes?

The animation is suggestive — a strong outgoing wave, a fainter one trailing behind it — but by itself, it does not tell us what we are actually looking at. Short wavelengths are exactly where numerical artifacts like to hide. Before we trust this as physics, we should check it against what Figure 4 actually predicted.

A first, easy check: running the simulation at higher spatial resolution does not make the short-wave structure disappear or shift. It sits at the same physical wavelength either way, so it is not just grid noise.

The more interesting check is in the spectrum itself.

![Figure_6](Figure_6.png)
**Figure 6 — Outgoing spatial spectrum compared with the predicted roots.** The measured spatial spectrum in the outgoing region is shown together with the predicted wavenumbers k₁, k₂, and k₅ for the local flow. Two clear peaks appear at k₁ and k₅, while no comparable peak is seen at k₂. This shows that the outgoing field is dominated by the negative-norm partner and the high-k positive-norm branch. Image by author.

*Alt text: Dark-background plot of power versus wavenumber k. Three dashed vertical lines mark the predicted roots k1, k2, and k5. The measured spectrum shows a strong peak near k5, a weaker peak near k1, no substantial peak near k2, and a small, unlabeled feature near k=0.*

Two things stand out. The dominant peak sits exactly at *k₅* — no surprise, that is where most of the energy goes. But there is also a smaller, clearly visible peak at *k₁*, right where Figure 4 said the negative-norm partner should be. The mathematically allowed k₂ root, by contrast, is essentially unpopulated: whatever mechanism launches *k₁* and *k₅* evidently does not favour *k₂*.

There is also a small, weak feature near *k* = 0 that does not line up with any predicted root. This is an ordinary spatial spectrum, taken over a finite window in both space and time — and a finite, localized packet in a finite window will always leak a little power into wavelengths that are not conserved-frequency solutions at all. So this feature does not necessarily mean anything is wrong; it just means Figure 6 alone is not a strict enough test.

That stricter test is a projection onto the one conserved quantity we actually trust: the original launch frequency, ω₀.

![Figure_7](Figure_7.png)
**Figure 7 — Exact projection onto the launch frequency ω₀.** This spectrum is obtained by projecting the outgoing signal onto the original laboratory frequency ω₀. The dominant peak at k5 is accompanied by a weaker but clearly visible peak at k1, showing that the negative-norm partner is present at the same conserved laboratory frequency. The predicted k2 root remains essentially absent. Image by author.

*Alt text: Dark-background plot of power versus wavenumber k after exact projection onto frequency ω₀. Dashed vertical lines mark k1, k2, and k5. A large peak appears at k5 and a smaller peak at k1, while the spectrum stays near the floor around k2.*

The *k* = 0 feature is gone. Projected exactly onto ω₀, only *k₅* and *k₁* survive — precisely the two roots Figure 4 predicted, and nothing else. That is the strongest evidence we have: the weak partner mode is not stray numerical content, because it passes a test that stray content does not.

We can also just look at the waves themselves, filtered by root.

![Figure_8](Figure_8.png)
**Figure 8 — Mode-filtered reconstruction of the two outgoing components.* The outgoing field is filtered around the two observed roots to reconstruct the corresponding wave components in space and time. The top panel shows the weak negative-norm mode, displayed with amplified contrast, while the bottom panel shows the dominant positive-norm mode. This makes the missing partner directly visible in the data rather than only in a spectrum. Image by author.

*Alt text: Two stacked space-time panels on a dark background. The top panel shows a faint striped wave pattern labeled as the negative-norm mode and displayed with boosted amplitude. The bottom panel shows a stronger striped wave pattern labeled as the positive-norm mode. A horizontal color bar indicates filtered wave amplitude.*

Filter the raw field around *k₁* and around *k₅*, and both come back as clean, ordinary-looking wave packets — not noise dressed up to look like a signal.

Note that we should not expect every mathematically allowed root to show up with equal strength. The scattering process determines how much energy goes where, and *k₂* simply gets very little of it in this run. What matters is that the two modes we do see land exactly where predicted, and survive the strictest test we can throw at them.

---

## This Is Not Just A Simulation

Everything so far has happened inside a computer. It is worth pausing to ask: has anyone actually done this with real water?

They have.

Schützhold and Unruh were the first to propose shallow-water surface waves as a genuinely controllable analogue system for this physics — accessible, tunable, and, unlike an astrophysical black hole, something you could actually build on a lab bench.

Rousseaux and colleagues put that proposal into practice. In a water tank, they sent long surface waves toward a horizon and observed exactly the conversion we have just been watching in simulation: an incoming positive-frequency wave partly converting into a negative-frequency component. They described this mixing as the classical mechanism underlying the Hawking process.

Weinfurtner and colleagues took this further still. By placing a streamlined obstacle in an open channel, they created a genuine white-hole horizon — a region where the flow speeds up enough to block incoming waves, on the lee side of the obstacle, just like our simulated horizon. Long waves sent upstream toward that region were blocked and converted into short, dispersive waves, with amplitudes at the converted frequencies. They called this the stimulated Hawking emission of a white hole, and measured it directly.

Note the word stimulated. Both experiments, like our simulation, start by deliberately sending a wave in. The horizon then does the converting. That distinction — stimulated versus something needing no input wave at all — is going to matter a great deal in a moment.

---

## Nice — But What Does This Have to Do With a Black Hole?

So far we have learned something rather interesting about waves in flowing water. But a black hole in deep space contains neither water nor a wave generator.

> **What does any of this actually have to do with a black hole?**

Here is Hawking's own argument, stripped to its essentials. Take a wave packet detected far from the black hole, long after anything interesting has happened. Instead of asking where it goes, ask where it came from: trace it backwards in time, back toward the horizon.

As that traced-back packet approaches the horizon, something dramatic happens to it. It gets squeezed and blueshifted, its wavelength shrinking without limit — exactly the runaway blueshift we met all the way back near the start of this post. And when you express that shrinking packet not in the distant observer's frame, but in the frame of someone falling freely across the horizon, it no longer looks like a single wave. It splits into two pieces: one with positive frequency, one with negative frequency, in that free-falling frame.

That splitting is the heart of Hawking's calculation.

Now, reverse the movie.

Recall Figure 1: a black hole is a white hole, run backwards in time. So tracing an outgoing wave backwards toward a black-hole horizon is, played the other way, exactly a wave scattering forwards off a white-hole horizon — which is precisely the experiment we have been running all along, and precisely what Rousseaux's and Weinfurtner's water tanks actually built.


![Figure 9](Figure_9.png)
**Figure 9 — Hawking's argument viewed backwards in time.** An outgoing wave packet detected far from the horizon can be traced backwards in time. Near the horizon, its precursor contains both positive- and negative-frequency components relative to a freely falling observer. Reversing this picture gives the corresponding white-hole scattering process used in analogue-gravity experiments. Image by author.

*Alt text: Dark-background spacetime diagram with time increasing upward and distance from the horizon along the horizontal axis. A dashed vertical line marks the horizon. A blue outgoing wave packet at late time is traced backwards toward the horizon, where it separates into a cyan positive-frequency precursor and a red negative-frequency precursor.*

So, the positive- and negative-frequency split we found sitting in our own dispersive simulation — *k₅* and *k₁* in Figure 4 — is not a coincidence, and it is not merely similar to what happens near a black hole. Run the tape backwards, and it is the same splitting, in the same place, for the same reason.
---

## From Negative Frequency to Particle Creation

Classically, positive- and negative-frequency pieces are just two flavours of an ordinary wave. Nothing quantum has happened by simply splitting one into the other — we saw exactly that back when k₁ and k₂ first appeared in our simulation.

Quantizing the field changes what that split means.

In quantum field theory, positive-frequency modes are paired with annihilation operators, and negative-frequency modes are paired with creation operators. A process that mixes the two — the way our horizon mixes k₅ and k₁, the way Hawking's backwards-traced packet mixes into positive and negative pieces near a black hole — is therefore not just reshaping a waveform. It is mixing creation and annihilation operators together.

That has a strange consequence. The definition of "no particles present" before the mixing is no longer the same as the definition of "no particles present" after it. Once those two definitions disagree, particle creation becomes possible even starting from what looked like empty space.

> **Classically, we see mode conversion. Quantize the same field, and positive/negative-frequency mixing becomes particle creation.**

This is the step that turns a classical scattering problem into Hawking radiation.

## Did We Just Make Hawking Radiation?

No.

Our simulation began with an incoming classical wave that we chose to send in. The water-tank experiments do exactly the same — a wave generator deliberately supplies the incoming signal, and the horizon scatters it. This is stimulated mode conversion.

A real black hole needs no such push. Even starting from the vacuum, with no incoming wave at all, the same positive/negative-frequency mixing still happens to the quantum field — and the quantum state itself supplies what gets converted. That is spontaneous emission, and it is what Hawking actually predicted.

Stimulated and spontaneous processes share the same underlying mode mixing, which is exactly why measuring the classical, stimulated version is worth doing. We have not built an evaporating black hole in a water tank. We have built something that probes one of the mechanisms that makes Hawking radiation possible in the first place.
---

## How Close Can a Water Basin Get?

A water tank is not a black hole. Its flow does not obey Einstein's equations. Its surface waves are not photons escaping curved spacetime. And our numerical model is more abstract again — its dispersion relation was chosen to expose mode conversion clearly, not to match any particular real fluid.

So, what has this experiment actually shown us?

What it reproduces is real: horizon kinematics, the runaway blueshift of the nondispersive approximation, the way modified high-frequency dispersion tames that blueshift, positive/negative-frequency mode conversion at the horizon, and stimulated scattering that behaves exactly as the water-tank measurements found.

What it does not reproduce is just as real: the dynamics of spacetime itself, the full quantum state around an astrophysical black hole, and spontaneous emission from the vacuum.

The interesting point is perhaps not that our analogue has the "right" short-distance physics. We do not know what the right short-distance physics of spacetime actually is — nobody does. What analogue systems let us do instead is alter that unknown physics deliberately, on purpose, and watch what survives the change. We saw earlier that, across water, lattice-like dispersion, and even light in a nonlinear medium, the same mode-conversion mechanism keeps showing up. That robustness holds under suitable assumptions, in the models studied so far — it is not a proof that whatever real spacetime does at short distances behaves the same way. Whether an actual black hole satisfies those assumptions remains genuinely open.

There is also a much more mundane obstacle to observing the real thing. For a stellar-mass black hole, the predicted Hawking temperature sits far below the temperature of the cosmic microwave background surrounding it — so even if nothing else stood in the way, the radiation would be swamped before it could ever be measured directly.

Which leaves analogue experiments, water tanks among them, as some of the closest working routes we currently have to the physics behind Hawking's prediction.

So, we are back to the question this post opened with, sharper now than it was at the start: how much of that mechanism actually needs a black hole at all?

**How much of Hawking radiation belongs specifically to gravity — and how much belongs to horizons themselves?**

---

## References
References
1. S. W. Hawking, "Particle Creation by Black Holes." Communications in Mathematical Physics 43, 199–220 (1975).
2. W. G. Unruh, "Experimental Black-Hole Evaporation?" Physical Review Letters 46, 1351–1353 (1981).
3. R. Schützhold & W. G. Unruh, "Gravity Wave Analogues of Black Holes." Physical Review D 66, 044019 (2002).
4. G. Rousseaux, C. Mathis, P. Maïssa, T. G. Philbin & U. Leonhardt, "Observation of Negative-Frequency Waves in a Water Tank: A Classical Analogue to the Hawking Effect?" New Journal of Physics 10, 053015 (2008).
5. S. Weinfurtner, E. W. Tedford, M. C. J. Penrice, W. G. Unruh & G. A. Lawrence, "Measurement of Stimulated Hawking Emission in an Analogue System." Physical Review Letters 106, 021302 (2011).
6. U. Leonhardt & S. Robertson, "Analytical Theory of Hawking Radiation in Dispersive Media." New Journal of Physics 14, 053003 (2012).
7. C. Barceló, S. Liberati & M. Visser, "Analogue Gravity." Living Reviews in Relativity 14, 3 (2011).
8. T. Jacobson, "Introduction to Quantum Fields in Curved Spacetime and the Hawking Effect." Lecture notes (2004).
9. M. F. Linder, R. Schützhold & W. G. Unruh, "Derivation of Hawking Radiation in Dispersive Dielectric Media." Physical Review D 93, 104010 (2016).
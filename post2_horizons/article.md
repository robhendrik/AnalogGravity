# The SpeedS of Light

## How Dispersion Connects Rainbows to Hawking Radiation

![FEATURE IMAGE — SEVERN BORE](figures/feature_image.jpg)

> **Feature image.** A tidal bore travelling upstream on the River Severn (Gloucestershire, UK). Photo: Jamie Cooper/Galaxy / Alamy Stock Photo.

*Alt text: A large tidal bore propagating upstream along the River Severn, forming a distinct moving front across the river. Photo: Jamie Cooper/Galaxy / Alamy Stock Photo.*

A wave has a speed — or so it seems. Measure the wavelength, count how often the crests pass, multiply. That simple picture is enough for most of what we meet in daily life.

For the wave trying to travel upstream in the photo above, though, the current carries the water one way while the wave tries to travel the other. If the current becomes strong enough, can the wave simply stop?

Interestingly enough, this question takes us close to black-hole physics. Waves moving through flowing water can obey much the same mathematics as waves near a black-hole horizon. Push the analogy further, and we can reproduce some of the classical physics behind Hawking radiation — in a water basin.

In this post, we will discuss what we actually mean by the speed of a wave, and why, once the medium itself starts moving, that question stops being so simple.

So before we get anywhere near a black hole, we need to look more carefully at a simple question:

> **What do we actually mean by the speed of a wave?**

## The Speed of a Wave

Back in school, waves seemed simple.

Draw a sinusoid. Measure its wavelength. Count how often the crests pass. From wavelength and frequency, we get a speed.

For a sinusoidal wave, that speed is the **phase velocity**. We get it by multiplying frequency and wavelength, though the more common notation divides ω (the frequency times 2π) by the wavenumber $k$ (2π divided by the wavelength):

$$
v_{\text{phase}} = \omega/k
$$

It tells us how fast a point of constant phase — a crest, say — moves through space.

For most of the waves we meet early on, that is all we need. The wave moves, its crests move with it, and there seems little reason to ask what we even mean by the speed of the wave.

Note that this only holds because we quietly assumed one thing: that the wave is a single, infinite sinusoid. Real waves rarely are.

## When Crests and Packet Part Ways

Real waves are rarely infinite sinusoids. They come in pulses, bursts and packets. In a non-dispersive medium — where the phase velocity does not depend on frequency — these packets travel at the same speed as the phase.

![Figure 1](figures/figure_1.gif)

**Figure 1. Phase and group velocity are the same in a nondispersive medium.** A wave packet travels without changing shape because the carrier oscillations and the packet envelope move together: group velocity equals phase velocity.

*Alt text: Animation of a blue sinusoidal wave packet with a white envelope moving from left to right without changing shape. The carrier crests remain locked to the envelope, illustrating equal group and phase velocity.*

In a dispersive medium, this can be different. The crests can run forward through the packet, or the packet can overtake its own crests.

![Figure 2](figures/figure_2.gif)

**Figure 2. Dispersion separates phase velocity from group velocity.** Top: two wave packets in which the carrier oscillations move at a different speed from the envelope. On the left, group velocity is smaller than phase velocity; on the right group velocity is higher. Bottom: the corresponding dispersion curves. The phase velocity is ω/k, while the group velocity is the local slope, dω/dk.

*Alt text: Four-panel figure. The top-left animation shows a blue carrier wave moving faster than its white envelope, so group velocity is smaller than phase velocity. The top-right shows the envelope moving faster than the carrier, so group velocity is larger than phase velocity. The two lower panels show the corresponding curved omega-versus-k dispersion relations, with a short tangent at the selected point indicating the group velocity.*

So the packet has its own velocity, distinct from the phase velocity: the **group velocity**:

$$
v_{\text{group}} = d\omega/dk
$$

## The Shape That Determines How Waves Move

That derivative has a geometric meaning, and it is worth making concrete.

Plot frequency ω vertically and wavenumber $k$ horizontally. Every possible sinusoidal wave the medium can support becomes a single point on a curve — the dispersion relation.

From that one curve, both velocities fall out almost for free. The phase velocity is the slope of the straight line connecting that point to the origin. The group velocity is the slope of the line tangent to the curve at that same point — the line that just touches the curve there and matches its local direction.

So, in the boundary case where the dispersion relation is itself a straight line through the origin, those two lines are the same line. Phase velocity and group velocity coincide, exactly as we saw for the non-dispersive packet in Figure 1.

Bend the curve, and the two lines pull apart.

Note that this is really all dispersion is, geometrically: a curved ω($k$). If there is no bending, there is no dispersion, and there will be no distinction between the speed of the crests and the speed of the packet.

That one geometric idea — a straight line through the origin against a tangent line — will carry us through the rest of the story.

## Why Rainbows Exist

One of the great insights of nineteenth-century physics was that the speed of light in vacuum is a constant. In a medium, however, different colours travel at slightly different speeds — which is exactly the kind of dispersion we have just been building up.

The refractive index of glass depends on frequency. Different colours therefore propagate at different phase velocities through it, which is why a prism separates white light into a spectrum.

A rainbow adds some extra physics on top — refraction, reflection inside water droplets, geometry — but its colours ultimately come down to the same fact: the phase velocity of light in glass, and in water, varies with wavelength. We see the consequences of dispersion every time white light breaks into colour.

> **The crests and the wave packet do not have to travel at the same speed.**

## Dispersion Curves Come in Many Shapes

Different physical systems produce remarkably different dispersion curves, and it is worth walking through a few to see how much the shape of that curve actually tells us.

An ideal, continuous string or rope is essentially non-dispersive — a straight line through the origin, phase and group velocity locked together. Add discrete masses along it, like beads on a rope, and the curve bends: the discreteness of the beads places a limit on the waves the chain can carry, and the curve eventually reaches a maximum frequency it cannot exceed.

For surface waves on water, two different mechanisms compete to set the wave speed. Gravity pulls the surface flat; surface tension does too, at short wavelengths. So, where gravity and surface tension trade off against each other, water waves reach a minimum phase velocity — the crossover point between the long gravity waves we associate with the ocean and the short capillary waves that ripple across a puddle.

Even a free quantum particle has a dispersion relation. For a de Broglie wave, the frequency grows with the square of the wavenumber, producing an upward-curving parabola. Remarkably, the velocity we associate with the particle itself is the group velocity of its wave packet, not the phase velocity of the underlying oscillations.

Different physics. Different curves. But the idea stays the same: the shape of the dispersion relation determines how waves move.

For what comes next, we need a medium with one more property on top of dispersion. The medium itself has to move. So let's go back to water, and see what happens once it starts to flow.

## Water Waves

For surface gravity waves on water of depth h, ignoring surface tension for the moment, the dispersion relation is

$$
\omega^2 = gk\tanh(kh)
$$

The exact formula matters less here than the shape it produces. At long wavelengths in shallow water, the curve is nearly straight — phase and group velocity almost coincide, and the water behaves almost like our non-dispersive rope from a few sections back. At shorter wavelengths the curve bends, and the two velocities separate.

So water gives us a familiar, everyday medium with a genuinely nonlinear dispersion curve. And, unlike glass or a rope, we can make it flow.

## Waves in the River

In the photo at the top of this post, we see the Severn bore — a tidal bore, a moving front shaped by the tide pushing upstream against the current. In the nineties I actually got the chance to ride it upstream in a canoe. I did not last very long on it, but watching that wave approach slowly against the flow, and having it lift the canoe as it passed, is not something you forget.

So, the river gives us a moving medium, and that changes something fundamental about how we describe a wave on it.

Imagine standing on the bank. We measure a wave with frequency ω and wavenumber *k*. Now imagine someone drifting along with the water instead — maybe because they just fell off their surfboard. That person measures a different frequency, ω′. If the water itself moves at velocity *u*, the two are related by a Doppler shift:

$$
\omega' = \omega - uk
$$

Note that this shift depends on *k*, so different wavelengths get shifted by different amounts. Nothing about the intrinsic water-wave physics has changed. In the frame moving with the water, the dispersion curve therefore stays exactly as it was. What changes is the relation between the co-moving frequency ω′ and the fixed frequency ω measured from the bank. Graphically, that relation becomes a straight line whose slope depends on the flow velocity *u*.

In Figure 3 we show both views side by side: the dispersion curve as seen by the bystander on the bank, and the same physics as seen by the observer drifting with the current.

## One Frequency, Several Waves

![FIGURE 3](figures/figure_3.gif)

**Figure 3. The same moving medium viewed in two frames.** Left: in the laboratory frame, the frequency ω is fixed while the dispersion curve changes as the flow speed $u$ changes. Right: in the locally co-moving frame, the intrinsic water-wave dispersion stays fixed while the same conserved laboratory frequency appears as the tilted line ω′ = ω − *uk*. The white dots mark the same allowed modes in both views.

*Alt text: Two animated dispersion plots shown side by side. In the laboratory-frame panel, a blue dispersion curve tilts and changes with flow speed while a red horizontal frequency line stays fixed. In the co-moving-frame panel, the blue water-wave dispersion curve stays fixed while a red straight line tilts as the flow speed changes. White dots mark the intersections in both panels, and the displayed flow speed passes through zero.*

So, in Figure 3 we see something worth pausing on: for a wave in flowing water, the line representing the frequency measured by a co-mover — ω′ — does not cross the dispersion curve just once. It can cross it several times.

![Figure 4](figures/figure_4.png)

**Figure 4. One frequency can correspond to several wave modes.** For a fixed laboratory frequency, the allowed wavenumbers are the intersections between the intrinsic water-wave dispersion relation and the Doppler-shifted line ω′ = ω − *uk*. Here there are three real solutions, k₁, k₂, and k₃: three distinct wave modes at the same laboratory frequency.

*Alt text: Static omega-prime-versus-k dispersion plot. A blue curved water-wave dispersion relation is crossed by a red straight Doppler-shifted line. Three white intersection points are labelled k1, k2, and k3, showing that one fixed laboratory frequency can correspond to three different wavenumbers.*

Each intersection between the ω′-line and the dispersion curve is a genuine, allowed wave. All three share exactly the same frequency in the laboratory frame — but they have different wavelengths, different phase velocities, different group velocities, and even different directions of propagation.

The assumption we quietly started this post with has broken.

> **One frequency does not necessarily mean one wave.**

## A Negative Frequency That Is Still a Real Wave

There is a surprise hiding among those intersections in Figure 4.

Remember that *k₁*, *k₂* and *k₃* all correspond to the same frequency ω for the bystander on the bank. But for the co-moving observer, something odd happens to one of them:

ω > 0, while ω′ < 0.

The wave has not somehow acquired a negative amplitude. Nor is it running backwards in time. The sign just tells us how its phase evolves in a particular reference frame — for that one mode, the co-moving observer sees the phase turning the 'wrong' way compared to the bystander.

Our waves are still entirely classical here — nothing quantum has entered the picture yet. But note that this distinction, between positive- and negative-frequency modes, will turn out to matter a great deal once we reach the analogue of Hawking radiation.

## Where the Modes Meet

So far we have made one important simplification: our river has been flowing everywhere at the same speed.

Now imagine that the current changes as we move along the river — slower upstream, faster downstream, say. The laboratory frequency ω stays fixed, but u now varies with position, so the Doppler line in Figure 4 no longer sits still. As we move along the river, it sweeps across the dispersion curve, and the intersection points sweep with it.

Two of them can drift toward each other, and eventually meet.

What happens then is worth spelling out, because it is not just a mathematical curiosity. Once the flow gets fast enough, those two intersections merge into one and then vanish altogether — there is simply no real k left that solves the equation. The wave has nowhere to go. And just as the two modes merge, something striking happens: the group velocity of the wave relative to the water exactly balances the opposing current. Its group velocity measured from the bank is zero. The packet has come to a standstill.

> **A wave can still move through the water while standing perfectly still relative to the bank.**

So, we have now encountered two ingredients that also feature in Hawking's analysis of black holes: negative frequencies, seen from the perspective of a co-moving observer, and a wave that stalls and simply cannot propagate any further. We have not done anything quantum or relativistic yet — this is all still classical water on a classical river. But it is hard not to wonder to what extent this point, where a wave trying to flow upstream stalls, is a true horizon.

That is where we will continue next time.

## References

1. Brillouin, L. *Wave Propagation and Group Velocity*. Academic Press, 1960.

2. Lighthill, M. J. *Waves in Fluids*. Cambridge University Press, 1978.

3. Ashcroft, N. W. & Mermin, N. D. *Solid State Physics*. Holt, Rinehart and Winston, 1976.

4. Hawking, S. W. "Particle Creation by Black Holes." *Communications in Mathematical Physics* **43**, 199–220 (1975).

5. Unruh, W. G. "Experimental Black-Hole Evaporation?" *Physical Review Letters* **46**, 1351–1353 (1981).

6. Schützhold, R. & Unruh, W. G. "Gravity Wave Analogues of Black Holes." *Physical Review D* **66**, 044019 (2002).

7. Rousseaux, G., Mathis, C., Maïssa, P., Philbin, T. G. & Leonhardt, U. "Observation of Negative-Frequency Waves in a Water Tank: A Classical Analogue to the Hawking Effect?" *New Journal of Physics* **10**, 053015 (2008).

8. Weinfurtner, S., Tedford, E. W., Penrice, M. C. J., Unruh, W. G. & Lawrence, G. A. "Measurement of Stimulated Hawking Emission in an Analogue System." *Physical Review Letters* **106**, 021302 (2011).

9. Leonhardt, U. & Robertson, S. "Analytical Theory of Hawking Radiation in Dispersive Media." *New Journal of Physics* **14**, 053003 (2012).

10. Barceló, C., Liberati, S. & Visser, M. "Analogue Gravity." *Living Reviews in Relativity* **14**, 3 (2011).
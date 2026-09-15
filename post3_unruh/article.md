# Relativity Of Nothingness

## How one observer sees vacuum where another sees a hot bath

<!--
PURPOSE OF THE POST

Start with the most ordinary possible question: if Bob is floating in an
endless ocean, can he determine how fast he is moving?

Use water to establish the intuitive idea of a preferred rest frame.
Then remove that preferred frame and ask what a wave must look like if
all inertial observers are genuinely equivalent.

The key turn comes when Bob accelerates. Alice and Bob can then agree
on the field itself while disagreeing about its decomposition into
positive and negative frequencies.

Classically this is frequency mixing. After quantization, positive-
frequency modes are paired with annihilation operators and
negative-frequency modes with creation operators. Alice therefore calls
the state vacuum while Bob's particle-number operator assigns it a
thermal Planck distribution.

End by asking what that actually means physically. The mathematics is
well established; the statement that Bob is literally surrounded by
"real particles" is more subtle. Close with the enormous experimental
challenge and current attempts to test an operational signature of the
effect.

ARC:

How fast am I going?
    ↓
Water gives Bob an answer
    ↓
What if no experiment can reveal a preferred inertial frame?
    ↓
Lorentz-invariant dispersion
    ↓
Acceleration changes the question
    ↓
Same wave, different frequencies
    ↓
Positive ↔ annihilation; negative ↔ creation
    ↓
Alice: vacuum
Bob: thermal occupation
    ↓
How real are Bob's particles?
    ↓
Can we actually test this?
    ↓
How empty is empty space?
-->


![Feature_image.png](Feature_image.png)

> **Feature image — How fast am I going?** Bob is swimming in an apparently endless ocean, with no shore, boat, or landmark in sight. The question looks simple, but the water itself turns out to hold the answer — and that will be our first clue. Photo: Peter Berglund/iStock.

> *Alt text: A lone observer floating in a small boat on a featureless ocean stretching to the horizon, with no land or other visible reference point. The scene poses the question of whether the observer can determine his own motion.*

A person (let's call him Bob) is floating in a seemingly endless ocean, asking: how fast am I moving through the water? From experience we know that this question can be answered by observing the waves on the water surface.

Now consider Einstein's relativity, where we learn that absolute speed does not exist, and all observers moving at constant speed should have the same experience. What would a hypothetical medium look like, where Bob could not determine his speed at all, and where his friend Alice, moving at a different speed would have exactly the same experience? How would it be different from ordinary water? It turns out that the answer to this question prescribes a specific kind of medium, with a well-defined dispersion relation.

Then let Bob fire his engines: he starts accelerating. Acceleration breaks the symmetry, and Bob certainly feels that he accelerates while his friend Alice remains at rest. If they both look at the same wave, what is a constant frequency for Alice turns into a chirped frequency for Bob. So, where Alice hears a single tone, Bob hears a spectrum.

Now apply quantum physics. Frequency components are associated with particle creation or annihilation. And, as we will see, this means that what looks like empty vacuum to Alice can appear to Bob as a space populated with thermal particles.

> **How can two obsevers disagree about whether space is empty?**

## The Ocean Gives The Game Away

So how, exactly, does Bob use the water to answer his question? He can move the water surface at a fixed frequency, and measure the wavelength that comes out. In the frame where the water is at rest surface waves obey their own intrinsic dispersion relation:

Ω² = g k tanh(kh)

This relation ties frequency Ω and wavenumber k together in one specific way, and only in one specific frame. If Bob is moving relative to the water, the frequency he measures is Doppler-shifted:

ω_B = Ω(k) − vk

So, the same drive frequency no longer corresponds to the same wavelength. At rest relative to the water, his fixed frequency picks out one wavenumber. Moving relative to it, that same frequency picks out a different one. Measure the wavelength, and Bob has measured his own speed; not some absolute speed, but his speed relative to the water.

That last qualification matters more than it might look. Bob has not learned whether "the water is moving." He has only learned how fast he is moving with respect to it. What Bob has found, is a physically preferred frame: the one frame in which the medium is at rest, and its own dispersion relation takes the simple form above.

![Figure_1.png](Figure_1.png)

**Figure 1 — Bob's local wave experiment.** Bob drives surface waves at the same frequency according to his own clock and measures their wavelength. When he is at rest relative to the water, the drive frequency intersects the intrinsic water-wave dispersion relation at one wavenumber. Moving relative to the water Doppler-shifts the relation and the same measured frequency corresponds to a different wavenumber — and therefore a different wavelength. Image by author.

*Alt text: Dark-background dispersion plot of frequency versus wavenumber. A blue curve shows the surface-wave dispersion measured when Bob is at rest relative to the water, and a red shifted curve shows the relation when he moves relative to it. A horizontal line at one fixed measured frequency intersects the curves at two different wavenumbers, labelled k_rest and k_moving.*


## What If There Is No Water?

For a long time, physicists suspected light might work the same way. If light were just another wave travelling through some material-like medium, call it the ether, then in principle its dispersion relation should reveal that medium's rest frame too, exactly the way Bob's water waves revealed his.

Nobody was ever able to measure this ether. So, let us turn the question around entirely. Suppose no local experiment — none, ever — can reveal a preferred frame at all. What kind of dispersion relation should the medium have to survive that requirement?

Note that "no preferred frame" on its own does not single out relativity. Ordinary Galilean physics also has no preferred inertial frame — a ball thrown on a moving train looks just as ordinary to a passenger as to someone standing on the platform. So the requirement alone is not enough; what matters is how frequency and wavenumber are allowed to transform when we change observers. That is where Galilean and Lorentzian physics part ways, and it is worth looking at side by side.


## The Same Curve For Everyone

Let's start with a hyperbolic dispersion relation and ask what kind of 'ether' it would describe:

ω(k) = √(ω₀² + c²k²)

Under a Galilean change of observer, wavenumber stays fixed while frequency shifts by the relative velocity (the Doppler shift):

k′ = k
ω′ = ω − vk

Plug that in, and the relation changes shape entirely — a new observer moving at speed v no longer sees a wave obeying the same curve. The dispersion relation itself is observer-dependent, which is just another way of saying that a Galilean observer could, in principle, use it to find their own speed, the same way Bob used the water.

Now do the same thing with a Lorentz transformation instead:

ω′ = γ(ω − vk)
k′ = γ(k − vω/c²)

Here something different happens. Individual points — a given ω and k — do change coordinates; a wave that looked like frequency ω to one observer really does look like a different frequency ω′ to another. But plug the transformed ω′ and k′ back into the original relation, and they still satisfy it. The point has moved, but it has moved along the same hyperbola.

> **The dispersion relation itself, the shape of the curve, not the coordinates of any one point on it, stays exactly the same for every inertial observer.**

That is the property we were looking for. A wave obeying this dispersion relation gives no inertial observer a way to find a preferred frame, because there simply isn't one to find — every inertial observer describes the same physics with the same equation, just different coordinates on it. In the massless limit, ω₀ → 0, this reduces to the familiar ω = ±ck: light, unable to pick out a rest frame because there is nothing left in the equation for a frame to attach to.

So, just taking the hyperbola

ω² − c²k² = ω₀²

as a dispersion curve does not, on its own, give us an undetectable 'ether'. We need to add the mixing of space and time components that follow from a Lorentz transformation. The medium that does the trick is, ultimately, space-time itself.

![Figure_2.png](Figure_2.png)

**Figure 2 — What must an undetectable 'ether' look like?** Both panels start with the same dispersion relation. A Galilean change of observer changes the curve itself. Under a Lorentz transformation, individual frequency and wavenumber coordinates change, but the transformed points remain on the same hyperbola. The dispersion relation therefore has the same form for every inertial observer. Image by author.

*Alt text: Two dark-background dispersion diagrams labelled Galilean and Lorentz. In the Galilean panel a red transformed dispersion curve departs visibly from the original blue hyperbola. In the Lorentz panel red transformed points lie along the same blue hyperbola, illustrating that the individual coordinates change while the dispersion relation remains invariant.*


## So Far, Alice And Bob Still Agree

Now consider Alice. Alice and Bob can move at different constant velocities through space-time and still agree completely about waves. Not on the numbers: Alice and Bob will measure different frequencies and different wavelengths for the very same wave. But the relation between their personal frequency and wavelength is the same for both: they see the same dispersion relation.

There is something else they agree about. If a wave has a 'positive frequeny' (i.e., the phase develops clockwise in time) for Alice, then it is also a positive frequency wave for Bob. This sound obvious, and is a consequence of the fact that the phase speed of a wave is always faster than light. Yes, you read it right. The statement that 'nothing' can go faster than light holds for information or particles whose speed is measured by the group velocity (the derivative of the dispersion curve, see an earlier post on this). The phase velocity of an infinite plane wave is always faster than light. So the sign of the frequency, or the (anti-)clockwise development of phase over time is the same for Alice and Bob.

Now change one thing. Instead of coasting at a constant velocity, Bob fires his engine and accelerates.

That single change turns out to matter enormously. An observer moving at constant velocity has one inertial frame, for all time. An accelerating observer does not — Bob's instantaneous rest frame is a different inertial frame at every instant along his path, continuously boosting relative to the last. 

This is where the story turns.


## Now Let Bob Accelerate

Bob turns on his engine at such power that he feels a constant proper acceleration *a*. This is not a constant acceleration as seen from Alice's frame, but constant acceleration as Bob experiences it.

We won't work through the full derivation, but we did put it in the appendix for anyone who wants to see it step by step. The result is a trajectory that traces out a hyperbola in Alice's coordinates:

$$
t(\tau) = \frac{c}{a}\sinh\!\left(\frac{a\tau}{c}\right), \qquad x(\tau) = \frac{c^2}{a}\cosh\!\left(\frac{a\tau}{c}\right)
$$

Here τ is Bob's own proper time, the time on his own wristwatch. Bob's velocity, as seen by Alice, v/c = tanh(aτ/c), approaches the speed of light as τ grows, but never reaches it. He is forever accelerating, forever getting closer to c.

Now imagine a single, perfectly ordinary wave — a pure tone, one fixed frequency ω, of the kind Alice could send to any observer without a second thought. In Alice's coordinates, its phase depends only on t − x/c, the usual combination for a wave moving to the right. Substitute in Bob's hyperbolic trajectory, and t − x/c collapses into a single exponential in Bob's proper time,

$$
t - \frac{x}{c} = -\frac{c}{a}\, e^{-a\tau/c}
$$

So for Bob, in his own time, the wave is not a pure tone at all. The phase is an oscillation whose instantaneous frequency changes exponentially with Bob's proper time.

$$\phi(\tau) = \exp\!\left[i\,\frac{\omega c}{a}\, e^{-a\tau/c}\right]$$

> **Alice sent one frequency. Bob receives a chirp.**

![Figure_3.png](Figure_3.png)

**Figure 3 — One frequency becomes a chirp.** Left: the same wave, plotted as a helix against Alice's time (top) and Bob's proper time (bottom). For Alice the turns are evenly spaced — a single frequency. For Bob the turns compress at early times and stretch apart later, the signature of a continuously changing instantaneous frequency. Right: the corresponding Fourier spectra. Alice's is a single sharp peak at +Ω. Bob's spreads into a broad peak and develops a faint tail reaching into negative Ω — the first hint that Bob's own decomposition into positive and negative frequency will not agree with Alice's. Image by author.

*Alt text: Two pairs of plots. Top left, a 3D helix of constant pitch labelled Alice's time, representing a single-frequency wave. Bottom left, a helix labelled Bob's proper time, with turns compressed near one end and stretched apart near the other, showing a chirping frequency. Top right, a Fourier amplitude spectrum for Alice with a single sharp peak at positive frequency Ω and no content at negative Ω. Bottom right, a Fourier amplitude spectrum for Bob with a broadened peak at positive Ω and a small but nonzero tail extending into negative Ω.*

The spectrum of the chirped wave received by Bob can have a tail in the negative frequency domain. A wave that had a positive frequency for Alice picks up a negative-frequency component for Bob. This could never happen for two observers at constant velocity, however different their speeds. Acceleration, it turns out, can change the sign of the frequency.

## Bob's Vacuum Isn't Empty

So far we studied the classical, non-quantum view: Alice's pure tone reaches Bob as a chirp, and that chirp gives Bob's spectrum a tail into negative frequency. Quantum mechanics is what gives that tail consequences.

In the quantum theory, the split between positive and negative frequency is not just a labelling convention — it is *the* thing that tells us which operator is which. A positive-frequency mode pairs with an annihilation operator, â; a negative-frequency mode pairs with a creation operator, â†.

We learned earlier that for accelerated Bob, a mode that was purely positive-frequency for Alice becomes a mix of positive and negative frequency in Bob's decomposition. Because his annihilation operator b̂ is built from that mixed decomposition, b̂ is itself a mixture of Alice's â and â† — weighted by two numbers, the Bogoliubov coefficients α and β. Their ratio depends on nothing but the ratio of frequency to acceleration:

$$\frac{|\beta|^2}{|\alpha|^2} = e^{-2\pi c \Omega/a}$$

Note what this equation is *not* saying: it is not a statement about Alice's field changing in any way. The field is exactly what it always was. What has changed is what counts as "positive frequency" for Bob — and therefore what Bob's own number operator, N̂_B = b̂†b̂, assigns to Alice's vacuum. Alice's number operator gives zero on her own vacuum, as it must. Bob's does not:

$$\langle 0_A|\hat N_B|0_A\rangle = |\beta|^2$$

Where Alice's detector never clicks in her vacuum, Bob's has a probability |β|² of clicking. Same state, same field — different answers.

To pin down |β|² itself, we only need one more piece: the normalization that keeps the whole construction consistent, |α|² − |β|² = 1. Combined with the ratio above, it fixes |β|² exactly:

$$|\beta|^2 = \frac{1}{e^{2\pi c \Omega/a} - 1}$$

Readers who know their statistical mechanics will recognize that shape immediately — it is a Bose-Einstein distribution. Not an approximation to one, not something that merely resembles one: this is the exact occupation number of a thermal state, with a temperature set entirely by the acceleration,

$$k_B T_U = \frac{\hbar a}{2\pi c}$$

Alice's vacuum — genuinely empty, by her own reckoning — looks to Bob like a bath of thermal particles, populated according to Planck's own formula, at a temperature fixed by nothing but how hard Bob is accelerating. This is the Unruh effect.

![Figure_4.png](Figure_4.png)

**Figure 4 — From mixed frequencies to a thermal spectrum.** Top: the same classical spectrum from Figure 3, now split into its two pieces for Bob — the familiar positive-frequency part, |α|², and the negative-frequency tail, |β|², related to each other by a simple exponential in Ω/a. Bottom: quantizing the field turns positive frequency into an annihilation operator and negative frequency into a creation operator. Alice's vacuum contains no particles by her own count, but Bob's particle-number operator, built from his own mixture of creation and annihilation operators, assigns Alice's vacuum a nonzero, thermal occupation number. Image by author.

*Alt text: Two-part diagram. Top: two frequency-domain plots labelled Alice — inertial and Bob — accelerated, connected by an arrow reading "same wave." Alice's spectrum has only a positive-frequency peak, labelled none for negative frequency. Bob's spectrum has the same positive-frequency peak, now labelled |α|², plus a smaller negative-frequency component labelled |β|², with the ratio given as an exponential formula. Bottom: a quantization diagram showing positive frequency mapping to an annihilation operator â and negative frequency mapping to a creation operator â†, followed by boxed formulas for Alice's and Bob's number operators, showing that Bob's operator evaluated on Alice's vacuum equals |β|², given by a Bose-Einstein-like expression.*

Alice never sees anything. She stays inertial, her detector never clicks, and as far as she is concerned there is nothing there to see. Bob, doing nothing more exotic than firing an engine, finds himself bathed in radiation with a well-defined temperature. Same field, same state — and yet the two of them fundamentally disagree about how many particles are in the room.


## Nothing Starts To Look Warm

<!--
PURPOSE

Deliver the Unruh reveal.

Use the Bogoliubov normalization:

    |α|² - |β|² = 1

together with:

    |β|² / |α|² = exp(-2πcΩ/a)

to obtain:

    <N_B(Ω)> =
    |β|² =
    1 / [exp(2πcΩ/a) - 1]

Then compare with the ordinary Planck/Bose-Einstein occupation:

    <N(Ω)> =
    1 / [exp(ℏΩ/k_B T) - 1]

The expressions are identical if:

    k_B T_U = ℏa / (2πc)

This is the Unruh temperature.

This should feel like recognition rather than another derivation:
"We have seen that denominator before."

Emphasize:
Bob does not merely obtain some arbitrary non-zero particle count.
He obtains exactly the frequency dependence of a thermal distribution.

At this point pay off the title:

Alice calls the state empty.
Bob assigns that same state a temperature.
-->


## But Are Those Particles Real?

<!--
PURPOSE

Introduce the interpretational controversy without undermining the
mathematics.

Be precise:

The standard Rindler/Minkowski calculation and the thermal response of
an ideal uniformly accelerated detector are not the main controversial
parts.

The subtler question is what we mean when we say:
"Bob sees a bath of particles."

Globally, the Minkowski vacuum remains the Minkowski vacuum.
Nothing has happened in Alice's description that fills spacetime with
an observer-independent cloud of particles.

Bob uses a different notion of positive frequency and therefore a
different particle-number operator.

An accelerated detector can become excited, but the energy accounting
also involves the external agency maintaining its acceleration.

Mention the Rindler horizon briefly:
Bob has access only to one Rindler wedge. Restricting the Minkowski
vacuum to that accessible region gives a thermal state.

This is a good place for one sentence acknowledging that physicists,
including Sabine Hossenfelder in popular discussions, object especially
to the loose statement that acceleration "creates real particles from
nothing."

Do not frame this as "some physicists reject the Unruh calculation."
The disagreement is primarily about physical interpretation and what
would constitute an unambiguous experimental observation.
-->


> **Alice calls it vacuum. Bob's particle detector calls it thermal.  
> What, then, do we mean when we say that a particle is 'really there'?**


## Can We Test It?

<!--
PURPOSE

One compact paragraph. Do not create another figure.

Start with the scale problem:

    T_U = ℏa / (2πck_B)

Earth gravity gives an unimaginably small temperature.
A temperature of order 1 K requires acceleration of order 10^20 m/s².

Then current experimental direction:

Gregori et al. (2024) propose using ultra-high-intensity lasers to
accelerate electrons and an X-ray probe to search for a measurable
laboratory signature associated with Unruh thermality.

Be careful:
Their paper explicitly notes both the technical difficulty and the
conceptual question of what a laboratory observer should actually
measure. It proposes a test; it is not a reported detection.

Can mention analogue/simulator experiments separately:
these can reproduce aspects of the mode mixing, correlations or detector
response, but should not be presented as direct detection of an observer
physically accelerating through the relativistic vacuum.

This makes the experimental paragraph part of the interpretation story:
the hard question is not merely producing a huge acceleration, but
identifying an observable that unambiguously distinguishes the Unruh
effect from ordinary radiation and acceleration effects.
-->


## Back To The Water

<!--
PURPOSE

Close the circle rather than introducing new physics.

We started with water because it made Bob's motion detectable.

Now return to water for a different reason.

Leonhardt et al. showed that classical noisy water waves, sampled along
an accelerated/Rindler trajectory, reproduce characteristic Unruh-like
correlations, including squeezing and indications of the Planck
spectrum.

Be explicit:
This is a CLASSICAL ANALOGUE / stimulated analogue.
It does not prove that the quantum Minkowski vacuum literally contains
particles.

Its value is conceptual:
the positive/negative-frequency mixing and the exponential structure
already belong to wave kinematics. Quantization changes what that mixing
means.

This echoes the previous Hawking post:
classical analogue systems can expose the mode-conversion mechanism
without themselves producing the full spontaneous quantum phenomenon.
Leonhardt et al. explicitly describe their experiment as a classical
analogue and connect the observed wave-noise correlations to the Planck
spectrum. 
-->


## How Empty Is Empty Space?

<!--
PURPOSE

Short open ending: 2–3 paragraphs maximum.

Return to feature image / Bob.

At the start Bob asked:
"How fast am I going?"

Water gave him an answer because the medium supplied a preferred frame.

Remove that preferred frame and constant velocity becomes relative.

But acceleration changes the story again. Alice and Bob can agree on
the quantum field and nevertheless disagree about which parts count as
positive and negative frequency — and therefore about what counts as a
particle.

Do NOT end by claiming that acceleration objectively manufactures
particles.

End on the deeper question:

Vacuum is not simply "nothing."
It is a quantum state, and what an observer calls particles depends on
how that observer moves through it.

Possible final lines:

"So, perhaps the strangest part of the Unruh effect is not that
acceleration creates something from nothing. It is that quantum field
theory forces us to ask what we meant by 'nothing' in the first place."

or, more open:

"We started by asking Bob how fast he was moving. We end with a stranger
question: how empty is empty space?"
-->


---

## Appendix — Where Does The Exponential Come From?

<!--
OPTIONAL

Only include if the main text feels as if the exponential appeared by
magic.

Keep this short and possibly turn it into one derivation image.

For constant proper acceleration a:

    dv/dτ = a(1 - v²/c²)

which gives:

    v(τ) = c tanh(aτ/c)

and:

    t(τ) = (c/a) sinh(aτ/c)

    x(τ) = (c²/a) cosh(aτ/c)

For a right-moving wave the phase depends on:

    t - x/c

so:

    t - x/c
      = (c/a)[sinh(aτ/c) - cosh(aτ/c)]
      = -(c/a) exp(-aτ/c)

Therefore a simple monochromatic wave for Alice becomes exponentially
chirped when sampled using Bob's proper time.

Do not go through rapidity unless needed.
-->


## References

1. W. G. Unruh, "Notes on Black-Hole Evaporation." *Physical Review D*
   **14**, 870–892 (1976).

2. S. A. Fulling, "Nonuniqueness of Canonical Field Quantization in
   Riemannian Space-Time." *Physical Review D* **7**, 2850–2862 (1973).

3. P. C. W. Davies, "Scalar Production in Schwarzschild and Rindler
   Metrics." *Journal of Physics A: Mathematical and General* **8**,
   609–616 (1975).

4. L. C. B. Crispino, A. Higuchi & G. E. A. Matsas,
   "The Unruh Effect and Its Applications." *Reviews of Modern Physics*
   **80**, 787–838 (2008).

5. U. Leonhardt, I. Griniasty, S. Wildeman, E. Fort & M. Fink,
   "Classical Analogue of the Unruh Effect." *Physical Review A*
   **97**, 022118 (2018).

6. G. Gregori, G. Marocco, S. Sarkar, R. Bingham & C. Wang,
   "Measuring Unruh Radiation from Accelerated Electrons."
   *European Physical Journal C* **84**, 475 (2024).

7. W. G. Unruh & R. M. Wald, "What Happens When an Accelerating
   Observer Detects a Rindler Particle." *Physical Review D* **29**,
   1047–1056 (1984).

8. W. G. Unruh & R. M. Wald, "Information Loss."
   *Reports on Progress in Physics* **80**, 092002 (2017).

![appendix](Appendix_exponential.png)
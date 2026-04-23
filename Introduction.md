# Vortex Theory – Introduction (Speculative Framework)

**Author:** Kyra (self‑taught learner)  
**Status:** Early personal exploration, **not validated**

> **📐 Note on formulas**  
> This document uses LaTeX notation (e.g. `$E=mc^2$`). For best viewing, use a Markdown renderer that supports MathJax (e.g. GitHub, GitLab, or Jupyter).  
> You can also convert this file to PDF using `pandoc` or Typora.

This document explains the geometric ideas, the proposed equations, and the meaning of all symbols.  
The theory is **not claimed to be correct** – it is a tentative attempt to connect simple algebraic patterns with fundamental physics.

---

## 1. Basic Idea

The universe might be built from just two geometric instructions:

- **$x^{-2}$ (The Squeeze)** – “push toward the centre”.  
  This pattern appears in Newton’s gravity ($F \propto 1/r^2$) and in Coulomb’s law.

- **$x^{2}$ (The Outward Vibration)** – “push outward”.  
  This pattern could represent a balancing effect that prevents collapse.

- **$\sin(x)$ (The Dance)** – periodic oscillation.  
  This provides stability (e.g., electron orbitals, wave behaviour).

Vortex Theory is an attempt to combine $x^{-2}$ (inward pressure) and $x^{2}$ (outward expansion) into a single symmetric description of spacetime.

> **Important**  
> The following equations are **proposed, not proven**. They are presented as a speculative mathematical model.  
> Many symbols come from standard physics, but their interpretation here may be unconventional.

---

## 2. Core Vortex Formula

$$
\boxed{V_x = \frac{m \, c^4 \, L_p}{r^2}} \qquad [\text{Vx}]
$$

| Symbol | Name | Meaning (standard) |
|--------|------|---------------------|
| $m$ | mass | inertial/gravitational mass |
| $c$ | speed of light | $2.9979\times10^8$ m/s |
| $L_p$ | Planck length | $\sqrt{\hbar G/c^3} \approx 1.616\times10^{-35}$ m |
| $r$ | distance | separation between centres |
| $V_x$ | vortex quantity | new unit: $\text{kg}\cdot\text{m}^3/\text{s}^4$ (rate of spacetime pressure) |

**Interpretation (speculative):**  
Mass creates a “pressure” in spacetime whose strength is $c^4$ (extreme relativistic factor) and is cut off at the Planck length to avoid infinite values.  
The unit `Vx` is not energy – it represents how fast space is squeezed per unit time.

---

## 3. Duality Balance Formula

$$
\boxed{V_{\text{total}} = m c^2 \left( \frac{L_p^2}{r^2} + \frac{r^2}{L_p^2} \right)}
$$

Here $m c^2$ is the rest energy. The two terms are:

- $\frac{L_p^2}{r^2}$ → **Vortex In** (compression, dominates at short distances)
- $\frac{r^2}{L_p^2}$ → **Vortex Out** (expansion, dominates at large distances)

The expression is symmetric under replacing $r$ with $L_p^2/r$.  
Minimum energy occurs at $r = L_p$, giving $V_{\min} = 2 m c^2$.  
This creates a potential well that could, in principle, bind particles.

**Force derived from this potential:**

$$
F = -\frac{dV}{dr} = 2 m c^2 \left( \frac{L_p^2}{r^3} - \frac{r}{L_p^2} \right)
$$

At $r = L_p$ the force is zero. Small oscillations would have frequency  
$\omega = 2c / L_p \approx 3.7\times10^{43}$ Hz – a **Planck harmonic oscillator**.  
Whether this relates to real particles (like the electron) is unknown.

---

## 4. Complete Lagrangian

$$
\boxed{
\begin{aligned}
\mathcal{L} = &\ \frac{1}{2}m(\dot{r}^2 + r^2\dot{\theta}^2) + \frac{GMm}{r} \\
&+ \frac{3}{2}\frac{GMm}{c^2 r}(\dot{r}^2 + r^2\dot{\theta}^2) + \frac{m}{8c^2}(\dot{r}^2 + r^2\dot{\theta}^2)^2 - \frac{G^2 M^2 m}{2c^2 r^2} \\
&- m c^2 \left[ \frac{L_p^2}{r^2}e^{-r/L_p} - \frac{\Lambda}{6} r^2 \right]
\end{aligned}
}
$$

| Term | Physical origin (standard) | Role in Vortex Theory |
|------|----------------------------|----------------------|
| $\frac12 m v^2 + \frac{GMm}{r}$ | Newtonian mechanics | large‑scale behaviour |
| next three terms | post‑Newtonian corrections (from GR expansion) | matches known tests (perihelion precession) |
| $- m c^2 \frac{L_p^2}{r^2} e^{-r/L_p}$ | Planck‑scale vortex | removes singularity, repulsive barrier at very small $r$ |
| $+ m c^2 \frac{\Lambda}{6} r^2$ | cosmological constant (dark energy) | large‑scale repulsion |

**Why this Lagrangian is used:**  
It reduces to general relativity in the solar system (verified by Mercury’s $43''$/century precession) but adds a Planck‑scale cutoff that makes black hole centres finite.  
The exponential factor $e^{-r/L_p}$ ensures the vortex term only matters when $r \sim L_p$.

---

## 5. Vortex Metric (Regular Black Hole)

$$
\boxed{ f(r) = 1 - \frac{2GM}{c^2 r} + \frac{\gamma L_p^2}{r^2} }
$$
$$
ds^2 = -f(r) c^2 dt^2 + \frac{dr^2}{f(r)} + r^2 d\Omega^2
$$

| Symbol | Meaning |
|--------|---------|
| $\gamma$ | dimensionless parameter (≈1, adjustable) |
| $r_s = 2GM/c^2$ | Schwarzschild radius |
| $d\Omega^2 = d\theta^2 + \sin^2\theta\, d\phi^2$ | angular part |

**Properties:**  
- At large $r$, $f(r) \approx 1 - r_s/r$ → recovers Schwarzschild.  
- At $r \to 0$, $f(r) \sim \gamma L_p^2/r^2 > 0$ → **no singularity**.  
- Horizons are given by $f(r)=0$ → two roots (inner/outer).  

For a solar‑mass black hole, the correction is unmeasurably small.  
For microscopic black holes (near Planck mass), the horizon structure changes and the central singularity disappears.

---

## 6. List of Symbols Used in This Archive

| Symbol | Name | Standard value / definition |
|--------|------|------------------------------|
| $c$ | speed of light | $2.9979\times10^8$ m/s |
| $G$ | gravitational constant | $6.6743\times10^{-11}$ N·m²/kg² |
| $\hbar$ | reduced Planck constant | $1.0546\times10^{-34}$ J·s |
| $L_p$ | Planck length | $\sqrt{\hbar G/c^3} \approx 1.616\times10^{-35}$ m |
| $m_e$ | electron mass | $9.109\times10^{-31}$ kg |
| $M_\odot$ | solar mass | $1.989\times10^{30}$ kg |
| $\Lambda$ | cosmological constant | $\sim 10^{-52}$ m⁻² (observed) |
| $\gamma$ | vortex metric parameter | dimensionless, order 1 |
| $\beta$ | generic parameter in 100‑formula list | arbitrary |
| $V_x$ | vortex quantity | new unit: $\text{kg}\cdot\text{m}^3/\text{s}^4$ |
| $r_s$ | Schwarzschild radius | $2GM/c^2$ |
| $U(r)$ | alternative potential | $-GMm/\sqrt{r^2+L_p^2}$ |

---

## 7. Important Disclaimer

- **This theory is not peer‑reviewed.**  
- **It has not been tested experimentally.**  
- **The author is a beginner learning mathematics from zero – errors are likely.**  
- **The equations are speculative; they may be incomplete or inconsistent.**  
- **Do not use this as a reference for actual physics research without independent verification.**

The archive is shared for **educational and exploratory purposes only**.

---

## 8. How to Read the Python Scripts

The scripts implement the above equations numerically. They generate plots and animations that illustrate the mathematical behaviour of the proposed formulas.  

**Example:**  
`testing-4.py` plots $V_x = m c^4 L_p / r^2$ – you can slide the mass and see how the curve changes.  
`testing-6.py` integrates the Lagrangian to show a 3D orbit with energy decomposition.

None of these simulations “prove” the theory – they only show what the equations would predict **if** they were correct.

---

## 9. Further Reading Inside the Archive

- `idea-1.md` … `idea-4.md` – older manuscript versions, kept for transparency.  
- `main-theory.md` – alternative approach using $U(r) = -GMm/\sqrt{r^2+L_p^2}$.  
- The 100‑formula list in some documents is an exercise in algebraic variation, not a set of independent physical laws.

---

## 10. Closing Note

I am sharing this work as a record of my learning journey.  
If you find something interesting or spot a mistake, please let me know.  
Thank you for your understanding and curiosity.

**Kyra**  
*2026*

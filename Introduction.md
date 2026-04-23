# Vortex Theory – Introduction (Speculative Framework)

**Author:** Kyra (self‑taught learner)  
**Status:** Early personal exploration, **not validated**

This document explains the geometric ideas, the proposed equations, and the meaning of all symbols.  
The theory is **not claimed to be correct** – it is a tentative attempt to connect simple algebraic patterns with fundamental physics.

---

## 1. Basic Idea

The universe might be built from just two geometric instructions:

- **`x⁻²` (The Squeeze)** – “push toward the centre”.  
  This pattern appears in Newton’s gravity (`F ∝ 1/r²`) and in Coulomb’s law.

- **`x²` (The Outward Vibration)** – “push outward”.  
  This pattern could represent a balancing effect that prevents collapse.

- **`sin(x)` (The Dance)** – periodic oscillation.  
  This provides stability (e.g., electron orbitals, wave behaviour).

Vortex Theory is an attempt to combine `x⁻²` (inward pressure) and `x²` (outward expansion) into a single symmetric description of spacetime.

> **Important**  
> The following equations are **proposed, not proven**. They are presented as a speculative mathematical model.  
> Many symbols come from standard physics, but their interpretation here may be unconventional.

---

## 2. Core Vortex Formula

\[
\boxed{V_x = \frac{m \, c^4 \, L_p}{r^2}} \qquad [\text{Vx}]
\]

| Symbol | Name | Meaning (standard) |
|--------|------|---------------------|
| `m` | mass | inertial/gravitational mass |
| `c` | speed of light | 299,792,458 m/s |
| `L_p` | Planck length | `√(ħG/c³)` ≈ 1.6×10⁻³⁵ m |
| `r` | distance | separation between centres |
| `V_x` | vortex quantity | new unit: M·L³·T⁻⁴ (rate of spacetime pressure) |

**Interpretation (speculative):**  
Mass creates a “pressure” in spacetime whose strength is `c⁴` (extreme relativistic factor) and is cut off at the Planck length to avoid infinite values.  
The unit `Vx` is not energy – it represents how fast space is squeezed per unit time.

---

## 3. Duality Balance Formula

\[
\boxed{V_{\text{total}} = m c^2 \left( \frac{L_p^2}{r^2} + \frac{r^2}{L_p^2} \right)}
\]

Here `m c²` is the rest energy. The two terms are:

- `Lp²/r²` → **Vortex In** (compression, dominates at short distances)
- `r²/Lp²` → **Vortex Out** (expansion, dominates at large distances)

The expression is symmetric under replacing `r` with `Lp²/r`.  
Minimum energy occurs at `r = Lp`, giving `V_min = 2 m c²`.  
This creates a potential well that could, in principle, bind particles.

**Force derived from this potential:**

\[
F = -\frac{dV}{dr} = 2 m c^2 \left( \frac{L_p^2}{r^3} - \frac{r}{L_p^2} \right)
\]

At `r = Lp` the force is zero. Small oscillations would have frequency  
`ω = 2c / Lp` ≈ 3.7×10⁴³ Hz – a **Planck harmonic oscillator**.  
Whether this relates to real particles (like the electron) is unknown.

---

## 4. Complete Lagrangian

\[
\boxed{
\begin{aligned}
\mathcal{L} = &\ \frac{1}{2}m(\dot{r}^2 + r^2\dot{\theta}^2) + \frac{GMm}{r} \\
&+ \frac{3}{2}\frac{GMm}{c^2 r}(\dot{r}^2 + r^2\dot{\theta}^2) + \frac{m}{8c^2}(\dot{r}^2 + r^2\dot{\theta}^2)^2 - \frac{G^2 M^2 m}{2c^2 r^2} \\
&- m c^2 \left[ \frac{L_p^2}{r^2}e^{-r/L_p} - \frac{\Lambda}{6} r^2 \right]
\end{aligned}
}
\]

| Term | Physical origin (standard) | Role in Vortex Theory |
|------|----------------------------|----------------------|
| `½m v²` + `GMm/r` | Newtonian mechanics | large‑scale behaviour |
| next three terms | post‑Newtonian corrections (from GR expansion) | matches known tests (perihelion precession) |
| `-m c² (Lp²/r²) e^{-r/Lp}` | Planck‑scale vortex | removes singularity, repulsive barrier at very small `r` |
| `+m c² (Λ/6) r²` | cosmological constant (dark energy) | large‑scale repulsion |

**Why this Lagrangian is used:**  
It reduces to general relativity in the solar system (verified by Mercury’s 43″/century precession) but adds a Planck‑scale cutoff that makes black hole centres finite.  
The exponential factor `e^{-r/Lp}` ensures the vortex term only matters when `r ~ Lp`.

---

## 5. Vortex Metric (Regular Black Hole)

\[
\boxed{ f(r) = 1 - \frac{2GM}{c^2 r} + \frac{\gamma L_p^2}{r^2} }
\]
\[
ds^2 = -f(r) c^2 dt^2 + \frac{dr^2}{f(r)} + r^2 d\Omega^2
\]

| Symbol | Meaning |
|--------|---------|
| `γ` | dimensionless parameter (≈1, adjustable) |
| `r_s = 2GM/c²` | Schwarzschild radius |

**Properties:**  
- At large `r`, `f(r) ≈ 1 - r_s/r` → recovers Schwarzschild.  
- At `r → 0`, `f(r) ∼ γ Lp²/r² > 0` → **no singularity**.  
- Horizons are given by `f(r)=0` → two roots (inner/outer).  

For a solar‑mass black hole, the correction is unmeasurably small.  
For microscopic black holes (near Planck mass), the horizon structure changes and the central singularity disappears.

---

## 6. List of Symbols Used in This Archive

| Symbol | Name | Standard value / definition |
|--------|------|------------------------------|
| `c` | speed of light | 2.9979×10⁸ m/s |
| `G` | gravitational constant | 6.6743×10⁻¹¹ N·m²/kg² |
| `ħ` | reduced Planck constant | 1.0546×10⁻³⁴ J·s |
| `Lp` | Planck length | `√(ħG/c³)` ≈ 1.616×10⁻³⁵ m |
| `m_e` | electron mass | 9.109×10⁻³¹ kg |
| `M_☉` | solar mass | 1.989×10³⁰ kg |
| `Λ` | cosmological constant | ~10⁻⁵² m⁻² (observed) |
| `γ` | vortex metric parameter | dimensionless, order 1 |
| `β` | generic parameter in 100‑formula list | arbitrary |
| `V_x` | vortex quantity | new unit: kg·m³/s⁴ |
| `r_s` | Schwarzschild radius | `2GM/c²` |
| `U(r)` | alternative potential | `-GMm/√(r²+Lp²)` |

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
`testing-4.py` plots `V_x = m c⁴ Lp / r²` – you can slide the mass and see how the curve changes.  
`testing-6.py` integrates the Lagrangian to show a 3D orbit with energy decomposition.

None of these simulations “prove” the theory – they only show what the equations would predict **if** they were correct.

---

## 9. Further Reading Inside the Archive

- `idea-1.md` … `idea-4.md` – older manuscript versions, kept for transparency.  
- `main-theory.md` – alternative approach using `U(r) = -GMm/√(r²+Lp²)`.  
- The 100‑formula list in some documents is an exercise in algebraic variation, not a set of independent physical laws.

---

## 10. Closing Note

I am sharing this work as a record of my learning journey.  
If you find something interesting or spot a mistake, please let me know.  
Thank you for your understanding and curiosity.

**Kyra**  
*2026*

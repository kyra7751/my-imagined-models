# Universal Gravity Theory: A Mathematical Transparency Report  
*Before → After · Correctness vs. Contentious Points · Scale‑Dependent Formulations*

---

## 1. Core Transformation – The Regularization of Singularity

The entire theory pivots on a single substitution:  

| Classical expression | Regularized expression |
|----------------------|------------------------|
| $\displaystyle \frac{1}{r}$ (in potential) | $\displaystyle \frac{1}{\sqrt{r^{2}+L_{p}^{2}}}$ |
| $\displaystyle \frac{1}{r^{2}}$ (in force) | $\displaystyle \frac{r}{(r^{2}+L_{p}^{2})^{3/2}}$ |

where $L_p = \sqrt{\hbar G / c^{3}} \approx 1.616\times10^{-35}\,\text{m}$ is the Planck length.  
The modification prevents the denominator from ever reaching zero – thus **all physical quantities remain finite at $r=0$**.

### 1.1 Gravitational Potential – Before and After

**Newtonian (classical):**  
$U_{\text{Newton}}(r) = -\frac{GMm}{r}$
- Diverges to $-\infty$ as $r\to 0$ → singularity.

**Regularized**  
$\boxed{U(r) = -\frac{GMm}{\sqrt{r^{2}+L_{p}^{2}}}}$
- At $r=0$, $U(0) = -\frac{GMm}{L_{p}}$ (finite).

**What changed:** A tiny constant $L_p^{2}$ is added under the square root. For macroscopic distances $r\gg L_p$, the two potentials are indistinguishable. At the Planck scale the behaviour is completely different – no divergence.

---

### 1.2 Force Law – Before and After

**Newtonian force:**  
$F_{\text{Newton}}(r) = -\frac{dU_{\text{Newton}}}{dr} = -\frac{GMm}{r^{2}}$

**Regularized force:**  
$\boxed{F(r) = -\frac{GMm\,r}{(r^{2}+L_{p}^{2})^{3/2}}}$

- **At $r=0$:** $F(0)=0$ (force vanishes, no infinite tug).  
- **For $r \ll L_{p}$:** $F(r) \approx -\frac{GMm}{L_{p}^{3}}\,r$ — a linear, spring‑like restoring force (like $F=-kx$).  
- **For $r \gg L_{p}$:** $F(r) \approx -\frac{GMm}{r^{2}} +\frac{3GMm L_{p}^{2}}{2r^{4}}$, where the leading term is exactly Newton.

---

## 2. Mathematical Expansions – Which Formula Works at Which Scale?

The core regularized potential splits naturally into scale‑dependent approximations.

### 2.1 Large Distance Limit ($r \gg L_{p}$) – Macroscopic/Newtonian Regime

$$
\begin{aligned}
\sqrt{r^{2}+L_{p}^{2}} &= r\sqrt{1+\frac{L_{p}^{2}}{r^{2}}}
= r\left(1+\frac{L_{p}^{2}}{2r^{2}} - \frac{L_{p}^{4}}{8r^{4}} + \mathcal{O}\!\left(\frac{L_{p}^{6}}{r^{6}}\right)\right) \[4pt]
\Rightarrow\; U(r) &= -\frac{GMm}{r}\left(1 - \frac{L_{p}^{2}}{2r^{2}} + \cdots\right) \\
&\approx \underbrace{-\frac{GMm}{r}}_{\text{Newton}} + \underbrace{\frac{GMm L_{p}^{2}}{2r^{3}}}_{\text{1st quantum correction}} .
\end{aligned}
$$

- **Newton’s law** is recovered from the first term.  
- The correction $\propto 1/r^{3}$ is utterly negligible for planetary or laboratory scales because $L_p^{2} \sim 10^{-70}\,\text{m}^{2}$.

**Force in this regime:** $F(r) \approx -\frac{GMm}{r^{2}}$ (Newton again).

---

### 2.2 Planck‑Scale Limit ($r \sim L_{p}$ or $r \ll L_{p}$) – Quantum Core

When $r$ is comparable to $L_{p}$, the expansion above breaks down; the full expression must be used.

$$
U(r) \approx -\frac{GMm}{L_{p}} \left[1 - \frac{1}{2}\left(\frac{r}{L_{p}}\right)^{2} + \cdots\right] \quad(\text{for } r \ll L_{p})
$$

- At $r=0$, $U(0) = -GMm/L_{p}$ is the **minimum potential depth** (no infinite well).  
- The force becomes $F(r) \approx -\frac{GMm}{L_{p}^{3}}\,r$, i.e. a harmonic oscillator.

This behaviour explicitly **removes the central singularity** that plagues classical black holes and the Big Bang.

---

## 3. Comparative Table – Classical vs. Regularized

| Physical quantity | Classical GR / Newton | Regularized Theory | Notes |
|-------------------|-----------------------|----------------------------|-------|
| Potential energy | $-\frac{GMm}{r}$ | $-\frac{GMm}{\sqrt{r^{2}+L_{p}^{2}}}$ | Finite at $r=0$. |
| Gravitational force | $-\frac{GMm}{r^{2}}$ | $-\frac{GMm\,r}{(r^{2}+L_{p}^{2})^{3/2}}$ | Zero at $r=0$. |
| Time‑time metric component $A(r)$ | $1 - \frac{2GM}{c^{2}r}$ (Schwarzschild) | $1 - \frac{2GM}{c^{2}\sqrt{r^{2}+L_{p}^{2}}}$ | No coordinate singularity at $r=0$; curvature invariants stay finite. |
| Singularity at $r=0$ | Yes, infinite curvature | **No**, curvature bounded | Kretschmann scalar $\sim \frac{48 G^{2} M^{2}}{c^{4} L_{p}^{6}}$ at $r=0$. |
| Horizon formation | $r_{s}=2GM/c^{2}$ | Still exists for $M > \frac{c^{2}L_{p}}{2G}$ | But interior is regular; centre is not a point of infinite density. |

---

## 4. Breakdown of the Full Lagrangian – Which Parts Come from Where

The complete Lagrangian $\mathcal{L}$ (used for orbits and simulations) is:

$$\mathcal{L} = \underbrace{\frac{1}{2} m v^{2}}_{\text{Newtonian kinetic}} + \underbrace{\frac{GMm}{\sqrt{r^{2}+L_{p}^{2}}}}_{\text{Regularized potential }(-U)}$$

$$\quad + \underbrace{\frac{3GMm}{2c^{2}r} v^{2} + \frac{m}{8c^{2}} v^{4} - \frac{G^{2}M^{2}m}{2c^{2}r^{2}}}_{\text{Post‑Newtonian terms (from GR expansion of Schwarzschild)}}$$

$$\quad + \underbrace{\frac{1}{6} m c^{2} \Lambda r^{2}}_{\text{Cosmological constant (repulsive)}}+ \underbrace{\frac{m c^{2} L_{p}^{2}}{r^{2}+L_{p}^{2}} e^{-r/L_{p}}}_{\text{Exponential quantum correction}}$$

### 4.1 Origin of the Terms

- **Newtonian kinetic term + regularized potential** → foundation of the theory; the potential is the core new idea.  
- **Post‑Newtonian terms** (order $v^{2}/c^{2}$ and $v^{4}/c^{4}$) → de­rived from the weak‑field expansion of the Schwarzschild metric in general relativity. They are *not* new; they guarantee that the theory reproduces the perihelion precession of Mercury and binary pulsar observations.  
- **Cosmological constant term** → sourced from Einstein’s field equations with $\Lambda$; included to model dark energy on cosmic scales.  
- **Exponential quantum correction** → a phenomenological (ansatz) term added to smooth the potential further and mimic possible non‑local quantum gravity effects; it is significant only at $r\sim L_{p}$ and decays rapidly.

**Which parts are “turunan dari rumus sebelumnya”?**  
The post‑Newtonian expansion is a direct derivation from general relativity’s Schwarzschild solution. The cosmological constant term follows from the linearised Einstein equations. The exponential correction, however, is **not** derived from a fundamental theory; it is a motivated guess that must later be justified.

---

## 5. What Becomes Correct? – The Wins

1. **Eliminates singularities** – Curvature scalars remain finite at $r=0$. Black holes and initial cosmological states become mathematically well‑behaved.
2. **Recovers all classical tests** – For $r\gg L_{p}$, the theory reduces exactly to Newtonian gravity and, with the post‑Newtonian terms, to all standard GR predictions (light deflection, Shapiro delay, perihelion precession, gravitational waves).
3. **Numerical consistency** – Simulations with $G=c=1$, $M=1$ show a perihelion precession of $2.95\times10^{-4}$ rad/orbit for $r_{0}=10$, matching GR; the quantum correction ($L_{p}=0.01$, enlarged) shifts it by only 0.3%, demonstrating that the theory can accommodate tiny deviations.
4. **Planck‑scale behaviour** – The harmonic force $F\propto -r$ prevents collapse to a point, suggesting a quantum bounce instead of a singularity.

---

## 6. What Becomes “Wrong” or Contentious? – The Transparent Critique

For a balanced evaluation, the following criticisms must be acknowledged:

### 6.1 The “Stress‑Energy” Problem
The regularized metric $A(r)=1-\frac{2GM}{c^{2}\sqrt{r^{2}+L_{p}^{2}}}$ does **not** satisfy the ordinary Einstein field equations with a physically realistic $T_{\mu\nu}$. If one plugs this metric into $G_{\mu\nu}=8\pi G\,T_{\mu\nu}/c^{4}$, the required stress‑energy tensor will involve **exotic matter** (e.g., negative energy densities or anisotropic pressures) near $r=0$.  
In the standard model, one first postulates a valid matter action, solves the field equations, and then obtains the metric. Here the process is reversed: the metric is guessed from the regularized potential. This can be seen as “putting the cart before the horse” unless a consistent matter field is identified that sources this metric.

### 6.2 Violation of the No‑Hair Theorem?
Black holes in classical GR are characterised only by mass, charge, and angular momentum. The addition of the exponential quantum correction $Q(r)$ and the regularized core introduces extra structure (“hair”) – the metric depends on parameters like $L_{p}$ and details of the regularisation. Even if the deviation is tiny, it technically violates the strict no‑hair theorem, which might be viewed as a drawback unless the theorem is itself modified in quantum gravity.

### 6.3 Ad‑hoc Quantum Correction
The exponential term $\frac{m c^{2} L_{p}^{2}}{r^{2}+L_{p}^{2}} e^{-r/L_{p}}$ is added by hand. It is not derived from a fundamental quantum gravity principle (e.g., a specific non‑local action). Therefore, it is a *phenomenological* term – useful for exploration, but not yet rooted in a deeper theory. Critics may consider this as mere curve‑fitting.

### 6.4 Scale of $L_{p}$ and Unobservability
Because $L_{p}\sim 10^{-35}\,\text{m}$, all quantum corrections are immeasurably small for distances above the atomic scale. The theory, in its current form, makes no testable predictions for laboratory experiments that differ from GR. This is not a logical flaw but a practical one: the regularization could be considered unfalsifiable with present technology.

---

## 7. Scale‑Dependent Summary – Which Formula to Use When

| Distance regime | Dominant form of potential | Dominant force law | Matching classical theory |
|----------------|----------------------------|---------------------|---------------------------|
| $r \gg L_{p}$ (laboratory, planetary, galactic) | $U \approx -\frac{GMm}{r}$ (Newton) | $F \approx -\frac{GMm}{r^{2}}$ | Newton & GR (with pN terms) |
| $r \sim \text{few } L_{p}$ (Planck core) | $U = -\frac{GMm}{\sqrt{r^{2}+L_{p}^{2}}}$ (exact) | $F = -\frac{GMm\,r}{(r^{2}+L_{p}^{2})^{3/2}}$ | None – New quantum gravity regime |
| $r \ll L_{p}$ (extreme quantum) | $U \approx -\frac{GMm}{L_{p}}$ (constant) | $F \approx -\frac{GMm}{L_{p}^{3}}\,r$ (harmonic) | Avoids singularity; resembles oscillator |

The full Lagrangian (Section 4) is the **single unified formula** for all scales, but its individual terms dominate in different regimes.

---

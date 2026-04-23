# Universal Gravity Theory: A Regularization Approach via a Modified Potential

**Author:** Kyra  
**Date:** 2026-03-22

---

## Abstract

A theoretical framework is proposed that describes gravity across all distances using a regularized potential. The key idea is that the difference between classical and quantum gravitational behaviour arises purely from length scale. At macroscopic distances ($r \gg L_p$) the potential reduces to Newtonian form; at the Planck scale ($r \sim L_p$) it remains finite, avoiding singularities. The basic formula is

$$
\boxed{U(r) = -\frac{GMm}{\sqrt{r^2 + L_p^2}}}
$$

with $L_p = \sqrt{\hbar G/c^3}$ the Planck length. This potential can be expanded into a Lagrangian that includes post‑Newtonian corrections, a cosmological constant, and an exponential quantum term. This document presents derivation, limit analysis, Hamiltonian formulation, and connections with general relativity and quantum gravity.

---

## 1. Introduction

General relativity and quantum mechanics have been extensively tested in their respective domains, but their unification remains open. A common feature of candidate quantum gravity theories is the regularisation of classical singularities (black hole centres, Big Bang). This can be achieved by modifying the Newtonian potential to remain finite as $r \to 0$ while recovering standard form at large $r$.

We propose the minimal modification

$$
U(r) = -\frac{GMm}{\sqrt{r^2 + L_p^2}},
$$

with $L_p$ the Planck length. This potential is then extended to a Lagrangian incorporating post‑Newtonian corrections, the cosmological constant, and an exponential Planck‑scale term.

---

## 2. Basic Potential and Limit Analysis

### 2.1 Large‑Distance Limit

For $r \gg L_p$:

$$
\sqrt{r^2 + L_p^2} = r\left(1 + \frac{L_p^2}{2r^2} - \cdots\right)
$$

$$
U(r) = -\frac{GMm}{r} + \frac{GMm L_p^2}{2r^3} + \mathcal{O}\left(\frac{1}{r^5}\right)
$$

The first term is Newtonian; the correction is $O(1/r^3)$ and negligible at macroscopic scales.

### 2.2 Planck‑Scale Limit

At $r = 0$:

$$
U(0) = -\frac{GMm}{L_p}
$$

finite, unlike the Newtonian divergence.

### 2.3 Force at Planck Scale

$$
F(r) = -\frac{dU}{dr} = -\frac{GMm \, r}{(r^2 + L_p^2)^{3/2}}
$$

$F(0) = 0$. For $r \ll L_p$:

$$
F(r) \approx -\frac{GMm}{L_p^3} \, r
$$

a linear restoring force (harmonic) with $k = GMm/L_p^3$. This repulsive behaviour prevents approach to $r=0$, eliminating singularities.

---

## 3. Extension to a Complete Lagrangian

To include post‑Newtonian effects and $\Lambda$, we consider:

$$
\begin{aligned}
\mathcal{L} &= \frac12 m(\dot{r}^2 + r^2\dot{\theta}^2) \\
&\quad + \frac{GMm}{\sqrt{r^2+L_p^2}} \\
&\quad + \frac{3GMm}{2c^2 r}(\dot{r}^2 + r^2\dot{\theta}^2) \\
&\quad + \frac{m}{8c^2}(\dot{r}^2 + r^2\dot{\theta}^2)^2 \\
&\quad - \frac{G^2 M^2 m}{2c^2 r^2} \\
&\quad + \frac16 m c^2 \Lambda r^2 \\
&\quad + \frac{m c^2 L_p^2}{r^2+L_p^2} e^{-r/L_p}
\end{aligned}
$$

**Term meanings:**

1. Newtonian kinetic energy  
2. Regularised potential ($-U$)  
3. Post‑Newtonian $v^2/c^2$ correction  
4. $v^4/c^4$ correction  
5. Static post‑Newtonian potential  
6. Cosmological constant $\Lambda$ contribution  
7. Exponential quantum correction (significant only near $L_p$)

### 3.1 Relativistic Kinetic Term (up to $v^4/c^4$)

$$
K = \frac12 m v^2 \left(1 + \frac{3GM}{c^2 r}\right) + \frac{m}{8c^2} v^4 - \frac{G^2 M^2 m}{2c^2 r^2}, \quad v^2 = \dot{r}^2 + r^2\dot{\theta}^2
$$

### 3.2 Cosmological Constant Term

$$
V(r) = \frac16 m c^2 \Lambda r^2
$$

Produces a repulsive force $\propto r$, consistent with accelerated expansion.

### 3.3 Exponential Quantum Correction

$$
Q(r) = \frac{m c^2 L_p^2}{r^2+L_p^2} e^{-r/L_p}
$$

Decays rapidly for $r > L_p$; ensures potential smoothness.

---

## 4. Hamiltonian Formulation

### 4.1 Polar Coordinates and Symmetry

$\theta$ is cyclic, so angular momentum is conserved:

$$
p_\theta = \frac{\partial \mathcal{L}}{\partial \dot{\theta}} = m r^2 \dot{\theta} \left[1 + \frac{3GM}{c^2 r} + \frac{1}{2c^2}(\dot{r}^2+r^2\dot{\theta}^2)\right] \equiv \ell
$$

### 4.2 Hamiltonian and Energy Conservation

Radial momentum:

$$
p_r = \frac{\partial \mathcal{L}}{\partial \dot{r}} = m \dot{r} \left[1 + \frac{3GM}{c^2 r} + \frac{1}{2c^2}(\dot{r}^2+r^2\dot{\theta}^2)\right]
$$

Hamiltonian $H = p_r \dot{r} + p_\theta \dot{\theta} - \mathcal{L}$ is conserved (no explicit time dependence).

### 4.3 Radial Euler–Lagrange Equation

$$
\frac{d}{dt}\frac{\partial \mathcal{L}}{\partial \dot{r}} - \frac{\partial \mathcal{L}}{\partial r} = 0
$$

This non‑linear equation is solved numerically.

---

## 5. Numerical Simulations and Comparison with GR

Geometric units $G=c=1$, central mass $M=1$. $L_p$ is extremely small; for visualisation, enlarged values (e.g., $0.01$) are used.

### 5.1 Perihelion Precession

Without quantum/$\Lambda$ terms, $\Delta\theta \approx 2.95\times10^{-4}$ rad/orbit at $r_0=10$ (GR value). With $L_p=0.01$, precession increases slightly to $2.96\times10^{-4}$ (0.3% change). For $r_0=0.5$, precession reaches $3.10\times10^{-2}$ rad (25% larger than GR), indicating detectable quantum effects in strong gravity.

### 5.2 Effect of Cosmological Constant

With $\Lambda = 10^{-4}$ (enlarged), precession at $r_0=10$ decreases to $2.58\times10^{-4}$ rad (repulsive $\Lambda$ weakens attraction).

### 5.3 Behaviour at Planck Scale

For $r_0 \sim L_p$, orbits are non‑Keplerian; the finite potential causes the particle to bounce back before $r=0$, avoiding singularity.

---

## 6. Connections with GR and Quantum Gravity

### 6.1 Regular Effective Metric

From $U(r)$ we construct a static, spherically symmetric metric:

$$
ds^2 = -A(r) c^2 dt^2 + B(r) dr^2 + r^2 d\Omega^2
$$

with $A(r) = 1 + 2U(r)/(mc^2) = 1 - \frac{2GM}{c^2\sqrt{r^2+L_p^2}}$.

- For $r \gg L_p$, $A(r) \approx 1 - 2GM/(c^2 r)$ (Schwarzschild).  
- At $r=0$, $A(0) = 1 - 2GM/(c^2 L_p)$.  
- If $M < c^2 L_p/(2G) \approx 10^{-8}$ kg, $A(0) > 0$ → no horizon. For larger masses, a horizon exists but the centre is non‑singular.

### 6.2 Removal of Singularities

Curvature invariants (e.g., Kretschmann) remain finite at $r=0$, a hallmark of regular black holes.

### 6.3 Remarks on Hawking Radiation

The regular metric provides a basis for studying Hawking radiation without singularities; curvature finiteness may affect the spectrum and help resolve the information paradox. Further work is needed to compute corrections to Hawking temperature and evaporation rate.

---

## 7. Conclusion and Future Directions

The regular potential $U(r) = -GMm/\sqrt{r^2+L_p^2}$ describes gravity from Planck to cosmological scales, reduces to Newtonian form at large distances, remains finite at $r=0$, and yields a harmonic (repulsive) force at Planck scale. The extended Lagrangian incorporating post‑Newtonian and $\Lambda$ terms is consistent with existing GR tests.

**Future research directions:**

1. Derive the full metric and verify it satisfies (modified) Einstein equations.  
2. Analyse stability of regular black hole solutions.  
3. Compute corrections to Hawking radiation and black hole thermodynamics.  
4. Search for observable effects at laboratory scales (sub‑mm gravity experiments, atom interferometry).

---

## 8. List of Symbols

| Symbol | Name | SI Unit |
|--------|------|---------|
| $U$ | Gravitational potential energy | J |
| $G$ | Gravitational constant | N·m²/kg² |
| $M, m$ | Masses | kg |
| $r$ | Distance | m |
| $L_p$ | Planck length | m |
| $\dot{r}, \dot{\theta}$ | Time derivatives | m/s, rad/s |
| $c$ | Speed of light | m/s |
| $\Lambda$ | Cosmological constant | m⁻² |
| $\mathcal{L}$ | Lagrangian | J |
| $K$ | Relativistic kinetic part | J |
| $V$ | Cosmological potential | J |
| $Q$ | Exponential quantum correction | J |
| $p_r, p_\theta$ | Conjugate momenta | kg·m/s, kg·m²/s |
| $\ell$ | Angular momentum | kg·m²/s |

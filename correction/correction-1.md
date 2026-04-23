# Correction 

## 1. Why a Correction Was Needed

The original formulation, while successfully removing singularities via

$$U(r)=-\frac{GMm}{\sqrt{r^{2}+L_{p}^{2}}},$$

relied on a particle‑only Lagrangian that included:

- an **ad‑hoc exponential quantum correction** without derivation,
- terms directly inserted into a non‑covariant mechanical Lagrangian,
- no clear path to a metric‑based, generally covariant description.

These features made the theory **phenomenological but not fundamental**.  
The correction aims to:

1. **Remove all "by‑hand" terms** (especially the exponential correction).
2. **Embed the regularisation into a covariant action**.
3. **Provide a geometric interpretation** (vortex field $\Phi(r)$ that naturally explains the regularisation.
4. **Ensure that standard GR**, Newtonian gravity, and Maxwell–Dirac matter fields are recovered in the appropriate limits.

---

## 2. What Has Changed – Summary Table

| Aspect | Original (main-theory.md) | Corrected (URVG) |
|--------|---------------------------|------------------|
| Core potential | $U(r)=-\frac{GMm}{\sqrt{r^{2}+L_{p}^{2}}}$ | **Unchanged** – the same regularised potential remains the foundation. |
| Extra quantum term | $\frac{m c^{2} L_{p}^{2}}{r^{2}+L_{p}^{2}} e^{-r/L_{p}}$ added by hand | **Removed** – replaced by a geometric vortex field in the action. |
| Formulation level | Particle Lagrangian (mechanics) | **Covariant effective action** (field theory). |
| Metric | $A(r)=1-\frac{2GM}{c^{2}\sqrt{r^{2}+L_{p}^{2}}}$ (just cited) | **Same metric**, but derived from $f(r)=1-\frac{2GM}{c^{2}\sqrt{r^{2}+L_{p}^{2}}}$ in a proper line element. |
| Gravitational action | No action; only a particle Lagrangian with post‑Newtonian terms | **Einstein–Hilbert term + vortex‑curvature coupling + $\Lambda$ term** |
| New field | None | **Vortex structural field** $\Phi(r) = \frac{L_{p}^{2}}{r^{2}+L_{p}^{2}}$ that modulates gravity at Planck scales. |
| Status | Ansatz model | **Effective covariant regularised gravity** with a transparent limit structure. |

---

## 3. The Corrected Core: Unified Regularized Vortex Gravity (URVG)

### 3.1 Guiding Principle – Finite Curvature

> **All geometric quantities (potential, force, curvature invariants) must remain finite for all $r\ge 0$, with the Planck length $L_{p}$ acting as the minimal spatial scale.**

No singularities are permitted; the classical Newtonian and Schwarzschild singularities are regularised by the substitution $r \to \sqrt{r^{2}+L_{p}^{2}}$.

### 3.2 The Regularised Potential and Force

The potential is left exactly as originally proposed:

$$
U(r)=-\frac{GMm}{\sqrt{r^{2}+L_{p}^{2}}}
$$

- For $r \gg L_{p}$: $U(r) \approx -\frac{GMm}{r} + \frac{GMm L_{p}^{2}}{2r^{3}}$ (Newton + tiny correction).  
- For $r \ll L_{p}$: $U(r) \approx -\frac{GMm}{L_{p}}$ (finite, constant core).  

The force law becomes:

$$
F(r) = -\frac{GMm\,r}{(r^{2}+L_{p}^{2})^{3/2}}
$$

- $F(0)=0$ – no infinite force at the centre.  
- For $r \ll L_{p}$: $F(r) \approx -\frac{GMm}{L_{p}^{3}}\,r$, a harmonic restoring behaviour.

### 3.3 Covariant Metric

The regularisation is embedded into a static, spherically symmetric metric:

$$
ds^{2} = -f(r)c^{2}dt^{2} + \frac{1}{f(r)}dr^{2} + r^{2}d\Omega^{2},
$$

with

$$
f(r) = 1 - \frac{2GM}{c^{2}\sqrt{r^{2}+L_{p}^{2}}}.
$$

- As $r\to\infty$, $f(r)\to 1 - \frac{2GM}{c^{2}r}$ (Schwarzschild recovered).  
- At $r=0$, $f(0)=1 - \frac{2GM}{c^{2}L_{p}}$, which is finite. All curvature invariants (e.g., Kretschmann scalar) remain bounded.

### 3.4 Vortex Structural Field

To give geometric meaning to the regularisation, we introduce a field that measures the “Planck‑scale activity” of spacetime:

$$
\Phi(r) = \frac{L_{p}^{2}}{r^{2}+L_{p}^{2}}.
$$

- $\Phi \approx 1$ in the deep core ($r \ll L_{p}$) – spacetime is in a **vortex state**, resisting further collapse.  
- $\Phi \approx 0$ for $r \gg L_{p}$ – ordinary flat/curved spacetime.

This field is not a matter field; it is a **geometric scalar** that controls the modification of the gravitational interaction at small scales.

### 3.5 Effective Action

The entire framework is now encoded in a **single covariant action**:

$$
S = \int d^{4}x \sqrt{-g} \left[ \frac{c^{4}}{16\pi G} R \;-\; \eta R \,\Phi(r) \;-\; \frac{1}{6}\Lambda c^{2} r^{2} \right] + S_{\text{matter}} .
$$

**Breakdown:**
- **Einstein term** $\frac{c^{4}}{16\pi G}R$ – standard general relativity.
- **Vortex‑curvature coupling** $-\eta R\,\Phi(r)$ – with a dimensionless constant $\eta$, this term activates the regularisation only where $\Phi$ is non‑zero (near $r\sim L_{p}$). It vanishes in the large‑distance limit, leaving pure GR.
- **Cosmological constant term** – included to account for dark energy on cosmological scales.
- **Matter sector** $S_{\text{matter}}$ – encompasses the Standard Model fields (e.g., Maxwell and Dirac) minimally coupled to the metric $g_{\mu\nu}$.
All post‑Newtonian corrections previously inserted by hand now emerge naturally from the expansion of this metric in the weak‑field, slow‑motion limit.

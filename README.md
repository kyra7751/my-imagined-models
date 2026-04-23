# Vortex Theory – A Speculative Geometric Framework for Gravity and Quantum Physics

**Author:** Kyra (self‑taught beginner in mathematics)  
**Repository archive date:** 2026  

This repository documents an original, exploratory idea called **Vortex Theory**. It attempts to unify Newtonian gravity, general relativity, and quantum‑mechanical stability through simple geometric patterns ($x^{-2}$ and $x^{2}$).  

> **Disclaimer**  
> This is a **personal, early‑stage theoretical proposal** written by someone who is learning mathematics from scratch.  
> The theory has **not been peer‑reviewed or experimentally validated**. It is shared as an open‑ended thinking exercise, not as established physics.  
> All equations and simulations are **speculative** and may contain errors or misconceptions.

---

## Repository Contents

| File | Description |
|------|-------------|
| `README.md` | This file |
| `INTRODUCTION.md` | Full theoretical introduction (English) with symbol definitions |
| `idea-1.md` … `idea-4.md` | Early manuscript versions (historical record) |
| `main-theory.md` | Alternative regularization form $U(r) = -GMm/\sqrt{r^2+L_p^2}$ |
| `testing-1.py` … `testing-7.py` | Python scripts for visualisation and simulation (see below) |

### Python scripts (demos)

| Script | What it shows |
|--------|----------------|
| `testing-1.py` | Duality potential $V_{\text{total}} = m c^2(L_p^2/r^2 + r^2/L_p^2)$ and force |
| `testing-2.py` | Vortex metric $f(r) = 1 - 2GM/(c^2 r) + \gamma L_p^2/r^2$ |
| `testing-3.py` | Time animation of a stable orbit (x, y, z, t) |
| `testing-4.py` | 2D + 3D interactive plot of core vortex formula $V_x = m c^4 L_p / r^2$ |
| `testing-5.py` | Spacetime curvature + nuclear chain reaction analogy |
| `testing-6.py` | Full 3D orbit with 5‑panel energy decomposition |
| `testing-7.py` | N‑body simulation (50 particles) with Newton, vortex repulsion and $\Lambda$ expansion |

> To run the scripts, install `numpy`, `matplotlib`, `scipy`. Example:  
> `pip install numpy matplotlib scipy`  
> then `python testing-4.py`

---

## Core Ideas in Brief

1. **Basic patterns**  
   - $x^{-2}$ → inward pressure (gravity, electric force)  
   - $x^{2}$ → outward balancing vibration (quantum stability, dark energy)  
   - $\sin(x)$ → oscillation that prevents collapse

2. **Four main equations** (proposed)  
   - **Core vortex formula** $V_x = m c^4 L_p / r^2$ (spacetime pressure rate)  
   - **Duality balance** $V_{\text{total}} = m c^2 (L_p^2/r^2 + r^2/L_p^2)$ (symmetry under $r \leftrightarrow L_p^2/r$)  
   - **Complete Lagrangian** – includes Newton, post‑Newtonian, Planck‑scale cutoff, cosmological constant  
   - **Vortex metric** $f(r) = 1 - \frac{2GM}{c^2 r} + \frac{\gamma L_p^2}{r^2}$ (regular black hole, no singularity)

3. **Key symbols** (see `INTRODUCTION.md` for full list)  
   - $c$ – speed of light  
   - $G$ – gravitational constant  
   - $L_p = \sqrt{\hbar G/c^3}$ – Planck length  
   - $\Lambda$ – cosmological constant  
   - $\gamma$ – dimensionless vortex parameter (≈1)

---

## How to Use This Archive

- **Read `INTRODUCTION.md` first** – it explains the physical motivation, defines every symbol, and states clearly that the theory is **untested and speculative**.  
- **Run the Python scripts** to visualise the mathematical behaviour of the proposed equations (not as physical predictions, but as geometric explorations).  
- **Do not cite as established science** – treat it as a personal learning archive.

---

## License

This work is shared under the **MIT License** – you are free to use, modify, and distribute the code and text, provided you include the original disclaimer and attribution.  
No claim of validity or correctness is made.

---

## Author’s Note

I am a beginner learning mathematics on my own. These documents and codes are part of my learning process.  
If you find errors or have suggestions, please feel free to open an issue – I welcome constructive feedback.

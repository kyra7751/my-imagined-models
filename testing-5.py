"""
╔══════════════════════════════════════════════════════════════════════════╗
║   VORTEX SPACETIME CURVATURE  ·  Nuclear Chain Reaction                 ║
║                                                                          ║
║   Metric:  f(r) = 1 - 2GM/r + (Lp²/r²)·e^{-r/Lp} + (Λ/6)·r²             ║
║   Neutron geodesic force: F = -∇φ(x,y)                                   ║
║                                                                          ║
║   Left Panel  : 3D grid of real-time deforming spacetime curvature      ║
║   Right Panel : N-body neutrons on curvature heatmap                    ║
║                 Red   = φ<0  Vortex In  (compression / gravity well)    ║
║                 Blue  = φ>0  Vortex Out (expansion / shockwave ring)    ║
║                                                                          ║
║   Install: pip install numpy matplotlib scipy                            ║
║   Run: python vortex_spacetime.py                                        ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import TwoSlopeNorm, Normalize
from matplotlib.cm import ScalarMappable
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from scipy.ndimage import gaussian_filter
import warnings
warnings.filterwarnings("ignore")

# ════════════════════════════════════════════════════════════════
#  PHYSICAL CONSTANTS  (Natural Units: G=c=1)
# ════════════════════════════════════════════════════════════════
G          = 1.0
c          = 1.0
Lp         = 0.42          # Planck length (enlarged for visibility)
LAM        = 0.009         # Cosmological constant Λ
BOX        = 9.0           # Box radius
SOFT       = 0.20          # Softening (prevents numerical singularities)
FISSION_R  = 0.52          # Fission detection radius
MAX_NEUT   = 110           # Maximum number of active neutrons
NUC_MASS   = 2.2           # Mass of each nucleus

DT                = 0.016
STEPS_PER_FRAME   = 3
SAVE_GIF          = False  # True → export vortex_spacetime.gif (requires Pillow)

rng = np.random.default_rng(42)

# ════════════════════════════════════════════════════════════════
#  SPACETIME GRID
# ════════════════════════════════════════════════════════════════
NG    = 54
x1d   = np.linspace(-BOX, BOX, NG)
y1d   = np.linspace(-BOX, BOX, NG)
XX, YY = np.meshgrid(x1d, y1d)          # (NG, NG) coordinate grid
R_GRID = np.sqrt(XX**2 + YY**2)

# ════════════════════════════════════════════════════════════════
#  NUCLEI  — 5×5 grid
# ════════════════════════════════════════════════════════════════
_sp   = 3.0
_gv   = np.arange(-2, 3) * _sp
_gx, _gy = np.meshgrid(_gv, _gv)
NUC_POS   = np.column_stack([_gx.ravel(), _gy.ravel()])   # (25, 2)
N_NUC     = len(NUC_POS)
nuc_mass  = np.full(N_NUC, NUC_MASS)
nuc_alive = np.ones(N_NUC, dtype=bool)
nuc_fiss_t= np.full(N_NUC, np.inf)       # fission time for each nucleus

# ════════════════════════════════════════════════════════════════
#  NEUTRON STATE  (dynamic list)
# ════════════════════════════════════════════════════════════════
neut_pos  = []
neut_vel  = []
neut_live = []

# 4 initial neutrons fired from the left
for _ky in [-1.5, -0.5, 0.5, 1.5]:
    neut_pos.append([-BOX * 0.93, _ky])
    neut_vel.append([2.8, rng.uniform(-0.15, 0.15)])
    neut_live.append(True)

# Shockwave: list (cx, cy, t_birth, amplitude)
shockwaves    = []
fission_count = 0
t_sim         = [0.0]

# ════════════════════════════════════════════════════════════════
#  SCALAR POTENTIAL  φ(x,y)
# ════════════════════════════════════════════════════════════════
def scalar_phi_grid():
    """
    φ(x,y) = Σ_i [ -2GM/rᵢ + (Lp²/rᵢ²)·e^{-rᵢ/Lp} ]
             + Σ_shock [Gaussian ring]
             + (Λ/6)·R²
    """
    phi   = np.zeros((NG, NG))
    t_now = t_sim[0]

    # ── Active nuclei (vectorised NxNG×NG) ──────────────
    active = np.where(nuc_alive)[0]
    if len(active):
        xn = NUC_POS[active, 0]
        yn = NUC_POS[active, 1]
        mn = nuc_mass[active]                                # (Na,)
        # Broadcasting: (NG, NG, Na)
        dx = XX[:, :, None] - xn
        dy = YY[:, :, None] - yn
        r  = np.sqrt(dx**2 + dy**2 + SOFT**2)
        # Metric potential terms: -2GM/r + (Lp²/r²)·e^{-r/Lp}
        phi_n = (-2.0 * G * mn / r
                 + (Lp**2 / r**2) * np.exp(-np.clip(r / Lp, 0, 700)))
        phi  += phi_n.sum(axis=-1)

    # ── Shockwave (expanding Gaussian ring) ──────────────
    for (cx, cy, tb, A) in shockwaves:
        age = t_now - tb
        if age < 0 or age > 9.0:
            continue
        r_ring = 2.4 * age
        sigma  = 0.65 + 0.38 * age
        rpts   = np.sqrt((XX - cx)**2 + (YY - cy)**2)
        phi   += A * np.exp(-(rpts - r_ring)**2 / (2 * sigma**2)) \
                   * np.exp(-age * 0.22)

    # ── Lambda: potential wall (Vortex Boundary) ─────
    phi += (LAM / 6.0) * R_GRID**2

    return phi


# ════════════════════════════════════════════════════════════════
#  GEODESIC FORCE  F = −∇φ  at neutron positions
# ════════════════════════════════════════════════════════════════
def force_at_points(pts):
    """
    pts: (M, 2) neutron positions
    Return: (M, 2) acceleration = -∇φ
    """
    M = len(pts)
    if M == 0:
        return np.zeros((0, 2))

    t_now = t_sim[0]
    gx    = np.zeros(M)
    gy    = np.zeros(M)

    # Lambda restoring: ∇[(Λ/6)R²] = (Λ/3)·pos  → F = -(Λ/3)·pos
    gx += (LAM / 3.0) * pts[:, 0]
    gy += (LAM / 3.0) * pts[:, 1]

    # ── Active nuclei ────────────────────────────────────
    active = np.where(nuc_alive)[0]
    if len(active):
        xn = NUC_POS[active, 0]
        yn = NUC_POS[active, 1]
        mn = nuc_mass[active]                                # (Na,)

        dx = pts[:, 0:1] - xn        # (M, Na)  Δx = neutron − nucleus
        dy = pts[:, 1:2] - yn
        r  = np.sqrt(dx**2 + dy**2) + SOFT

        # Derivatives of φ with respect to r (per nucleus):
        #   dφ_Newton/dr  = +2GM/r²          → ∇ away from nucleus (net attractive)
        #   dφ_Vortex/dr  = −exp()(2Lp²/r³+Lp/r²)  → ∇ toward nucleus (net repulsive at short range)
        exp_v = np.exp(-np.clip(r / Lp, 0, 700))
        dN    = 2.0 * G * mn / r**2                         # (M, Na) positive
        dV    = exp_v * (2.0 * Lp**2 / r**3 + Lp / r**2)   # (M, Na) positive

        # ∇φ_i = (dN − dV) · (Δ/r)   ; Δ points away from nucleus
        coeff = dN - dV                                      # (M, Na)
        gx   += (coeff * dx / r).sum(axis=1)
        gy   += (coeff * dy / r).sum(axis=1)

    # ── Shockwave gradient ──────────────────────────────
    for (cx, cy, tb, A) in shockwaves:
        age = t_now - tb
        if age < 0 or age > 6.5:
            continue
        r_ring = 2.4 * age
        sigma  = 0.65 + 0.38 * age
        dx2    = pts[:, 0] - cx
        dy2    = pts[:, 1] - cy
        rp     = np.sqrt(dx2**2 + dy2**2) + 1e-7
        decay  = np.exp(-age * 0.22)
        dphi   = (A * decay
                  * (-(rp - r_ring) / sigma**2)
                  * np.exp(-(rp - r_ring)**2 / (2 * sigma**2)))
        gx    += dphi * dx2 / rp
        gy    += dphi * dy2 / rp

    # F = -∇φ
    return -np.column_stack([gx, gy])


# ════════════════════════════════════════════════════════════════
#  PHYSICS STEP  (Velocity-Verlet + fission + boundaries)
# ════════════════════════════════════════════════════════════════
def physics_step():
    global shockwaves, fission_count

    t_now    = t_sim[0]
    live_idx = [i for i, a in enumerate(neut_live) if a]
    if not live_idx:
        t_sim[0] += DT
        return

    pts  = np.array([neut_pos[i] for i in live_idx])   # (M, 2)
    vels = np.array([neut_vel[i] for i in live_idx])

    # ── Velocity Verlet ─────────────────────────────────
    F1    = force_at_points(pts)
    vels += 0.5 * F1 * DT
    pts  += vels * DT
    F2    = force_at_points(pts)
    vels += 0.5 * F2 * DT

    # Clip maximum speed
    vmag = np.linalg.norm(vels, axis=1, keepdims=True)
    mask = vmag[:, 0] > 5.8
    if mask.any():
        vels[mask] = vels[mask] / vmag[mask] * 5.8

    # ── Spherical boundary (Vortex Boundary) ────────────────────
    rmag = np.linalg.norm(pts, axis=1)
    out  = rmag > BOX * 0.94
    if out.any():
        rhat        = pts[out] / (rmag[out, None] + 1e-9)
        vr          = (vels[out] * rhat).sum(axis=1, keepdims=True)
        vels[out]  -= 2.0 * vr * rhat          # elastic reflection
        pts[out]    = rhat * (BOX * 0.92)

    # Write back to lists
    for k, i in enumerate(live_idx):
        neut_pos[i] = pts[k].tolist()
        neut_vel[i] = vels[k].tolist()

    # ── Fission detection ─────────────────────────────────────
    new_neutrons = []
    for k, i in enumerate(live_idx):
        if not neut_live[i]:
            continue
        np_pos = pts[k]
        for j in range(N_NUC):
            if not nuc_alive[j]:
                continue
            if np.linalg.norm(np_pos - NUC_POS[j]) < FISSION_R:
                # ── FISSION OCCURS ──
                nuc_alive[j]    = False
                nuc_fiss_t[j]   = t_now
                fission_count  += 1
                neut_live[i]    = False          # trigger neutron destroyed

                # Shockwave
                shockwaves.append(
                    (NUC_POS[j, 0], NUC_POS[j, 1], t_now, 1.5)
                )

                # Emit 2–3 fission product neutrons
                n_emit = rng.integers(2, 4)
                for _ in range(n_emit):
                    theta = rng.uniform(0, 2 * np.pi)
                    speed = rng.uniform(2.2, 3.8)
                    offset = rng.uniform(-0.12, 0.12, 2)
                    new_neutrons.append((
                        (NUC_POS[j] + offset).tolist(),
                        [speed * np.cos(theta), speed * np.sin(theta)]
                    ))
                break

    # Add new neutrons (if under limit)
    n_alive = sum(neut_live)
    for (pp, vv) in new_neutrons:
        if n_alive < MAX_NEUT:
            neut_pos.append(pp)
            neut_vel.append(vv)
            neut_live.append(True)
            n_alive += 1

    # Remove old shockwaves
    shockwaves = [(cx, cy, tb, A)
                  for (cx, cy, tb, A) in shockwaves
                  if t_now - tb < 9.0]

    t_sim[0] += DT


# ════════════════════════════════════════════════════════════════
#  FIGURE & AXES
# ════════════════════════════════════════════════════════════════
plt.style.use('dark_background')
fig = plt.figure(figsize=(21, 10), facecolor='#02020c')
fig.suptitle(
    'VORTEX SPACETIME CURVATURE  ·  '
    r'f(r) = 1 − 2GM/r + (L$_p^2$/r²)e$^{-r/L_p}$ + (Λ/6)r²'
    '   ·   Nuclear Chain Reaction',
    color='#5577bb', fontsize=11, fontweight='bold', y=0.998
)

gs = gridspec.GridSpec(
    1, 2, figure=fig, wspace=0.05,
    left=0.02, right=0.97, bottom=0.05, top=0.95
)
ax3d = fig.add_subplot(gs[0], projection='3d')
ax2d = fig.add_subplot(gs[1])

# ── 2D panel ──────────────────────────────────────────────────
ax2d.set_facecolor('#03030e')
for sp in ax2d.spines.values():
    sp.set_edgecolor('#151540')
ax2d.tick_params(colors='#2d3e66', labelsize=7.5)
ax2d.set_xlim(-BOX, BOX)
ax2d.set_ylim(-BOX, BOX)
ax2d.set_aspect('equal')
ax2d.set_xlabel('x  [natural units]', color='#3d5088', fontsize=9)
ax2d.set_ylabel('y  [natural units]', color='#3d5088', fontsize=9)
ax2d.set_title('N-Body: Neutrons on Vortex Spacetime Geodesics',
               color='#8899dd', fontsize=10, pad=5)

# Colorbar 2D
norm2 = TwoSlopeNorm(vmin=-4.5, vcenter=0.0, vmax=2.0)
sm2   = ScalarMappable(cmap='RdBu_r', norm=norm2)
sm2.set_array([])
cb2   = fig.colorbar(sm2, ax=ax2d, pad=0.012, shrink=0.88,
                      aspect=30, location='right')
cb2.set_label(
    'φ(x,y)  |  Red = Vortex In (well/compression)  '
    'Blue = Vortex Out (expansion/Λ)',
    color='#5566aa', fontsize=7.5
)
cb2.ax.tick_params(colors='#3a4e77', labelsize=6.5)

# Heatmap
hmap = ax2d.imshow(
    np.zeros((NG, NG)),
    extent=[-BOX, BOX, -BOX, BOX],
    origin='lower', cmap='RdBu_r', norm=norm2,
    aspect='equal', zorder=1, alpha=0.87
)

# Nuclei scatter
nuc_scat = ax2d.scatter(
    NUC_POS[:, 0], NUC_POS[:, 1],
    s=78, c='#2dff70', zorder=5,
    linewidths=0.8, edgecolors='#174430', alpha=0.93
)

# Neutron scatter
neut_scat = ax2d.scatter(
    [], [], s=16, c='#ffec30', zorder=6,
    linewidths=0, alpha=0.93
)

# Info text box
info_box = ax2d.text(
    -BOX * 0.96, BOX * 0.87, '',
    color='#99bbdd', fontsize=9, va='top',
    fontfamily='monospace', linespacing=1.75, zorder=10,
    bbox=dict(facecolor='#060618', edgecolor='#181848',
              alpha=0.78, boxstyle='round,pad=0.45')
)

# Legend
legend_items = [
    mpatches.Patch(color='#2dff70', label='Nucleus (intact)'),
    mpatches.Patch(color='#ff4400', label='Nucleus (fissioned)'),
    mpatches.Patch(color='#ffec30', label='Neutron (geodesic)'),
    mpatches.Patch(color='#cc1100', label='φ ≪ 0  Vortex In (well)'),
    mpatches.Patch(color='#0033cc', label='φ > 0  Vortex Out (expansion)'),
]
ax2d.legend(handles=legend_items, fontsize=7.5, loc='lower right',
            facecolor='#060618', edgecolor='#151540',
            labelcolor='white', framealpha=0.9)

# Footer
fig.text(
    0.5, 0.003,
    '⬡  Geodesic = −∇φ  ·  Shockwave = expanding Gaussian ring  '
    '·  Boundary = Vortex Boundary (Λ·r² wall + elastic reflection)  '
    '·  Red=Vortex In  Blue=Vortex Out',
    ha='center', color='#181840', fontsize=7.5
)

# ── 3D panel (header-only; content filled each frame) ──────────
ax3d.set_facecolor('#020210')


# ════════════════════════════════════════════════════════════════
#  ANIMATION FUNCTION
# ════════════════════════════════════════════════════════════════
def animate(frame):
    # ── Physics integration ─────────────────────────────────
    for _ in range(STEPS_PER_FRAME):
        physics_step()

    t_now = t_sim[0]

    # ── Compute potential ─────────────────────────────────
    phi   = scalar_phi_grid()
    phi_s = gaussian_filter(phi, sigma=0.75)    # light smoothing

    # ════════════════════════════════
    #  UPDATE RIGHT PANEL (2D)
    # ════════════════════════════════
    hmap.set_data(phi_s)

    # Nuclei colours
    col_nuc = []
    for j in range(N_NUC):
        if nuc_alive[j]:
            col_nuc.append('#2dff70')
        else:
            age     = t_now - nuc_fiss_t[j]
            bright  = max(0.12, 1.0 - age * 0.11)
            r_val   = min(1.0, age / 3.5)
            col_nuc.append((1.0, 0.17 * (1 - r_val), 0.0, bright))
    nuc_scat.set_facecolor(col_nuc)

    # Live neutron positions
    live_pts = [neut_pos[i] for i, a in enumerate(neut_live) if a]
    if live_pts:
        neut_scat.set_offsets(np.array(live_pts))
    else:
        neut_scat.set_offsets(np.empty((0, 2)))

    # Info
    phi_min = phi_s.min()
    phi_max = phi_s.max()
    info_box.set_text(
        f' t          = {t_now:.2f}\n'
        f' Fission    = {fission_count} / {N_NUC}\n'
        f' Neutron    = {sum(neut_live)}\n'
        f' Nuclei     = {nuc_alive.sum()}\n'
        f' Shockwave  = {len(shockwaves)}\n'
        f' φ min/max  = {phi_min:.2f} / {phi_max:.2f}'
    )

    # ════════════════════════════════
    #  UPDATE LEFT PANEL (3D)
    # ════════════════════════════════
    ax3d.clear()
    ax3d.set_facecolor('#020210')
    ax3d.set_xlabel('x', color='#2e4066', fontsize=7, labelpad=1)
    ax3d.set_ylabel('y', color='#2e4066', fontsize=7, labelpad=1)
    ax3d.set_zlabel('φ (curvature)', color='#2e4066', fontsize=7, labelpad=1)
    ax3d.set_title(
        '3D Spacetime Curvature Grid\n'
        r'Red=Vortex In  ·  Blue=Vortex Out/Λ',
        color='#6677cc', fontsize=8.5, pad=2
    )
    ax3d.tick_params(colors='#141e33', labelsize=5)

    # Downsample grid for performance
    sk  = 3
    Xs  = XX[::sk, ::sk]
    Ys  = YY[::sk, ::sk]
    Zs  = np.clip(phi_s[::sk, ::sk], -5.5, 2.8)

    # Per‑facet colours from RdBu_r
    norm3   = Normalize(vmin=-5.5, vmax=2.8)
    fcolors = plt.cm.RdBu_r(norm3(Zs))

    # Surface with shading
    ax3d.plot_surface(
        Xs, Ys, Zs,
        facecolors=fcolors,
        alpha=0.90, linewidth=0,
        rstride=1, cstride=1,
        antialiased=False, shade=True
    )

    # Thin wireframe overlay
    ax3d.plot_wireframe(
        Xs, Ys, Zs,
        color='#0a0a28', linewidth=0.22,
        alpha=0.38, rstride=2, cstride=2
    )

    ax3d.set_xlim(-BOX, BOX)
    ax3d.set_ylim(-BOX, BOX)
    ax3d.set_zlim(-6.0, 3.5)

    # Automatic camera rotation (elevation oscillates slowly)
    ax3d.view_init(
        elev=28 + 8 * np.sin(frame * 0.011),
        azim=frame * 0.28
    )

    # Mark explosion points on 3D grid
    for j in np.where(~nuc_alive)[0]:
        age = t_now - nuc_fiss_t[j]
        if age > 6.0:
            continue
        # Find Z at nucleus position
        ix = int(np.clip(
            (NUC_POS[j, 0] + BOX) / (2 * BOX) * (NG - 1), 0, NG - 1))
        iy = int(np.clip(
            (NUC_POS[j, 1] + BOX) / (2 * BOX) * (NG - 1), 0, NG - 1))
        z_mark = phi_s[iy, ix] + 0.5
        alpha  = max(0.08, 1.0 - age * 0.16)
        ax3d.scatter(
            [NUC_POS[j, 0]], [NUC_POS[j, 1]], [z_mark],
            c=[[1.0, 0.28, 0.0, alpha]],
            s=40, marker='*', zorder=15
        )

    # Neutrons on 3D surface
    live_pts = np.array([neut_pos[i]
                          for i, a in enumerate(neut_live) if a])
    if len(live_pts):
        # Interpolate Z from grid
        ix_n = np.clip(
            ((live_pts[:, 0] + BOX) / (2 * BOX) * (NG - 1)).astype(int),
            0, NG - 1)
        iy_n = np.clip(
            ((live_pts[:, 1] + BOX) / (2 * BOX) * (NG - 1)).astype(int),
            0, NG - 1)
        z_n  = phi_s[iy_n, ix_n] + 0.3
        ax3d.scatter(
            live_pts[:, 0], live_pts[:, 1], z_n,
            c='#ffec30', s=12, alpha=0.85,
            zorder=10, linewidths=0
        )

    ax3d.text2D(
        0.02, 0.97,
        f't={t_now:.2f}  fission={fission_count}/{N_NUC}  n={sum(neut_live)}',
        transform=ax3d.transAxes,
        color='#99aacc', fontsize=8.5, va='top',
        fontfamily='monospace'
    )

    return hmap, nuc_scat, neut_scat, info_box


# ════════════════════════════════════════════════════════════════
#  RUN ANIMATION
# ════════════════════════════════════════════════════════════════
print("═" * 70)
print("  VORTEX SPACETIME CURVATURE + NUCLEAR CHAIN REACTION")
print(f"  G={G}  c={c}  Lp={Lp}  Λ={LAM}  BOX={BOX}  DT={DT}")
print(f"  Nuclei={N_NUC}  MaxNeutron={MAX_NEUT}")
print("═" * 70)
print("  Left Panel  : 3D curvature grid deforming in real time")
print("  Right Panel : Heatmap φ + neutrons following geodesics")
print("  Red=Vortex In (φ<0)  ·  Blue=Vortex Out (φ>0)")
print("  Set SAVE_GIF=True to export GIF")
print("═" * 70)

ani = FuncAnimation(
    fig, animate,
    frames=5000,
    interval=32,
    blit=False,
    cache_frame_data=False
)

if SAVE_GIF:
    print("💾 Saving vortex_spacetime.gif ...")
    ani.save('vortex_spacetime.gif',
             writer=PillowWriter(fps=20), dpi=88)
    print("✓ Done!")
else:
    plt.show()
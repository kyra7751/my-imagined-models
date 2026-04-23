"""
╔══════════════════════════════════════════════════════════════════════╗
║        VORTEX N-BODY  ·  Interactive 3D Particle Simulation         ║
║                                                                      ║
║  Physics (Vortex Lagrangian):                                        ║
║  1. Newton attraction   : F = -G·mᵢ·mⱼ / r²                        ║
║  2. Vortex repulsion    : F = +2·m·c²·(Lp²/r³)·exp(-r/Lp)           ║
║  3. Lambda expansion    : F = +(m·c²·Λ/3)·r                         ║
║                                                                      ║
║  Install: pip install numpy matplotlib scipy                         ║
║  Run: python vortex_nbody.py                                         ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────
#  SIMULATION PARAMETERS
# ─────────────────────────────────────────────────────────────────────
N          = 50          # Number of particles
G          = 1.0         # Gravitational constant (natural units)
c          = 1.0         # Speed of light
Lp         = 0.5         # Planck length (natural units)
LAM        = 0.001       # Cosmological constant
BOX        = 12.0        # Box radius (Spherical Container)
DT         = 0.004       # Time step
MASS_RANGE = (0.8, 1.5)  # Particle mass range (random)
V_INIT     = 0.35        # Maximum initial random speed
SOFTENING  = 0.12        # Softening length (prevents numerical singularities)

TRAIL_LEN  = 55          # Particle trail length
RDF_BINS   = 60          # Number of RDF bins
RDF_RMAX   = BOX * 0.45  # Maximum RDF distance
INTERVAL   = 22          # ms per frame
SAVE_GIF   = False       # True → save vortex_nbody.gif

# ─────────────────────────────────────────────────────────────────────
#  PARTICLE INITIALISATION
# ─────────────────────────────────────────────────────────────────────
rng  = np.random.default_rng(42)

# Initial positions: random distribution inside a sphere of radius BOX*0.55
pos  = np.zeros((N, 3))
for k in range(N):
    while True:
        p = rng.uniform(-BOX*0.55, BOX*0.55, 3)
        if np.linalg.norm(p) < BOX * 0.55:
            pos[k] = p
            break

vel  = rng.uniform(-V_INIT, V_INIT, (N, 3))
mass = rng.uniform(*MASS_RANGE, N)

# Trail history: deque via circular buffer
trail_pos  = np.full((TRAIL_LEN, N, 3), np.nan)
trail_head = 0

# RDF buffer (rolling average)
rdf_history = []

# ─────────────────────────────────────────────────────────────────────
#  PHYSICS FUNCTIONS  (fully vectorised via NumPy broadcasting)
# ─────────────────────────────────────────────────────────────────────
def compute_forces_and_energy(pos, vel, mass):
    """
    Compute acceleration and local potential energy for each particle.
    Output: acc (N,3), pot_energy (N,)
    """
    # Difference vectors: delta[i,j] = pos[j] - pos[i]
    delta = pos[np.newaxis, :, :] - pos[:, np.newaxis, :]   # (N,N,3)

    # Distance (with softening ε)
    r2    = np.sum(delta**2, axis=-1) + SOFTENING**2         # (N,N)
    r     = np.sqrt(r2)                                       # (N,N)
    r3    = r2 * r                                            # (N,N)

    # Unit direction vectors (avoid diagonal i=j)
    with np.errstate(invalid='ignore', divide='ignore'):
        rhat = delta / r[:, :, np.newaxis]                    # (N,N,3)
    np.fill_diagonal(r2,  1.0)   # dummy to avoid division by zero on diagonal
    np.fill_diagonal(r,   1.0)
    np.fill_diagonal(r3,  1.0)

    # ── 1. Newton force (attraction) ─────────────────────────────────
    mj       = mass[np.newaxis, :]                            # (1,N)
    F_newt   = -G * mj / r2                                   # (N,N)  scalar

    # ── 2. Planck Vortex force (repulsion) ──────────────────────────
    #    F_vort = +2·c²·(Lp²/r³)·exp(-r/Lp)  per unit mass of particle i
    exp_term = np.exp(-np.clip(r / Lp, 0, 700))
    F_vort   = 2.0 * c**2 * (Lp**2 / r3) * exp_term          # (N,N)

    # ── 3. Cosmological Lambda force (expansion) ──────────────────────
    #    F_lam = (c²·Λ/3)·r   → linear in distance
    F_lam    = (c**2 * LAM / 3.0) * r                         # (N,N)

    # Total scalar force (per unit mass of particle i)
    F_scalar = F_newt + F_vort + F_lam                        # (N,N)

    # Zero out diagonal
    np.fill_diagonal(F_scalar, 0.0)

    # Acceleration vector
    acc = np.sum(F_scalar[:, :, np.newaxis] * rhat, axis=1)   # (N,3)

    # Local potential energy for each particle
    #   V_Newton  = -G·mᵢ·mⱼ / r
    #   V_Vortex  = +c²·Lp²·exp(-r/Lp) / r²  (derived from F_vort)
    #   V_Lambda  = +(c²·Λ/6)·r²
    V_newt = -G * mass[:, np.newaxis] * mj / r                 # (N,N)
    V_vort = c**2 * (Lp**2 / r2) * exp_term                   # (N,N)
    V_lam  = (c**2 * LAM / 6.0) * r2                          # (N,N)

    np.fill_diagonal(V_newt, 0.0)
    np.fill_diagonal(V_vort, 0.0)
    np.fill_diagonal(V_lam,  0.0)

    pot_energy = 0.5 * np.sum(V_newt + V_vort + V_lam, axis=1)  # (N,)

    return acc, pot_energy


def apply_spherical_boundary(pos, vel, radius=BOX):
    """Elastic reflection at spherical wall."""
    r_mag = np.linalg.norm(pos, axis=1, keepdims=True)        # (N,1)
    mask  = (r_mag[:, 0] > radius)
    if mask.any():
        r_hat = pos[mask] / r_mag[mask]
        # Reflect radial velocity component
        v_r   = np.sum(vel[mask] * r_hat, axis=1, keepdims=True)
        vel[mask] -= 2.0 * v_r * r_hat
        # Push back inside
        pos[mask] = r_hat * radius * 0.98
    return pos, vel


def compute_rdf(pos, n_bins=RDF_BINS, r_max=RDF_RMAX):
    """Radial Distribution Function g(r) via pair distances."""
    delta = pos[np.newaxis, :, :] - pos[:, np.newaxis, :]    # (N,N,3)
    r_ij  = np.sqrt(np.sum(delta**2, axis=-1))               # (N,N)
    # Take unique pairs (upper triangle, i < j)
    idx   = np.triu_indices(N, k=1)
    dists = r_ij[idx]

    counts, edges = np.histogram(dists, bins=n_bins,
                                 range=(0, r_max))
    r_mid = 0.5 * (edges[:-1] + edges[1:])
    dr    = edges[1] - edges[0]

    # Normalisation: g(r) = V·counts / (N(N-1)/2 · 4πr²dr)
    V_box  = (4.0/3.0) * np.pi * BOX**3
    n_pair = N * (N - 1) / 2.0
    ideal  = n_pair * (4.0 * np.pi * r_mid**2 * dr) / V_box
    ideal  = np.where(ideal < 1e-12, 1e-12, ideal)
    g_r    = counts / ideal

    return r_mid, g_r


# ─────────────────────────────────────────────────────────────────────
#  SETUP FIGURE  (dark, 3 panels)
# ─────────────────────────────────────────────────────────────────────
plt.style.use('dark_background')
fig = plt.figure(figsize=(19, 10), facecolor='#04040e')
fig.suptitle(
    'VORTEX N-BODY  ·  F = −G·mᵢmⱼ/r²  +  2c²(Lp²/r³)e^{−r/Lp}  +  (c²Λ/3)r'
    f'   |   N={N}  G={G}  Lp={Lp}  Λ={LAM}',
    color='#7799dd', fontsize=10, fontweight='bold', y=0.995
)
plt.subplots_adjust(left=0.04, right=0.97,
                    bottom=0.07, top=0.96,
                    hspace=0.0, wspace=0.35)

gs   = gridspec.GridSpec(2, 2, figure=fig,
                         height_ratios=[1.0, 0.72],
                         hspace=0.38, wspace=0.32)
ax3d = fig.add_subplot(gs[:, 0], projection='3d')  # left: 3D orbits
ax_e = fig.add_subplot(gs[0, 1])                    # top right: energy
ax_r = fig.add_subplot(gs[1, 1])                    # bottom right: RDF

BG = '#07071a'
for ax in [ax_e, ax_r]:
    ax.set_facecolor(BG)
    for sp in ax.spines.values():
        sp.set_edgecolor('#1e2244')
    ax.tick_params(colors='#556688', labelsize=8)

# ── 3D axes ──────────────────────────────────────
ax3d.set_facecolor('#030312')
lim = BOX * 0.9
ax3d.set_xlim(-lim, lim)
ax3d.set_ylim(-lim, lim)
ax3d.set_zlim(-lim, lim)
ax3d.set_xlabel('x', color='#4466aa', fontsize=8, labelpad=2)
ax3d.set_ylabel('y', color='#4466aa', fontsize=8, labelpad=2)
ax3d.set_zlabel('z', color='#4466aa', fontsize=8, labelpad=2)
ax3d.set_title('3D Orbits  ·  colour = local potential energy',
               color='#aabbff', fontsize=9, pad=4)
ax3d.tick_params(colors='#223355', labelsize=6)
ax3d.grid(color='#0e0e2a', linewidth=0.5)

# Container sphere (thin wireframe)
u, v = np.mgrid[0:2*np.pi:36j, 0:np.pi:18j]
xs = BOX * np.cos(u) * np.sin(v)
ys = BOX * np.sin(u) * np.sin(v)
zs = BOX * np.cos(v)
ax3d.plot_wireframe(xs, ys, zs, color='#0d1533', linewidth=0.3,
                    alpha=0.4, rstride=2, cstride=2)

# Colormap for potential energy
cmap   = plt.cm.plasma
norm_e = Normalize(vmin=-8, vmax=0.5)
sm     = ScalarMappable(cmap=cmap, norm=norm_e)
sm.set_array([])
cbar   = fig.colorbar(sm, ax=ax3d, pad=0.01, shrink=0.55,
                       aspect=22, location='left')
cbar.set_label('Local pot. energy', color='#6677aa', fontsize=7)
cbar.ax.tick_params(colors='#445566', labelsize=6)

# Particle scatter and trails
scatter = ax3d.scatter([], [], [], s=22, c=[], cmap=cmap,
                       norm=norm_e, alpha=0.92, zorder=5,
                       edgecolors='none')
# Trails: one Line3D per particle (list)
trail_lines = [ax3d.plot([], [], [],
                          color='#1a1a55', lw=0.6, alpha=0.55)[0]
               for _ in range(N)]

info_txt = ax3d.text2D(0.02, 0.97, '', transform=ax3d.transAxes,
                        color='#99bbdd', fontsize=8.5, va='top',
                        fontfamily='monospace')
stat_txt = ax3d.text2D(0.02, 0.83, '', transform=ax3d.transAxes,
                        color='#6688bb', fontsize=7.8, va='top',
                        fontfamily='monospace', linespacing=1.65)

# ── Total energy vs time ────────────────────────
ax_e.set_facecolor(BG)
ax_e.set_title('System energy vs time', color='#aabbff', fontsize=9)
ax_e.set_xlabel('step', color='#556688', fontsize=8)
ax_e.set_ylabel('Specific energy', color='#556688', fontsize=8)
e_kin_hist = []
e_pot_hist = []
e_tot_hist = []
step_hist  = []
ln_kin, = ax_e.plot([], [], color='#ffaa33', lw=1.1, label='T kinetic')
ln_pot, = ax_e.plot([], [], color='#44aaff', lw=1.1, label='V potential')
ln_tot, = ax_e.plot([], [], color='#ffffff', lw=1.4, ls='--', label='E total')
ax_e.legend(fontsize=7, labelcolor='white', ncol=3,
            facecolor='#0a0a22', edgecolor='none', loc='upper right')

# ── RDF ─────────────────────────────────────────
ax_r.set_facecolor(BG)
ax_r.set_title('Radial Distribution Function g(r)', color='#aabbff', fontsize=9)
ax_r.set_xlabel('r  [natural units]', color='#556688', fontsize=8)
ax_r.set_ylabel('g(r)', color='#556688', fontsize=8)
ax_r.axhline(1.0, color='#334466', lw=0.8, ls=':')
ax_r.axvline(Lp,  color='#ff4433', lw=0.8, ls='--', alpha=0.7)
ax_r.text(Lp*1.03, 0.2, 'Lp', color='#ff6655', fontsize=7)
ln_rdf, = ax_r.plot([], [], color='#44ffcc', lw=1.5)
ln_rdf2,= ax_r.plot([], [], color='#224433', lw=0.6, alpha=0.5)

fig.text(0.5, 0.005,
    '⬡ Vortex Lagrangian physics  ·  adaptive scipy RK45  ·  spherical container  '
    '·  fully vectorised NumPy broadcasting',
    ha='center', color='#223355', fontsize=7.5)

# ─────────────────────────────────────────────────────────────────────
#  INTEGRATOR  (Velocity-Verlet + adaptive)
# ─────────────────────────────────────────────────────────────────────
acc, pot = compute_forces_and_energy(pos, vel, mass)

frame_count = [0]
step_count  = [0]
STEPS_PER_FRAME = 3   # integrate several steps per frame

def step_verlet():
    """One Velocity-Verlet step."""
    global pos, vel, acc, pot
    pos_new = pos + vel * DT + 0.5 * acc * DT**2
    pos_new, vel_tmp = apply_spherical_boundary(pos_new, vel)
    acc_new, pot_new = compute_forces_and_energy(pos_new, vel_tmp, mass)
    vel_new = vel_tmp + 0.5 * (acc + acc_new) * DT
    pos, vel, acc, pot = pos_new, vel_new, acc_new, pot_new


# ─────────────────────────────────────────────────────────────────────
#  ANIMATION FUNCTION
# ─────────────────────────────────────────────────────────────────────
def animate(frame):
    global trail_head, rdf_history

    # Integrate several steps
    for _ in range(STEPS_PER_FRAME):
        step_verlet()
        step_count[0] += 1

    frame_count[0] += 1

    # ── Update trail buffer ──────────────────────
    trail_pos[trail_head] = pos.copy()
    trail_head = (trail_head + 1) % TRAIL_LEN

    # ── 3D scatter (positions + energy colour) ──────
    scatter._offsets3d = (pos[:, 0], pos[:, 1], pos[:, 2])
    scatter.set_array(pot)

    # ── Particle trails ──────────────────────
    # Rearrange circular buffer → chronological order
    idx_ord = np.arange(trail_head, trail_head + TRAIL_LEN) % TRAIL_LEN
    trail_sorted = trail_pos[idx_ord]   # (TRAIL_LEN, N, 3)

    for i, ln in enumerate(trail_lines):
        tdata = trail_sorted[:, i, :]     # (TRAIL_LEN, 3)
        valid = ~np.isnan(tdata[:, 0])
        if valid.any():
            ln.set_data_3d(tdata[valid, 0],
                           tdata[valid, 1],
                           tdata[valid, 2])

    # ── Camera rotation ────────────────────────────
    ax3d.view_init(elev=18 + 10*np.sin(frame * 0.008),
                   azim=frame * 0.25)

    # ── Energy ──────────────────────────────────
    KE = 0.5 * np.sum(mass * np.sum(vel**2, axis=1))
    PE = np.sum(pot)
    E  = KE + PE

    step_hist.append(step_count[0])
    e_kin_hist.append(KE)
    e_pot_hist.append(PE)
    e_tot_hist.append(E)

    # Plot only last 400 points to keep it fast
    sl = slice(-400, None)
    ln_kin.set_data(step_hist[sl], e_kin_hist[sl])
    ln_pot.set_data(step_hist[sl], e_pot_hist[sl])
    ln_tot.set_data(step_hist[sl], e_tot_hist[sl])

    if len(step_hist) > 2:
        ax_e.set_xlim(step_hist[max(0,len(step_hist)-400)], step_hist[-1])
        evals = e_kin_hist + e_pot_hist + e_tot_hist
        ax_e.set_ylim(min(evals[-400*3:])*1.05,
                      max(evals[-400*3:])*1.1 + 0.1)

    # ── RDF (every 8 frames) ─────────────────────
    if frame % 8 == 0:
        r_mid, g_r = compute_rdf(pos)
        rdf_history.append(g_r)
        # Average over last 10 frames
        g_avg = np.mean(rdf_history[-10:], axis=0)
        ln_rdf.set_data(r_mid, g_avg)
        ln_rdf2.set_data(r_mid, g_r)
        ax_r.set_xlim(0, RDF_RMAX)
        ax_r.set_ylim(0, min(max(g_avg)*1.25 + 0.5, 12))

    # ── Info text ────────────────────────────────
    v_mag = np.linalg.norm(vel, axis=1)
    r_mag = np.linalg.norm(pos, axis=1)
    info_txt.set_text(f't = {step_count[0]*DT:.2f}')
    stat_txt.set_text(
        f'step   = {step_count[0]}\n'
        f'E tot  = {E:.3f}\n'
        f'T kin  = {KE:.3f}\n'
        f'V pot  = {PE:.3f}\n'
        f'v̄     = {v_mag.mean():.3f}\n'
        f'r̄     = {r_mag.mean():.3f}\n'
        f'r min  = {r_mag.min():.3f}'
    )

    return (scatter, ln_kin, ln_pot, ln_tot, ln_rdf,
            info_txt, stat_txt, *trail_lines)


# ─────────────────────────────────────────────────────────────────────
#  RUN ANIMATION
# ─────────────────────────────────────────────────────────────────────
print("═" * 65)
print("  VORTEX N-BODY SIMULATION")
print(f"  N={N}  G={G}  c={c}  Lp={Lp}  Λ={LAM}  dt={DT}  BOX={BOX}")
print("═" * 65)
print("  Press Ctrl+C to stop.")
print("  Set SAVE_GIF=True to export GIF (requires Pillow).")
print("═" * 65)

ani = FuncAnimation(
    fig, animate, frames=4000,
    interval=INTERVAL, blit=False, cache_frame_data=False
)

if SAVE_GIF:
    from matplotlib.animation import PillowWriter
    print("💾 Saving vortex_nbody.gif ...")
    ani.save('vortex_nbody.gif',
             writer=PillowWriter(fps=28), dpi=90)
    print("✓ Saved!")
else:
    plt.show()
"""
VORTEX THEORY — Full 3D Animation
═══════════════════════════════════════════════════════
Lagrangian:
  L = ½m(ṙ²+r²θ̇²) + GMm/r + (GMm/c²r)(ṙ²+r²θ̇²)
      − mc²[ (Lp²/r²)e^{−r/Lp} − (Λ/6)r² ]

Equations of motion derived via Euler-Lagrange,
integrated with Runge-Kutta 4/5 (scipy solve_ivp).

5 animated panels: 3D orbit, r(t), energy, x‑y orbit,
                   Planck Vortex + Λ potentials

Install: pip install numpy matplotlib scipy
Run: python vortex3d_full.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D       # noqa: F401
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.integrate import solve_ivp

# ══════════════════════════════════════════════════
#  PARAMETERS  (dimensionless units: GM = c = 1)
# ══════════════════════════════════════════════════
GM       = 1.0
c        = 1.0
Lp       = 0.08    # Planck length (enlarged for visibility)
Lam      = 3e-5    # Cosmological constant Λ

r0       = 8.0     # Initial distance [GM/c²]
rdot0    = 0.02    # Initial radial speed
J        = 4.2     # Angular momentum (conserved)
t_end    = 500.0   # Simulation duration

TRAIL    = 140     # Orbit trail length (points)
INTERVAL = 28      # ms per animation frame
SAVE_GIF = False   # True → save vortex3d.gif (requires Pillow)

# ══════════════════════════════════════════════════
#  EQUATIONS OF MOTION from Euler-Lagrange
#
#  Coordinates: q = (r, θ)
#  Conjugate momentum for θ is conserved:
#    p_θ = mr²θ̇·(1 + 2GM/c²r) = J  (constant)
#  → θ̇ = J / (r²·α)   with α = 1 + 2GM/(c²r)
#
#  Radial equation from EL:
#    r̈·α = rθ̇² − GM/r² + GM(ṙ²+θ̇²·r²−2r²θ̇²)/(c²r²)
#           + c²Lp²e^{−r/Lp}(2/r³ + 1/(Lp·r²))
#           + c²(Λ/3)r
# ══════════════════════════════════════════════════
def eom(t, state):
    r, rdot = state
    r = max(r, 1e-7)                          # floor to avoid divergence

    alpha  = 1.0 + 2.0*GM / (c**2 * r)       # PN factor
    thdot  = J / (r**2 * alpha)               # θ̇ from conservation of J

    # ∂L/∂r  (divided by m) — four physical terms
    T_cent  =  r * thdot**2                           # centrifugal
    T_newt  = -GM / r**2                              # Newton
    T_pn    =  GM * (rdot**2 + thdot**2*c**2) \
               / (c**2 * r**2)                       # Post-Newton
    exp_v   = np.exp(-min(r/Lp, 700.0))
    T_vort  =  c**2 * Lp**2 * exp_v \
               * (2.0/r**3 + 1.0/(Lp*r**2))      # Planck Vortex
    T_cosm  =  c**2 * (Lam/3.0) * r                # Cosmology Λ

    rddot = (T_cent + T_newt + T_pn + T_vort + T_cosm) / alpha
    return [rdot, rddot]

# ══════════════════════════════════════════════════
#  NUMERICAL INTEGRATION  (Runge-Kutta 4/5)
# ══════════════════════════════════════════════════
print("⏳ Integrating equations of motion (RK45)...")
sol = solve_ivp(
    eom, [0, t_end], [r0, rdot0],
    method='RK45', max_step=0.1,
    rtol=1e-9, atol=1e-11, dense_output=True
)

t_arr    = sol.t
r_arr    = sol.y[0]
rdot_arr = sol.y[1]

# Numerical integration of θ(t) from θ̇ = J/(r²α)
alpha_arr = 1.0 + 2.0*GM / (c**2 * r_arr)
thdot_arr = J / (r_arr**2 * alpha_arr)
theta_arr = np.cumsum(thdot_arr * np.gradient(t_arr))

# Cartesian 3D coordinates
x_arr = r_arr * np.cos(theta_arr)
y_arr = r_arr * np.sin(theta_arr)
# z — "Vortex sin(x)" oscillation: quantum component perpendicular to orbital plane
z_arr = 0.45 * np.sin(3.0 * theta_arr) * np.exp(-r_arr / 6.0)

# ── Energy decomposition per Lagrangian term ──────
v2      = rdot_arr**2 + (r_arr * thdot_arr)**2
KE      =  0.5 * v2
V_newt  = -GM / r_arr
V_pn    =  (GM / (c**2 * r_arr)) * v2
exp_v2  = np.exp(-np.clip(r_arr/Lp, 0, 700))
V_vort  = -c**2 * (Lp**2 / r_arr**2) * exp_v2
V_cosm  =  c**2 * (Lam/6.0) * r_arr**2
E_tot   = KE + V_newt + V_pn + V_vort + V_cosm

SKIP = max(1, len(t_arr) // 1400)
print(f"✓ {len(t_arr)} points | SKIP={SKIP} | ~{len(t_arr)//SKIP} frames")

# ══════════════════════════════════════════════════
#  SETUP FIGURE  (dark theme, 5 panels)
# ══════════════════════════════════════════════════
plt.style.use('dark_background')
fig = plt.figure(figsize=(18, 10))
fig.patch.set_facecolor('#05050f')
fig.suptitle(
    'VORTEX  ·  L = ½mv² + GMm/r + (GMm/c²r)v² − mc²[(Lp²/r²)e^{−r/Lp} − (Λ/6)r²]',
    color='#8899ff', fontsize=11, fontweight='bold', y=0.995
)
plt.subplots_adjust(left=0.05, right=0.97,
                    bottom=0.07, top=0.95,
                    hspace=0.52, wspace=0.38)

gs   = gridspec.GridSpec(3, 4, figure=fig)
ax3d = fig.add_subplot(gs[:2, :2], projection='3d')
ax_r = fig.add_subplot(gs[0, 2:])
ax_e = fig.add_subplot(gs[1, 2:])
ax_p = fig.add_subplot(gs[2, :2])
ax_v = fig.add_subplot(gs[2, 2:])

BG = '#080818'
for ax in [ax_r, ax_e, ax_p, ax_v]:
    ax.set_facecolor(BG)
    for sp in ax.spines.values():
        sp.set_edgecolor('#1e2244')
    ax.tick_params(colors='#556688', labelsize=7)

# ── 3D panel ────────────────────────────────────
lim  = max(np.abs(x_arr).max(), np.abs(y_arr).max()) * 1.15
zlim = max(np.abs(z_arr).max() * 2.5, 0.1)
ax3d.set_facecolor('#030310')
ax3d.set_xlim(-lim, lim); ax3d.set_ylim(-lim, lim)
ax3d.set_zlim(-zlim, zlim)
ax3d.set_xlabel('x  [GM/c²]', color='#6677aa', fontsize=8, labelpad=3)
ax3d.set_ylabel('y  [GM/c²]', color='#6677aa', fontsize=8, labelpad=3)
ax3d.set_zlabel('z  [oscillation]', color='#6677aa', fontsize=8, labelpad=3)
ax3d.set_title('3D Vortex Orbit  (x, y, z, t)',
               color='#aabbff', fontsize=10, pad=3)
ax3d.tick_params(colors='#334466', labelsize=6)
ax3d.grid(color='#111133', linewidth=0.4)

# Black hole at centre (small black sphere)
ug, vg = np.mgrid[0:2*np.pi:24j, 0:np.pi:14j]
rs = 2.0 * GM / c**2
rb = rs * 0.55
ax3d.plot_surface(
    rb*np.cos(ug)*np.sin(vg), rb*np.sin(ug)*np.sin(vg),
    rb*np.cos(vg)*0.12,
    color='#0a0a22', alpha=0.9, zorder=1, linewidth=0
)
# Thin background trail
ax3d.plot(x_arr[::SKIP], y_arr[::SKIP], z_arr[::SKIP],
          color='#151535', lw=0.4, alpha=0.4)

trail3d, = ax3d.plot([], [], [], '#4466ff', lw=1.5, alpha=0.95)
point3d, = ax3d.plot([], [], [], 'o', color='#ffdd55', ms=6, zorder=10)
ttxt = ax3d.text2D(0.02, 0.96, '', transform=ax3d.transAxes,
                    color='white', fontsize=8.5, va='top',
                    fontfamily='monospace')
itxt = ax3d.text2D(0.02, 0.82, '', transform=ax3d.transAxes,
                    color='#88aaff', fontsize=7.8, va='top',
                    linespacing=1.6, fontfamily='monospace')

# ── Panel r(t) ──────────────────────────────────
ax_r.plot(t_arr[::SKIP], r_arr[::SKIP],
          color='#1a2855', lw=0.8, alpha=0.5)
ax_r.axhline(rs, color='#ff3322', ls=':', lw=0.9, alpha=0.7)
ax_r.set_xlim(0, t_end)
ax_r.set_ylim(r_arr.min()*0.85, r_arr.max()*1.12)
ax_r.set_ylabel('r  [GM/c²]', color='#7788bb', fontsize=9)
ax_r.set_title('r(t) — radial distance', color='#aabbff', fontsize=9)
ax_r.text(t_end*0.01, rs*1.04, 'r_Schwarzschild',
          color='#ff5544', fontsize=6.5)
line_r,  = ax_r.plot([], [], '#4477ff', lw=1.3)
dot_r,   = ax_r.plot([], [], 'o', color='#ffdd55', ms=4)

# ── Energy panel (5 terms) ───────────────────────
sk = SKIP
ax_e.plot(t_arr[::sk], E_tot[::sk],  '#ffffff', lw=1.0, alpha=0.6, label='E total')
ax_e.plot(t_arr[::sk], KE[::sk],     '#ffaa33', lw=0.9, alpha=0.7, label='T kinetic')
ax_e.plot(t_arr[::sk], V_newt[::sk], '#ff5544', lw=0.8, alpha=0.6, label='V Newton')
ax_e.plot(t_arr[::sk], V_pn[::sk],   '#44bbff', lw=0.8, alpha=0.6, label='V post-Newton')
ax_e.plot(t_arr[::sk], V_vort[::sk], '#44ff88', lw=0.8, alpha=0.6, label='V Vortex Lp')
ax_e.plot(t_arr[::sk], V_cosm[::sk], '#ffcc44', lw=0.8, alpha=0.6, label='V Cosmology Λ')
ax_e.set_xlim(0, t_end)
ax_e.set_ylabel('Specific energy', color='#7788bb', fontsize=9)
ax_e.set_title('Energy decomposition per Lagrangian term',
               color='#aabbff', fontsize=9)
ax_e.legend(fontsize=6.5, labelcolor='white', ncol=3,
            facecolor='#0a0a22', edgecolor='none', loc='upper right')
dot_e, = ax_e.plot([], [], 'o', color='#ffdd55', ms=5, zorder=10)

# ── x‑y orbit panel (precession) ───────────────────
ax_p.plot(x_arr[::sk], y_arr[::sk],
          color='#1a2460', lw=0.6, alpha=0.5)
ax_p.add_patch(plt.Circle((0,0), rb, color='#220011',
               fill=True, alpha=0.5))
ax_p.set_xlim(-lim, lim); ax_p.set_ylim(-lim, lim)
ax_p.set_aspect('equal')
ax_p.set_xlabel('x  [GM/c²]', color='#7788bb', fontsize=9)
ax_p.set_ylabel('y  [GM/c²]', color='#7788bb', fontsize=9)
ax_p.set_title('x‑y projection  (perihelion precession)',
               color='#aabbff', fontsize=9)
trail_p, = ax_p.plot([], [], '#3355cc', lw=1.1, alpha=0.9)
dot_p,   = ax_p.plot([], [], 'o', color='#ffdd55', ms=5, zorder=10)

# ── Planck Vortex potential panel ────────────────
r_plt = np.linspace(0.01*Lp, 18.0*Lp, 900)
Vv_plt = -(Lp**2/r_plt**2) * np.exp(-r_plt/Lp)
Vc_plt = (Lam/6.0) * r_plt**2
ax_v.plot(r_plt/Lp, Vv_plt, '#44ff88', lw=1.5, label='V Vortex')
ax_v.plot(r_plt/Lp, Vc_plt, '#ffaa44', lw=1.5, label='V Cosmology Λ')
ax_v.plot(r_plt/Lp, Vv_plt+Vc_plt,
          '#ffffff', lw=1.2, ls='--', label='Total')
ax_v.axvline(1.0, color='#ff4433', ls=':', lw=0.9)
ax_v.text(1.05, Vv_plt.min()*0.5, 'r = Lp',
          color='#ff6655', fontsize=7)
ax_v.set_xlabel('r / Lp', color='#7788bb', fontsize=9)
ax_v.set_ylabel('V(r)', color='#7788bb', fontsize=9)
ax_v.set_title('Planck Vortex + Λ potential',
               color='#aabbff', fontsize=9)
ax_v.legend(fontsize=7, labelcolor='white',
            facecolor='#0a0a22', edgecolor='none')
dot_vp, = ax_v.plot([], [], 'o', color='#ffdd55', ms=5)

fig.text(0.5, 0.01,
    '⬡ All panels computed from the same Lagrangian · Euler-Lagrange + scipy RK45',
    ha='center', color='#334466', fontsize=8)

# ══════════════════════════════════════════════════
#  ANIMATION FUNCTION
# ══════════════════════════════════════════════════
def animate(frame):
    i   = min(frame * SKIP, len(t_arr) - 1)
    i0  = max(0, i - TRAIL * SKIP)
    sl  = slice(i0, i+1, SKIP)    # trail
    sl2 = slice(0,  i+1)           # full history

    # 3D orbit + automatic camera rotation
    trail3d.set_data_3d(x_arr[sl], y_arr[sl], z_arr[sl])
    point3d.set_data_3d([x_arr[i]], [y_arr[i]], [z_arr[i]])
    ax3d.view_init(elev=22 + 8*np.sin(frame*0.006),
                   azim=frame * 0.22)

    # r(t)
    line_r.set_data(t_arr[sl2], r_arr[sl2])
    dot_r.set_data([t_arr[i]], [r_arr[i]])

    # Energy cursor
    dot_e.set_data([t_arr[i]], [E_tot[i]])

    # x‑y orbit trail
    trail_p.set_data(x_arr[sl], y_arr[sl])
    dot_p.set_data([x_arr[i]], [y_arr[i]])

    # Potential dot — current r position
    r_now = r_arr[i]
    if r_now < r_plt[-1]:
        Vv_now = -(Lp**2/r_now**2)*np.exp(-min(r_now/Lp, 700))
        dot_vp.set_data([r_now/Lp], [Vv_now])

    # 3D info text
    ttxt.set_text(f't = {t_arr[i]:.1f}')
    itxt.set_text(
        f'r    = {r_arr[i]:.3f} GM/c²\n'
        f'ṙ    = {rdot_arr[i]:+.4f}\n'
        f'θ̇   = {thdot_arr[i]:.4f}\n'
        f'|v|  = {np.sqrt(v2[i]):.4f} c\n'
        f'E    = {E_tot[i]:.5f}\n'
        f'V_vx = {V_vort[i]:.3e}'
    )
    return (trail3d, point3d, line_r, dot_r,
            dot_e, trail_p, dot_p, dot_vp)

n_frames = len(t_arr) // SKIP
ani = FuncAnimation(fig, animate, frames=n_frames,
                    interval=INTERVAL, blit=False)

if SAVE_GIF:
    print("💾 Saving vortex3d.gif ...")
    ani.save('vortex3d.gif', writer=PillowWriter(fps=30), dpi=100)
    print("✓ Saved!")

plt.show()
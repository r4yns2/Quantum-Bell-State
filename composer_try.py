import math, numpy as np
import matplotlib.pyplot as plt

# --- theory for X⊗X on |Φ_φ> ---
def theory_probs_xx(phi):
    c = math.cos(phi)
    return {
        "00": (1+c)/4, 
        "11": (1+c)/4, 
        "01": (1-c)/4, 
        "10": (1-c)/4
        }

def counts_to_probs(counts):
    shots = sum(counts.values()) or 1
    return {k: counts.get(k, 0)/shots for k in ["00","01","10","11"]}

def stderr_binom(p_hat, shots):
    # 1-sigma binomial standard error (good visual error bar)
    return math.sqrt(max(p_hat * (1 - p_hat), 0.0) / max(shots, 1))

def reverse_keys(d):  # flip bitstring order if needed
    return {k[::-1]: v for k, v in d.items()}

# === EDIT THESE ===
phi_points = [0.0, math.pi/2, math.pi]

# Paste Composer counts (X-basis runs: H on both before measure)
composer_counts = [
    {"00": 504, "11": 495},                               # φ=0
    {"00": 233, "01": 248, "10": 271, "11": 247},         # φ=π/2
    {"01": 495, "10": 504},                               # φ=π
]
BITSTRINGS_REVERSED = False
# ==================

assert len(phi_points) == len(composer_counts), "phi_points and composer_counts length mismatch"

# ----- plotting -----
fig, ax = plt.subplots(figsize=(8, 5))

# 1) Theory curves (thin lines)
phis = np.linspace(0, 2*math.pi, 500)
for outcome in ["00", "01", "10", "11"]:
    ax.plot(phis,
            [theory_probs_xx(p)[outcome] for p in phis],
            label=f"Theory {outcome}",
            linewidth=1.5, alpha=0.9)

# 2) Composer points with error bars + small jitter to separate pairs
markers = {"00":"o", "11":"o", "01":"s", "10":"s"}
# small horizontal jitter so (00,11) and (01,10) don't sit on top of each other
jitter = {"00": -0.035, "11": +0.035, "01": -0.035, "10": +0.035}

for outcome in ["00", "01", "10", "11"]:
    xs, ys, yerrs = [], [], []
    for x, c in zip(phi_points, composer_counts):
        c_use = reverse_keys(c) if BITSTRINGS_REVERSED else c
        p = counts_to_probs(c_use).get(outcome, 0.0)
        n = sum(c_use.values())
        xs.append(x + jitter[outcome])
        ys.append(p)
        yerrs.append(stderr_binom(p, n))
    ax.errorbar(xs, ys, yerr=yerrs,
                fmt=markers[outcome],
                mfc="white", mec="black", mew=1,
                ms=7, elinewidth=1, capsize=3,
                linestyle="none", label=f"Composer {outcome}")

# 3) Cosmetics
ax.set_xlabel(r"$\varphi$ (radians)")
ax.set_ylabel("Probability")
ax.set_title("Bell-like state — X⊗X probabilities vs. phase\n(lines: theory, markers: IBM Composer)")

# π ticks
pi = math.pi
ax.set_xticks([0, 0.5*pi, pi, 1.5*pi, 2*pi],
              [r"$0$", r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$"])

ax.set_ylim(-0.02, 0.62)
ax.grid(True, alpha=0.25)
ax.legend(ncol=2, frameon=False)
fig.tight_layout()
fig.savefig("phi_overlay_test.png", dpi=300)
print("Saved: phi_overlay_test.png")

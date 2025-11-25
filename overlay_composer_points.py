import math, numpy as np
import matplotlib.pyplot as plt
# --- theory for X⊗X on |Φ_φ> ---
def theory_probs_xx(phi):
    c = math.cos(phi)
    return {
        "00": (1+c)/4,
        "11": (1+c)/4,
        "01": (1-c)/4,
        "10": (1-c)/4,
    }

def counts_to_probs(counts):
    shots = sum(counts.values())
    if shots == 0:
        return {"00":0,"01":0,"10":0,"11":0}
    return {k: counts.get(k, 0)/shots for k in ["00","01","10","11"]}

def reverse_keys(d):  # use if your bit order is flipped
    return {k[::-1]: v for k, v in d.items()}

# === EDIT THESE ===
# φ values (radians) you actually ran in Composer, in the same order as the dicts below
phi_points = [0.0, math.pi/2, math.pi]

# Paste counts dicts copied from Composer (X-basis runs: H on both before measure).
# Example placeholders below—REPLACE with your Composer counts.
composer_counts = [
    {"00": 504, "11": 495},                    # φ=0
    {"00": 233, "01": 248, "10": 271, "11": 247},  # φ=π/2
    {"01": 495, "10": 504},                    # φ=π
]
# If you discover bitstrings are reversed, set this True:
BITSTRINGS_REVERSED = False
# ==================

assert len(phi_points) == len(composer_counts), "phi_points and composer_counts length mismatch"

# 1) theory curves
phis = np.linspace(0, 2*math.pi, 400)
for outcome in ["00","01","10","11"]:
    plt.plot(phis, [theory_probs_xx(p)[outcome] for p in phis], label=f"theory {outcome}")

# 2) Composer points
markers = {"00":"o", "01":"s", "10":"^", "11":"D"}
for outcome in ["00","01","10","11"]:
    y = []
    for c in composer_counts:
        c_use = reverse_keys(c) if BITSTRINGS_REVERSED else c
        y.append(counts_to_probs(c_use).get(outcome, 0.0))
    plt.scatter(phi_points, y, marker=markers[outcome], edgecolor="k", facecolors="none",
                label=f"Composer {outcome}")

plt.xlabel("φ (radians)")
plt.ylabel("Probability")
plt.title("Bell-like state: X⊗X probabilities vs φ\n(lines = theory, open markers = IBM Composer)")
plt.legend(ncol=2)
plt.tight_layout()
plt.savefig("phi_overlay.png", dpi=300)
print("Saved: phi_overlay.png")
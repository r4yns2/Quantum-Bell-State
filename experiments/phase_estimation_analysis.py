import os, json, math, csv
import numpy as np

RAW_DIR = "data/raw/x_basis"
OUT_CSV = "data/processed/phase_estimates/estimates.csv"
os.makedirs("data/processed/phase_estimates", exist_ok=True)

def counts_to_probs(counts):
    total = sum(counts.values())
    return {k: counts.get(k, 0) / total for k in ["00","01","10","11"]}


# ------------ Phase Estimators (NO CLAMPING) ------------
def safe_phase_estimator(arg):
    """
    Returns:
        - phi_hat if valid
        - None if arg is outside [-1, 1]
    """
    if arg < -1 or arg > 1:
        return None     # invalid — too noisy or unphysical
    return math.acos(arg)


def estimate_from_P00(p00):
    arg = 4*p00 - 1
    return safe_phase_estimator(arg), arg


def estimate_from_P11(p11):
    arg = 4*p11 - 1
    return safe_phase_estimator(arg), arg


def estimate_from_Peven(peven):
    arg = 2*peven - 1
    return safe_phase_estimator(arg), arg


def estimate_from_Podd(podd):
    arg = 1 - 2*podd
    return safe_phase_estimator(arg), arg


# ------------ PROCESS ALL FILES ------------
rows = []

for fname in sorted(os.listdir(RAW_DIR)):
    if not fname.endswith(".json"):
        continue

    with open(os.path.join(RAW_DIR, fname)) as f:
        data = json.load(f)

    phi_true = float(data["phi"])
    counts = data["counts"]
    probs = counts_to_probs(counts)

    p00  = probs["00"]
    p11  = probs["11"]
    peven = p00 + p11
    podd  = probs["01"] + probs["10"]

    # --- Compute raw arguments + estimators ---
    phi00,   arg00   = estimate_from_P00(p00)
    phi11,   arg11   = estimate_from_P11(p11)
    phieven, argeven = estimate_from_Peven(peven)
    phiodd,  argodd  = estimate_from_Podd(podd)

    rows.append([
        phi_true,
        p00, p11, peven, podd,
        arg00, phi00,
        arg11, phi11,
        argeven, phieven,
        argodd, phiodd
    ])


# ------------ SAVE CSV ------------
with open(OUT_CSV, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "phi_true",
        "P00", "P11", "Peven", "Podd",
        "arg00_raw", "phi_hat_00",
        "arg11_raw", "phi_hat_11",
        "argeven_raw", "phi_hat_even",
        "argodd_raw", "phi_hat_odd"
    ])
    writer.writerows(rows)

print("Saved phase estimates to:", OUT_CSV)

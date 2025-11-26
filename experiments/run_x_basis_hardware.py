# experiments/run_x_basis_hardware.py

import os
import json
import numpy as np

from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.visualization import plot_histogram

from src.circuits.bell_phase_circuit import build_circuit

# --- output paths ---
RAW_DIR = "data/hardware/x_basis"
FIG_DIR = "results/figures/x_histograms_hardware"

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)

shots = 1000
phi_values = [0, np.pi/2, np.pi]

# --- connect to IBM Quantum ---
# This assumes you already ran: qiskit-ibm-runtime init
service = QiskitRuntimeService(channel="ibm_quantum")

# Pick a backend: replace with a device you have access to,
# e.g. "ibm_oslo", "ibm_perth", "ibm_brisbane", etc.
backend_name = "ibm_oslo"
backend = service.backend(backend_name)

print(f"Using backend: {backend_name}")

for phi in phi_values:
    print(f"Running circuit for phi = {phi:.3f} ...")

    qc = build_circuit(phi, with_basis_rotation=True)

    # Submit job to hardware
    job = backend.run(qc, shots=shots)
    result = job.result()
    counts = result.get_counts()

    # Save raw counts as JSON
    json_path = os.path.join(RAW_DIR, f"phi_{phi:.3f}.json")
    with open(json_path, "w") as f:
        json.dump(
            {
                "phi": float(phi),
                "backend": backend_name,
                "shots": shots,
                "counts": counts,
            },
            f,
            indent=4,
        )
    print("Saved counts to:", json_path)

    # Save histogram figure
    fig = plot_histogram(counts)
    fig_path = os.path.join(FIG_DIR, f"hist_phi_{phi:.3f}.png")
    fig.savefig(fig_path)
    print("Saved histogram to:", fig_path)

print("Done.")

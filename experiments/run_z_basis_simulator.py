import json, os
import numpy as np
from qiskit_aer import Aer
from matplotlib import pyplot as plt
from qiskit.visualization import plot_histogram
from src.circuits.bell_phase_circuit import build_circuit

OUTPUT_DIR = "data/raw/z_basis"
FIG_DIR = "results/figures/z_histograms"
CIRCUIT_DIR = "results/figures/"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)

backend = Aer.get_backend("qasm_simulator")
shots = 1000

phi_values = [0, np.pi/2, np.pi]

for phi in phi_values:
    qc = build_circuit(phi, with_basis_rotation=False)
    job = backend.run(qc, shots=shots)
    result = job.result()
    counts = result.get_counts()

    # Save JSON
    filename = os.path.join(OUTPUT_DIR, f"phi_{phi:.3f}.json")
    with open(filename, "w") as f:
        json.dump({"phi": float(phi), "counts": counts}, f, indent=4)

    # Save Histogram
    fig = plot_histogram(counts)
    fig_path = os.path.join(FIG_DIR, f"hist_phi_{phi:.3f}.png")
    fig.savefig(fig_path)
    print("Saved:", fig_path)

    fig = qc.draw(output="mpl") # diagram of the circuit
    fig.savefig(CIRCUIT_DIR+"bell_circuit_y.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("Saved circuit diagram to bell_circuit.png")

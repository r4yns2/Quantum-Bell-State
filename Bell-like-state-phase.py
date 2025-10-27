import math
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from matplotlib import pyplot as plt


def bell_like_state(phi, measure_in_x_basis=False):
    """
    Prepare (|00> + e^{i phi}|11>)/sqrt(2).
    If measure_in_x_basis=True, rotate both qubits into X-basis before measuring.
    """
    qc = QuantumCircuit(2, 2)

    # 1. Create Bell pair
    qc.h(0)
    qc.cx(0, 1)

    # 2. Add relative phase e^{i phi} to the |11> component
    qc.p(phi, 1)

    # 3. Optional: rotate into X basis (Hadamard before measuring is X-basis measurement)
    if measure_in_x_basis:
        qc.h(0)
        qc.h(1)

    # 4. Measure
    qc.measure([0, 1], [0, 1])

    return qc


def run_and_analyze(qc, label, save_prefix):
    """
    - Runs the given circuit on AerSimulator
    - Prints raw counts and probabilities
    - Saves histogram and circuit diagram as PNGs
    """
    print(f"\n--- Running: {label} ---")

    sim = AerSimulator()
    print("Transpiling circuit...")
    qc_t = transpile(qc, sim)

    print("Simulating circuit...")
    result = sim.run(qc_t, shots=1000).result()

    print("Getting counts...")
    counts = result.get_counts()

    print(f"Counts for {label}: {counts}")

    total = sum(counts.values())
    probs = {state: c / total for state, c in counts.items()}

    print("Probabilities:")
    for state, p in probs.items():
        print(f"  {state}: {p:.3f}")

    # Save histogram
    print("Saving histogram image...")
    hist_fig = plot_histogram(counts)
    hist_path = f"{save_prefix}_hist.png"
    hist_fig.savefig(hist_path, dpi=300, bbox_inches="tight")
    plt.close(hist_fig)
    print(f"Saved histogram to {hist_path}")

    # Save circuit diagram
    print("Saving circuit diagram image...")
    fig = qc.draw(output="mpl")
    circ_path = f"{save_prefix}_circuit.png"
    fig.savefig(circ_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved circuit diagram to {circ_path}")

    print(f"--- Done: {label} ---\n")


if __name__ == "__main__":
    # Pick the phase φ (radians). Try 0, math.pi/2, math.pi, etc.
    phi = math.pi # 90 degrees

    # 1. Z-basis measurement (direct measurement)
    qc_z = bell_like_state(phi, measure_in_x_basis=False)
    run_and_analyze(
        qc_z,
        label=f"Z-basis measurement, phi={phi:.2f} rad",
        save_prefix=f"phi_{phi:.2f}_Z"
    )

    # 2. X-basis measurement (Hadamards before measure)
    qc_x = bell_like_state(phi, measure_in_x_basis=True)
    run_and_analyze(
        qc_x,
        label=f"X-basis measurement, phi={phi:.2f} rad",
        save_prefix=f"phi_{phi:.2f}_X"
    )
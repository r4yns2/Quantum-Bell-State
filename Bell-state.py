# Bell-state.py

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from matplotlib import pyplot as plt

# 1. Build a 2-qubit Bell state circuit
# We'll create |Φ+> = (|00> + |11>)/√2

qc = QuantumCircuit(2, 2)  # 2 qubits, 2 classical bits

# Step 1: Put qubit 0 into superposition
qc.h(0)        # Hadamard on qubit 0

# Step 2: Entangle qubit 1 with qubit 0
qc.cx(0, 1)    # CNOT: control=0, target=1

# Step 3: Measure both qubits into classical bits
qc.measure([0, 1], [0, 1])

fig = qc.draw(output="mpl") # diagram of the circuit
fig.savefig("bell_circuit.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved circuit diagram to bell_circuit.png")

# 2. Run the circuit on a simulator
sim = AerSimulator()               # get simulator backend
qc_t = transpile(qc, sim)          # adapt circuit to the backend
job_result = sim.run(qc_t, shots=1000).result()  # run 1000 shots
counts = job_result.get_counts()

print("\nMeasurement counts (number of times we saw each bitstring):")
print(counts)

# 3. Convert counts to probabilities
total_shots = sum(counts.values())
probs = {state: count / total_shots for state, count in counts.items()}

print("\nEstimated probabilities:")
for state, p in probs.items():
    print(f"{state}: {p:.3f}")

# Optional: show a histogram pop-up if you're running in an environment
# that can display windows (like VSCode interactive / Jupyter)
hist_fig = plot_histogram(counts)
hist_fig.savefig("bell_histogram.png", dpi=300, bbox_inches="tight")
plt.close(hist_fig)
print("Saved measurement histogram to bell_histogram.png")

# Quantum Bell State with Phase Encoding

## What it does

This project creates and analyzes Bell states with phase encoding using Qiskit. It:

- Constructs a 2-qubit Bell state (|Φ⟩ = (|00⟩ + |11⟩)/√2)
- Applies phase encoding with variable angle φ
- Measures in both Z-basis and X-basis (X⊗X)
- Compares experimental results against theoretical predictions
- Runs on both Qiskit simulator and IBM Quantum hardware
- Estimates phase from measurement probabilities

## How to run

### Installation

```bash
pip install -r requirements.txt
```

### Run experiments

**Simulator (X-basis):**
```bash
python -m experiments/run_x_basis_simulator
```

**Simulator (Z-basis):**
```bash
python -m experiments/run_z_basis_simulator
```

**Hardware (requires IBM Quantum account):**
```bash
python -m experiments/run_x_basis_hardware
```

**Phase estimation analysis:**
```bash
python -m experiments/phase_estimation_analysis
```

**Plot theory vs experiment:**
```bash
python -m composer
```

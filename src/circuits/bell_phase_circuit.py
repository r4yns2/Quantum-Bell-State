from qiskit import QuantumCircuit

def prepare_bell_state(qc):
    qc.h(0)
    qc.cx(0, 1)

def apply_phase_encoding(qc, phi):
    qc.p(phi, 0)  # phase on qubit 0

def apply_basis_rotation(qc):
    qc.h(0)
    qc.h(1)

def build_circuit(phi, with_basis_rotation=False):
    """
    Returns a 2-qubit circuit that prepares a Bell state,
    applies a phase gate, and optionally rotates basis.
    """
    qc = QuantumCircuit(2, 2)

    prepare_bell_state(qc)
    apply_phase_encoding(qc, phi)

    if with_basis_rotation:
        apply_basis_rotation(qc)

    qc.measure([0, 1], [0, 1])
    return qc

"""
#############################################
#
# circuit_2.py
#
# example code for configurable circuit 2
# from https://arxiv.org/abs/1905.10876 fig 3.
#
#############################################
"""

from qiskit.circuit.library import TwoLocal
from qiskit import QuantumCircuit


def circuit_2(width=4, layer=1, verbose=False) -> QuantumCircuit:
    """Template circuit 2

    Args:
        width: number of qubits
        layer: number of repetitions
        verbose: True/False

    Return:
        The circuit generate
    """

    entangler_map = [(i, i - 1) for i in range(width - 1, 0, -1)]

    circuit = TwoLocal(
        num_qubits=width,
        rotation_blocks=["rx", "rz"],
        entanglement_blocks="cx",
        entanglement=entangler_map,
        reps=layer,
        skip_unentangled_qubits=False,
        skip_final_rotation_layer=True,
        parameter_prefix="θ",
        insert_barriers=True,
        initial_state=None,
        name="sim_circuit_2_%d_",
    )

    if verbose:
        print(entangler_map)
        print(circuit.decompose())

    return circuit

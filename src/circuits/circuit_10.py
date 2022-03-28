"""
#############################################
#
# circuit_10.py
#
# example code for configurable circuit 10
# from https://arxiv.org/abs/1905.10876 fig 3.
#
#############################################
"""

from qiskit.circuit.library import TwoLocal
from qiskit import QuantumCircuit


def circuit_10(width=4, layer=1, verbose=False) -> QuantumCircuit:
    """Template circuit 10

    Args:
        width: number of qubits
        layer: number of repetitions
        verbose: True/False

    Return:
        The circuit generate
    """
    nb_qubits = width
    repetitions = layer

    rotation_blocks = ["ry"]
    entanglement_blocks = "cz"
    entanglement = "circular"
    insert_barriers = True
    skip_final_rotation_layer = False

    circuit = TwoLocal(
        num_qubits=nb_qubits,
        rotation_blocks=rotation_blocks,
        entanglement_blocks=entanglement_blocks,
        entanglement=entanglement,
        reps=repetitions,
        insert_barriers=insert_barriers,
        skip_final_rotation_layer=skip_final_rotation_layer,
    )

    if verbose:
        print(circuit.decompose())

    return circuit

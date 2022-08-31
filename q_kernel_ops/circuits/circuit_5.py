"""
#############################################
#
# circuit_5.py
#
# example code for configurable circuit 5
# from https://arxiv.org/abs/1905.10876 fig 3.
#
#############################################
"""

from qiskit import QuantumCircuit
from .circuit_tpl import twolocal_tpl


def circuit_5(width=4, layer=1, verbose=False) -> QuantumCircuit:
    """Template circuit 5

    Args:
        width: number of qubits
        layer: number of repetitions
        verbose: True/False

    Return:
        The circuit generate
    """
    entangler_map = []
    for i in range(width):
        for target_qubit in range(width):
            if target_qubit != i:
                entangler_map.append((i, target_qubit))

    circuit = twolocal_tpl(
        nb_qubits=width,
        repetitions=layer,
        rotation_blocks=["rx", "rz"],
        entanglement_blocks="crz",
        entanglement=entangler_map,
        skip_final_rotation_layer=False,
        name="sim_circuit_5_%d_",
        verbose=verbose,
    )

    return circuit

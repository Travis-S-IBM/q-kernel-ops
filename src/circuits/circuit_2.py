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

from qiskit import QuantumCircuit
from .circuit_tpl import twolocal_tpl


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

    circuit = twolocal_tpl(
        nb_qubits=width,
        repetitions=layer,
        rotation_blocks=["rx", "rz"],
        entanglement_blocks="cx",
        entanglement=entangler_map,
        skip_final_rotation_layer=True,
        name="sim_circuit_2_%d_",
        verbose=verbose,
    )

    return circuit

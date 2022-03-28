"""
#############################################
#
# circuit_18.py
#
# example code for configurable circuit 18
# from https://arxiv.org/abs/1905.10876 fig 3.
#
#############################################
"""

from qiskit import QuantumCircuit
from .circuit_tpl import twolocal_tpl


def circuit_18(width=4, layer=1, verbose=False) -> QuantumCircuit:
    """Template circuit 18

    Args:
        width: number of qubits
        layer: number of repetitions
        verbose: True/False

    Return:
        The circuit generate
    """
    nb_qubits = width
    repetitions = layer

    rotation_blocks = ["rx", "ry"]
    entanglement_blocks = "crz"
    entanglement = "circular"
    skip_final_rotation_layer = True

    circuit = twolocal_tpl(
        nb_qubits=nb_qubits,
        repetitions=repetitions,
        rotation_blocks=rotation_blocks,
        entanglement_blocks=entanglement_blocks,
        entanglement=entanglement,
        skip_final_rotation_layer=skip_final_rotation_layer,
        name="sim_circuit_18_%d_",
        verbose=verbose,
    )

    return circuit

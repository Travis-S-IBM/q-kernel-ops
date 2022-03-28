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

from qiskit import QuantumCircuit
from .circuit_tpl import twolocal_tpl


def circuit_10(width=4, layer=1, verbose=False) -> QuantumCircuit:
    """Template circuit 10

    Args:
        width: number of qubits
        layer: number of repetitions
        verbose: True/False

    Return:
        The circuit generate
    """
    circuit = twolocal_tpl(
        nb_qubits=width,
        repetitions=layer,
        rotation_blocks=["ry"],
        entanglement_blocks="cz",
        entanglement="circular",
        skip_final_rotation_layer=False,
        name="sim_circuit_10_%d_",
        verbose=verbose,
    )

    return circuit

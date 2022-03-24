"""
#############################################
#
# kernel_circuit.py
#
# circuit generation for kernel
#
#
#############################################
"""

from qiskit import QuantumCircuit
import numpy as np


def kernel_circuit(
    circuit: QuantumCircuit, seed1: int, seed2: int, verbose=False
) -> QuantumCircuit:
    """Function to create the kernel circuit.

    Args:
        circuit: the template circuit
        seed1: seed for the x axes
        seed2: seed for the y axes
        verbose: True/False

    Return:
        The generate circuit without measurement
    """
    template = circuit

    np.random.seed(seed1)
    x_axe = np.random.uniform(size=template.num_parameters)
    np.random.seed(seed2)
    y_axe = np.random.uniform(size=template.num_parameters)

    kernel_cirq = QuantumCircuit(template.num_qubits)
    kernel_cirq.append(
        template.inverse().bind_parameters(x_axe), list(range(template.num_qubits))
    )
    kernel_cirq.append(
        template.inverse().bind_parameters(y_axe), list(range(template.num_qubits))
    )

    if verbose:
        print(kernel_cirq.decompose())

    return kernel_cirq

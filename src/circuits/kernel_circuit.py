#!/usr/bin/python3

#############################################
#
# kernel_circuit.py
#
# circuit generation for kernel
#
#
#############################################

from qiskit import QuantumCircuit
import numpy as np


def kernel_circuit(circuit: QuantumCircuit, seed1: int, seed2: int, verbose=False) -> QuantumCircuit:
    template = circuit
    seed1 = seed1
    seed2 = seed2

    np.random.seed(seed1)
    x = np.random.uniform(size=template.num_parameters)
    np.random.seed(seed2)
    y = np.random.uniform(size=template.num_parameters)

    kernel_cirq = QuantumCircuit(template.num_qubits)
    kernel_cirq.append(
        template.inverse().bind_parameters(x), [i for i in range(template.num_qubits)]
    )
    kernel_cirq.append(
        template.inverse().bind_parameters(y), [i for i in range(template.num_qubits)]
    )

    if verbose:
        print(kernel_cirq.decompose())

    return kernel_cirq

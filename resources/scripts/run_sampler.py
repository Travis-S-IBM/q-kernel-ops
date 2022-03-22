#!/usr/bin/python3

#############################################
#
# run_sampler.py
#
# Runtime launcher for sampler program.
# doc : https://cloud.ibm.com/docs/quantum-computing?topic=quantum-computing-example-sampler
#
#############################################

from qiskit_ibm_runtime import IBMRuntimeService, IBMSampler
from qiskit import QuantumCircuit
import numpy as np


def run_sampler(circuit: QuantumCircuit, token: str, shots=1024, seed1=42, verbose=False):
    circuit = circuit
    token = token
    shots = shots
    np.random.seed(seed=seed1)
    theta = np.random.rand(len(circuit.parameters))

    service = IBMRuntimeService(auth="legacy", token=token, instance="ibm-q/open/main")
    sampler_factory = IBMSampler(service=service, backend="ibmq_qasm_simulator")

    with sampler_factory(circuits=circuit) as sampler:
        result = sampler(circuit_indices=[0], shots=shots, parameter_values=[theta])
        if verbose:
            print(result)

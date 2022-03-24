#!/usr/bin/python3

#############################################
#
# run_sampler.py
#
# Runtime launcher for sampler program.
# doc : https://cloud.ibm.com/docs/quantum-computing?topic=quantum-computing-example-sampler
#
#############################################

from qiskit_ibm_runtime import IBMRuntimeService, IBMSampler, SamplerResult
from qiskit import QuantumCircuit


def run_sampler(
    circuits: [QuantumCircuit], auth: str, token: str, backend="ibmq_qasm_simulator", shots=1024, verbose=False
) -> SamplerResult:
    circuits = circuits
    token = token
    auth = auth
    shots = shots
    backend = backend
    
    if backend =! "statevector_simulator":
        for cirq in circuits:
            cirq.measure_all()

    service = IBMRuntimeService(auth=auth, token=token, instance="ibm-q/open/main")
    sampler_factory = IBMSampler(service=service, backend=backend)

    with sampler_factory(circuits=circuits) as sampler:
        result = sampler(circuit_indices=[i for i in range(len(circuits))], shots=shots)
        if verbose:
            print(result)

        return result

"""
#############################################
#
# run_sampler.py
#
# Runtime launcher for sampler program.
# doc : https://cloud.ibm.com/docs/quantum-computing?topic=quantum-computing-example-sampler
#
#############################################
"""

from qiskit_ibm_runtime import IBMRuntimeService, IBMSampler, SamplerResult
from qiskit import QuantumCircuit


def run_sampler(
    circuits: [QuantumCircuit], backend="ibmq_qasm_simulator", shots=1024, verbose=False
) -> SamplerResult:
    """Function to run the final circuit on quantum computer.

    Args:
        circuits: list of circuits
        backend: quantum computer name or simulator
        shots: number of shots
        verbose: True/False

    Return:
        Result from the running
    """
    circuits = circuits
    shots = shots
    backend = backend

    if backend != "statevector_simulator":
        for cirq in circuits:
            cirq.measure_all()

    service = IBMRuntimeService()
    sampler_factory = IBMSampler(service=service, backend=backend)

    with sampler_factory(circuits=circuits) as sampler:
        result = sampler(circuit_indices=list(range(len(circuits))), shots=shots)
        if verbose:
            print(result)

        return result

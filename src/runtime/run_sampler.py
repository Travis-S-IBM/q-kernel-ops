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
from typing import Tuple, List
from time import time

from qiskit_ibm_runtime import IBMRuntimeService, IBMSampler, SamplerResult
from qiskit import QuantumCircuit


def run_sampler(
    circuits: [QuantumCircuit], backend="ibmq_qasm_simulator", shots=1024, verbose=False
) -> Tuple[SamplerResult, List[str, float, float]]:
    """Function to run the final circuit on quantum computer.

    Args:
        circuits: list of circuits
        backend: quantum computer name or simulator
        shots: number of shots
        verbose: True/False

    Return:
        Result from the running
    """
    if backend != "simulator_statevector":
        for cirq in circuits:
            cirq.measure_all()

    service = IBMRuntimeService()
    sampler_factory = IBMSampler(service=service, backend=backend)

    with sampler_factory(circuits=circuits) as sampler:
        start_time = time()
        result = sampler(circuit_indices=list(range(len(circuits))), shots=shots)

        while result.status() == "in queue":
            pass
        time_queue = time() - start_time
        while result.status() == "running":
            pass
        time_simu = time() - time_queue

        if verbose:
            print(result)

        telemetry_info = [result.job_id, time_queue, time_simu]
        return result, telemetry_info

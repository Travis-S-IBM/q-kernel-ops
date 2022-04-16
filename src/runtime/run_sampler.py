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
from typing import Tuple
from time import time

from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit import QuantumCircuit


def run_sampler(
    circuits: [QuantumCircuit], backend="ibmq_qasm_simulator", shots=1024, verbose=False
) -> Tuple[dict, list]:
    """Function to run the final circuit on quantum computer.

    Args:
        circuits: list of circuits
        backend: quantum computer name or simulator
        shots: number of shots
        verbose: True/False

    Return:
        Result from the running + telemetry info
    """
    if backend != "simulator_statevector":
        for cirq in circuits:
            cirq.measure_all()

    service = QiskitRuntimeService()
    program_inputs = {
        "circuits": circuits,
        "circuit_indices": list(range(len(circuits))),
        "run_options": {"shots": shots},
    }

    options = {"backend_name": backend}

    start_time = time()

    job = service.run(
        program_id="sampler",
        options=options,
        inputs=program_inputs,
    )

    while str(job.status()) == "JobStatus.QUEUED":
        pass
    time_queue = time() - start_time
    while str(job.status()) == "JobStatus.RUNNING":
        pass
    time_simu = time() - time_queue

    result = job.result()
    if verbose:
        print(result)

    telemetry_info = [job.job_id, time_queue, time_simu]
    return result, telemetry_info

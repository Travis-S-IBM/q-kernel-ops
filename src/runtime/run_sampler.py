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
from exception import known_exception


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

    # Runtime exceptions
    try:
        start_time = time()

        # Launch exceptions
        try:
            job = service.run(
                program_id="sampler",
                options=options,
                inputs=program_inputs,
            )
        except Exception as launch_error:  # pylint: disable=broad-except
            tele_comment = known_exception(str(launch_error))
            telemetry_info = ["None", 0, 0, tele_comment]
            catch_exception = str(launch_error)
            result = {"quasi_dists": [], "metadata": []}
            return result, telemetry_info, catch_exception

        while str(job.status()) == "JobStatus.QUEUED":
            pass
        time_queue = time() - start_time

        # Simulation exceptions
        try:
            while str(job.status()) == "JobStatus.RUNNING":
                pass
            result = job.result()
        except Exception as simu_error:  # pylint: disable=broad-except
            tele_comment = known_exception(str(simu_error))
            telemetry_info = [job.job_id, time_queue, 0, tele_comment]
            catch_exception = str(simu_error)
            result = {"quasi_dists": [], "metadata": []}
            return result, telemetry_info, catch_exception

        time_simu = time() - time_queue - start_time

    except Exception as runtime_error:  # pylint: disable=broad-except
        tele_comment = known_exception(str(runtime_error))
        telemetry_info = ["None", 0, 0, tele_comment]
        catch_exception = str(runtime_error)
        result = {"quasi_dists": [], "metadata": []}
        return result, telemetry_info, catch_exception

    if verbose:
        print(result)

    tele_comment = "SUCCESS"
    catch_exception = "None"

    telemetry_info = [job.job_id, time_queue, time_simu, tele_comment]
    return result, telemetry_info, catch_exception

"""
#############################################
#
# run_runtime.py
#
# Runtime launcher for program.
#
#
#############################################
"""
from typing import Tuple
from time import time

from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit import QuantumCircuit
from src.exception import known_exception


def run_runtime(
    circuits: [QuantumCircuit], backend="ibmq_qasm_simulator", shots=1024, verbose=False
) -> Tuple[dict, list, str, str]:
    """Function to run the final circuit on quantum computer.

    Args:
        circuits: list of circuits
        backend: quantum computer name or simulator
        shots: number of shots
        verbose: True/False

    Return:
        Result from the running + telemetry info
    """
    if backend == "simulator_statevector":
        program_id = "circuit-runner"
    else:
        for cirq in circuits:
            cirq.measure_all()
        program_id = "sampler"

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
                program_id=program_id,
                options=options,
                inputs=program_inputs,
            )
        except Exception as launch_error:  # pylint: disable=broad-except
            tele_comment = known_exception(str(launch_error))
            telemetry_info = ["Null", 0, 0, tele_comment]
            catch_exception = str(launch_error)
            if program_id == "circuit-runner":
                result = {"results": [], "metadata": []}
            if program_id == "sampler":
                result = {"quasi_dists": [], "metadata": {}}
            return result, telemetry_info, catch_exception, program_id

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
            time_simu = time() - time_queue - start_time
            telemetry_info = [job.job_id, time_queue, time_simu, tele_comment]
            catch_exception = str(simu_error)
            if program_id == "circuit-runner":
                result = {"results": [], "metadata": []}
            if program_id == "sampler":
                result = {"quasi_dists": [], "metadata": []}
            return result, telemetry_info, catch_exception, program_id

        time_simu = time() - time_queue - start_time

    except Exception as runtime_error:  # pylint: disable=broad-except
        tele_comment = known_exception(str(runtime_error))
        telemetry_info = ["Null", 0, 0, tele_comment]
        catch_exception = str(runtime_error)
        if program_id == "circuit-runner":
            result = {"results": [], "metadata": []}
        elif program_id == "sampler":
            result = {"quasi_dists": [], "metadata": []}
        return result, telemetry_info, catch_exception, program_id

    if verbose:
        print(result)

    tele_comment = "SUCCESS"
    catch_exception = "None"

    telemetry_info = [job.job_id, time_queue, time_simu, tele_comment]
    return result, telemetry_info, catch_exception, program_id

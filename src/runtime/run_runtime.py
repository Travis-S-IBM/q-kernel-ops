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
from time import time

from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit import QuantumCircuit
from src.exception import known_exception


class Runtime:
    """Runtime class.
    Everything about Runtime object.
    """

    def __init__(self, payload_limit: int = 2e9):
        """Runtime init.

        Args:
            payload_limit: limit size for each part of the payload to send to the Runtime
        """
        self.circuits = []
        self.backend = "ibmq_qasm_simulator"
        self.shots = 1024
        self.payload_limit = payload_limit

        self.program_id = "Null"
        self.job_id = "Null"
        self.time_queue = 0
        self.time_simu = 0
        self.tele_comment = "SUCCESS"
        self.catch_exception = None
        self.result = {}

    def run_runtime(
        self,
        circuits: [QuantumCircuit],
        backend="ibmq_qasm_simulator",
        shots=1024,
        verbose=False,
    ) -> None:
        """Function to run the final circuit on quantum computer.

        Args:
            circuits: list of circuits
            backend: quantum computer name or simulator
            shots: number of shots
            verbose: True/False

        Return:
            Result from the running + telemetry info
        """
        self.circuits = circuits
        self.backend = backend
        self.shots = shots

        if self.backend == "simulator_statevector":
            self.program_id = "circuit-runner"
        else:
            for cirq in self.circuits:
                cirq.measure_all()
            self.program_id = "sampler"

        service = QiskitRuntimeService()
        program_inputs = {
            "circuits": self.circuits,
            "circuit_indices": list(range(len(self.circuits))),
            "run_options": {"shots": self.shots},
        }

        options = {"backend_name": self.backend}

        # Runtime exceptions
        try:
            start_time = time()

            # Launch exceptions
            try:
                job = service.run(
                    program_id=self.program_id,
                    options=options,
                    inputs=program_inputs,
                )
            except Exception as launch_error:  # pylint: disable=broad-except
                self.tele_comment = known_exception(str(launch_error))
                self.catch_exception = str(launch_error)
                if self.program_id == "circuit-runner":
                    self.result = {"results": [], "metadata": []}
                if self.program_id == "sampler":
                    self.result = {"quasi_dists": [], "metadata": []}
                return

            while str(job.status()) == "JobStatus.QUEUED":
                pass
            self.time_queue = time() - start_time
            self.job_id = job.job_id

            # Simulation exceptions
            try:
                while str(job.status()) == "JobStatus.RUNNING":
                    pass
                self.result = job.result()
            except Exception as simu_error:  # pylint: disable=broad-except
                self.time_simu = time() - self.time_queue - start_time
                self.tele_comment = known_exception(str(simu_error))
                self.catch_exception = str(simu_error)
                if self.program_id == "circuit-runner":
                    self.result = {"results": [], "metadata": []}
                if self.program_id == "sampler":
                    self.result = {"quasi_dists": [], "metadata": []}
                return

            self.time_simu = time() - self.time_queue - start_time

        except Exception as runtime_error:  # pylint: disable=broad-except
            self.tele_comment = known_exception(str(runtime_error))
            self.catch_exception = str(runtime_error)
            if self.program_id == "circuit-runner":
                self.result = {"results": [], "metadata": []}
            elif self.program_id == "sampler":
                self.result = {"quasi_dists": [], "metadata": []}
            return

        if verbose:
            print(self.result)

        self.tele_comment = "SUCCESS"

        return

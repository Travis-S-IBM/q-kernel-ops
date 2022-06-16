"""
#############################################
#
# kernel.py
#
# function for kernel programs
#
#
#############################################
"""

import sys
import copy
import math
from pympler import asizeof

from src.circuits import circuit_2, circuit_5, circuit_10, circuit_18, kernel_circuit
from src.data import kernel_metadata, kernel_telemetry
from src.runtime import Runtime


class Kernel:
    """Kernel class.
    Everything about Kernel object.
    """

    def __init__(
        self,
        circuit_tpl_id: [int],
        seed_x: [int],
        seed_y: [int],
        width: int = 4,
        layer: int = 1,
        backend: str = "ibmq_qasm_simulator",
        shots: int = 1024,
    ):
        """Kernel init.

        Args:
            circuit_tpl_id: list of circuit id to run as template
            width: number of qubits
            layer: number of reps for the tpl
            seed_x: seed for x axes
            seed_y: seed for y axes
            backend: backend for running circuit
            shots: number of shots for the circuit
        """
        self.circuit_tpl_id = circuit_tpl_id
        self.seed_x = seed_x
        self.seed_y = seed_y
        self.width = width
        self.layer = layer
        self.backend = backend
        self.shots = shots

        self.circuits_tpl = []
        self.kernel_cirq = []

        self.list_runtimes = []
        self.run_result = {}

    def gen_circuits_tpl(self):
        """Function to gen template circuits.

        Args:
            circuit_tpl_id: list of circuit id to run as template
            width: number of qubits
            layer: number of reps for the tpl
        Returns:
            List of template quantum circuits
        """
        for tpl_id in self.circuit_tpl_id:
            if tpl_id == 2:
                self.circuits_tpl.append(circuit_2(width=self.width, layer=self.layer))
            elif tpl_id == 5:
                self.circuits_tpl.append(circuit_5(width=self.width, layer=self.layer))
            elif tpl_id == 10:
                self.circuits_tpl.append(circuit_10(width=self.width, layer=self.layer))
            elif tpl_id == 18:
                self.circuits_tpl.append(circuit_18(width=self.width, layer=self.layer))
            else:
                print("Please chooce a circuit_tpl_id between [2, 5, 10, 18, X]")
                sys.exit(1)

    def gen_kernel_circuits(self):
        """Function to generate the kernel circuits.

        Args:
            circuits_tpl: list of template quantum circuits
            seed_x: seed for x axes
            seed_y: seed for y axes
        Return:
            list of kernel circuits
        """
        for tpl in self.circuits_tpl:
            for index, _ in enumerate(self.seed_x):
                self.kernel_cirq.append(
                    kernel_circuit(
                        circuit=tpl,
                        seed1=self.seed_x[index],
                        seed2=self.seed_y[index],
                    )
                )

    def exec_circuits(self) -> str:
        """Function to execute the circuits through Runtime and generate telemetry and metadata.

        Returns:
            Name of the generate metadata file or the error.
        """
        run = Runtime()
        nb_split = 1

        def split_list(my_list, nb_split):
            for index in range(0, len(my_list), nb_split):
                yield my_list[index : index + nb_split]

        if asizeof.asizeof(self.kernel_cirq) >= run.payload_limit:
            nb_split = math.ceil(asizeof.asizeof(self.kernel_cirq) / run.payload_limit)

        split_circuit = split_list(
            self.kernel_cirq, round(len(self.kernel_cirq) / nb_split)
        )

        for split in list(split_circuit):

            run.run_runtime(
                circuits=split,
                backend=self.backend,
                shots=self.shots,
            )
            kernel_telemetry(
                circuit_tpl_id=self.circuit_tpl_id,
                job_id=run.job_id,
                time_queue=float(run.time_queue),
                time_simu=float(run.time_simu),
                payload_size=asizeof.asizeof(run.circuits),
                width=self.width,
                layer=self.layer,
                shots=self.shots,
                program_id=run.program_id,
                nb_circuits=len(run.circuits),
                comment=run.tele_comment,
            )

            if run.catch_exception is not None:
                if run.tele_comment == "Unknown Error":
                    return_str = (
                        "Telemetry complete but Runtime failed ! "
                        + run.tele_comment
                        + " \nException::"
                        + run.catch_exception
                    )
                else:
                    return_str = (
                        "Telemetry complete but Runtime failed ! " + run.tele_comment
                    )

                return return_str

            self.list_runtimes.append(copy.deepcopy(run))

        if run.program_id == "sampler":
            list_quasi_dists = []
            list_metadata = []

            for runtime in self.list_runtimes:
                new_quasi = runtime.result["quasi_dists"]
                list_quasi_dists = [*list_quasi_dists, *new_quasi]
                new_metadata = runtime.result["metadata"]
                list_metadata = [*list_metadata, *new_metadata]
            self.run_result = {
                "quasi_dists": list_quasi_dists,
                "metadata": list_metadata,
            }

        if run.program_id == "circuit-runner":
            list_results = []

            for runtime in self.list_runtimes:
                new_results = runtime.result["results"]
                list_results = [*list_results, *new_results]
            self.run_result = {"results": list_results, "metadata": {}}

        job_id = []
        for result in self.list_runtimes:
            job_id.append(result.job_id)

        return kernel_metadata(
            circuit_tpl_id=self.circuit_tpl_id,
            job_id=job_id,
            width=self.width,
            seed1=self.seed_x,
            seed2=self.seed_y,
            backend=self.backend,
            runtime_result=self.run_result,
        )
